#!/usr/bin/env python3
"""Build DATA/registry/ADC_TARGET_SEED_UNIVERSE.tsv (Module A output) per schemas/target_seed.tsv.

Source: the two Module A source locations declared in config/external_sources.yaml,
resolved per-machine via their path_env_var (ADCDB_PUBLISHED_PATH, ADCDB_CLAUDE_REDO_PATH
in that file today, but this script reads the YAML for the var names -- it does not
hardcode them). Fails closed if either env var is unset -- never falls back to the
example_local_path.

This is a canonical generated artifact, so every reconciliation step below hard-fails
rather than warning-and-skipping: a partial or stale seed universe is worse than no
seed universe, because nothing downstream would know it was silently short a target.

Inputs joined:
  - $ADCDB_CLAUDE_REDO_PATH/DATA/feasibility/adc_candidates.tsv
      curated known-ADC-asset registry. Only status=VALIDATED rows with a recognized
      clinical stage (Approved/Phase1/2/3) count as "expected" -- everything else is
      out of scope for this v1 build, not silently included or silently dropped.
  - DATA/reference/adcdb_asset_antigen_crossref.tsv (checked in, see DATA/reference/README.md)
      each expected asset's antigen (surface target), manually cross-referenced against
      $ADCDB_PUBLISHED_PATH/ADCs/*.md -- not re-derived here. Its asset_entity_id set
      must exactly match the expected-candidate set computed above: any candidate missing
      from the crossref, any crossref row referencing a candidate that isn't expected, and
      any duplicate asset_entity_id are all hard failures, not warnings. A row's
      resolution_status must be RESOLVED_DIRECT, RESOLVED_BACKLINK, or
      UNRESOLVED_SOURCE_GAP; only UNRESOLVED_SOURCE_GAP may have an empty
      antigen_display_name, and only a RESOLVED_* row may have a non-empty one.
  - $ADCDB_PUBLISHED_PATH/Antigens/<antigen_display_name>.md
      per-antigen General Information table: Gene Name, HGNC ID, Antigen ID. A RESOLVED_*
      crossref row whose antigen file is missing, or whose file has no parseable Gene Name,
      is a hard failure -- a target that was resolvable when the crossref was built must
      not silently disappear from the output because a file moved.
  - DATA/reference/uniprot_accession_map.tsv (checked in)
      gene_symbol -> UniProt accession (the antigen pages carry a UniProt *entry name* like
      ERBB2_HUMAN but not the accession itself). Any resolved target gene missing from this
      map is a hard failure, not an UNKNOWN placeholder -- update the map first.

human_adc_exposure_evidence is deliberately NOT derived from adcdb_highest_clinical_stage:
"a clinical trial exists / entered clinical development" (what stage=PHASE1/2/3 shows) and
"documented human dosing exposure exists" are different claims, and adc_candidates.tsv does
not carry an explicit per-asset dosing-evidence field. Only APPROVED (which by definition
means patients were dosed) sets YES; PHASE1/2/3-only targets get UNKNOWN, not an
automatic upgrade from stage.

Scope of this v1 build: only assets present in adc_candidates.tsv (an ADC construct already
approved or dosed in a human trial). This yields derisking_tier=A_CLINICAL for every row --
it does NOT enumerate ADCdb's broader ~300-antigen universe (B_PRECLINICAL_ADC /
C_ANTIBODY_OR_BIOLOGY_ONLY tier candidates), which is future work. See notes column and
reports/PROJECT_STATUS.md.

Usage: python3 scripts/build_target_seed_universe.py [--as-of YYYY-MM-DD]
Self-test (distillation logic only, no external sources needed):
       python3 scripts/test_build_target_seed_universe.py
"""
import argparse
import csv
import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

STAGE_RANK = {"APPROVED": 4, "PHASE3": 3, "PHASE2": 2, "PHASE1": 1}


def normalize_stage(raw):
    raw = raw.strip().upper()
    if raw == "APPROVED":
        return "APPROVED"
    m = re.match(r"PHASE(\d)", raw)
    if m:
        return f"PHASE{m.group(1)}"
    return raw or "UNKNOWN"


def payload_token(raw):
    raw = raw.strip()
    m = re.match(r"^([A-Za-z0-9\-]+)", raw)
    if not m:
        return raw
    token = m.group(1)
    if token.lower() in ("an", "a"):
        low = raw.lower()
        if "pbd" in low:
            return "PBD dimer"
        if "exatecan" in low:
            return "exatecan-derivative (topo1i)"
        return raw
    return token


STAGE_QUALIFIERS = re.compile(
    r"^(recurrent|refractory|relapsed( or)?( refractory)?|advanced|metastatic|"
    r"stage\s+[ivx]+[ab]?|ann arbor stage\s+[ivx]+[ab]?|adult|childhood|"
    r"newly diagnosed|untreated|progressive|persistent)\s+",
    re.IGNORECASE,
)

CRC_RELEVANT = re.compile(r"colorectal|colon cancer|colon carcinoma|colon\b|rectal", re.IGNORECASE)
NEGATIVE_CONTEXT = re.compile(r"\b(excluding|except|non-|exclude[sd]?)\b", re.IGNORECASE)


def split_indications(raw):
    """Split a raw indication-list string on ';' at parenthesis depth 0 only, so
    labels containing cytogenetic notation like 't(9;22)(q34.1;q11.2)' (a real pattern
    in this source) don't get shredded into fragments like '22)(q34.1'."""
    terms = []
    buf = []
    depth = 0
    for ch in raw:
        if ch == "(":
            depth += 1
            buf.append(ch)
        elif ch == ")":
            depth = max(0, depth - 1)
            buf.append(ch)
        elif ch == ";" and depth == 0:
            terms.append("".join(buf))
            buf = []
        else:
            buf.append(ch)
    if buf:
        terms.append("".join(buf))
    return terms


def distill_cancer_types(indication_strings, cap=8):
    """Collapse a raw NCI-thesaurus-style indication list to a capped set of root cancer
    types by stripping staging/treatment-history qualifier prefixes and deduping
    case-insensitively, keeping the shortest surviving surface form per root. A
    colorectal/colon/rectal-relevant root term is surfaced first (this repo's scope is a
    CRC atlas -- alphabetical truncation must not silently hide CRC precedent) UNLESS the
    term itself carries explicit negative/exclusion context (e.g. 'Excluding ... Colorectal
    Cancer'), which is never counted as precedent. `cap` bounds the total number of terms
    shown (CRC-relevant terms included), not just the non-CRC remainder."""
    seen = {}
    total_raw = set()
    for s in indication_strings:
        for term in split_indications(s):
            term = term.strip()
            if not term:
                continue
            total_raw.add(term)
            core = term
            changed = True
            while changed:
                new = STAGE_QUALIFIERS.sub("", core)
                changed = new != core
                core = new
            key = core.lower()
            if key not in seen or len(term) < len(seen[key]):
                seen[key] = core if core else term
    distinct = sorted(seen.values())

    def is_positive_crc(t):
        return bool(CRC_RELEVANT.search(t)) and not NEGATIVE_CONTEXT.search(t)

    crc_terms = [t for t in distinct if is_positive_crc(t)]
    other_terms = [t for t in distinct if t not in crc_terms]

    crc_shown = crc_terms[:cap]
    other_shown = other_terms[: max(0, cap - len(crc_shown))]
    shown = crc_shown + other_shown
    truncated = len(distinct) - len(shown)
    label = "; ".join(shown)
    if truncated > 0:
        label += f" (+{truncated} more distinct root terms, {len(total_raw)} raw indication strings total)"
    return label


def parse_antigen_file(path):
    text = path.read_text(encoding="utf-8", errors="replace")
    gene = re.search(r"\|\s*Gene Name\s*\|\s*([^\|]+?)\s*\|", text)
    hgnc = re.search(r"\|\s*HGNC ID\s*\|\s*([^\|]+?)\s*\|", text)
    aid = re.search(r'id:\s*"([^"]+)"', text)
    return {
        "gene_symbol": gene.group(1).strip() if gene else None,
        "hgnc_id": hgnc.group(1).strip() if hgnc else None,
        "antigen_id": aid.group(1).strip() if aid else None,
    }


def resolve_env_path(var_name):
    val = os.environ.get(var_name)
    if not val:
        print(
            f"ERROR: {var_name} is not set. This script resolves Module A source "
            f"locations only via config/external_sources.yaml's path_env_var -- it will "
            f"not fall back to any example_local_path. Set {var_name} and re-run.",
            file=sys.stderr,
        )
        sys.exit(1)
    p = Path(val)
    if not p.is_dir():
        print(f"ERROR: {var_name}={val} is not a directory.", file=sys.stderr)
        sys.exit(1)
    return p


def load_external_sources_config(path):
    """Minimal, targeted extraction of the module_a_derisked_target_universe.sources
    list's `id:`/`path_env_var:` pairs from config/external_sources.yaml. This is not a
    general YAML parser (scripts/ stays dependency-free, no PyYAML requirement) -- it is
    intentionally narrow to this one known structure, so the env var names actually come
    from the YAML instead of being duplicated as string literals in this script."""
    if not path.is_file():
        print(f"ERROR: {path} not found.", file=sys.stderr)
        sys.exit(1)
    sources = {}
    current_id = None
    for line in path.read_text().splitlines():
        m_id = re.match(r"\s*-\s*id:\s*(\S+)", line)
        if m_id:
            current_id = m_id.group(1)
            continue
        m_var = re.match(r"\s*path_env_var:\s*(\S+)", line)
        if m_var and current_id:
            sources[current_id] = m_var.group(1)
            current_id = None
    for expected in ("adcdb_published", "adcdb_claude_redo"):
        if expected not in sources:
            print(
                f"ERROR: could not find a 'path_env_var' for source id '{expected}' in "
                f"{path} -- the YAML structure may have changed; update this parser.",
                file=sys.stderr,
            )
            sys.exit(1)
    return sources


def load_tsv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--as-of", default=None, help="last_synced date stamp, default: today")
    args = ap.parse_args()
    import datetime

    as_of = args.as_of or datetime.date.today().isoformat()

    env_vars = load_external_sources_config(REPO_ROOT / "config" / "external_sources.yaml")
    adcdb_published = resolve_env_path(env_vars["adcdb_published"])
    adcdb_claude_redo = resolve_env_path(env_vars["adcdb_claude_redo"])

    candidates_path = adcdb_claude_redo / "DATA" / "feasibility" / "adc_candidates.tsv"
    if not candidates_path.is_file():
        print(f"ERROR: {candidates_path} not found.", file=sys.stderr)
        sys.exit(1)
    all_candidates = load_tsv(candidates_path)
    candidates = {r["entity_id"]: r for r in all_candidates}

    # Expected set: only status=VALIDATED rows with a recognized clinical stage are in
    # scope for this A_CLINICAL-tier v1 build.
    expected_ids = {
        r["entity_id"]
        for r in all_candidates
        if r.get("status") == "VALIDATED" and normalize_stage(r["stage"]) in STAGE_RANK
    }

    crossref_path = REPO_ROOT / "DATA" / "reference" / "adcdb_asset_antigen_crossref.tsv"
    crossref_rows = load_tsv(crossref_path)

    errors = []
    seen_crossref_ids = set()
    for row in crossref_rows:
        eid = row["asset_entity_id"]
        if eid in seen_crossref_ids:
            errors.append(f"duplicate asset_entity_id in crossref: {eid}")
        seen_crossref_ids.add(eid)
        status = row.get("resolution_status")
        if status not in ("RESOLVED_DIRECT", "RESOLVED_BACKLINK", "UNRESOLVED_SOURCE_GAP"):
            errors.append(f"{eid}: invalid resolution_status {status!r}")
        has_antigen = bool(row["antigen_display_name"].strip())
        if status == "UNRESOLVED_SOURCE_GAP" and has_antigen:
            errors.append(f"{eid}: resolution_status=UNRESOLVED_SOURCE_GAP but antigen_display_name is non-empty")
        if status in ("RESOLVED_DIRECT", "RESOLVED_BACKLINK") and not has_antigen:
            errors.append(f"{eid}: resolution_status={status} but antigen_display_name is empty")

    missing_from_crossref = expected_ids - seen_crossref_ids
    if missing_from_crossref:
        errors.append(
            f"{len(missing_from_crossref)} expected candidate(s) (status=VALIDATED, "
            f"recognized stage) have no crossref row: {sorted(missing_from_crossref)}"
        )
    extra_in_crossref = seen_crossref_ids - expected_ids
    if extra_in_crossref:
        errors.append(
            f"{len(extra_in_crossref)} crossref row(s) reference a candidate that is not "
            f"in the current expected set (removed, no longer VALIDATED, or a typo'd "
            f"entity_id): {sorted(extra_in_crossref)}"
        )

    if errors:
        for e in errors:
            print(f"ERROR: {e}", file=sys.stderr)
        print(
            "ERROR: DATA/reference/adcdb_asset_antigen_crossref.tsv is out of sync with "
            "adc_candidates.tsv. Regenerate/update the crossref file (see DATA/reference/README.md) "
            "before running this build -- refusing to silently emit a stale or partial seed universe.",
            file=sys.stderr,
        )
        sys.exit(1)

    antigen_cache = {}
    per_target = {}
    unresolved_gaps = []

    for row in crossref_rows:
        eid = row["asset_entity_id"]
        cand = candidates[eid]
        status = row["resolution_status"]

        if status == "UNRESOLVED_SOURCE_GAP":
            unresolved_gaps.append(row["asset_name"])
            continue

        antigen_name = row["antigen_display_name"].strip()
        if antigen_name not in antigen_cache:
            antigen_path = adcdb_published / "Antigens" / f"{antigen_name}.md"
            if not antigen_path.is_file():
                print(
                    f"ERROR: crossref marks '{row['asset_name']}' as {status} against antigen "
                    f"file '{antigen_path}', but that file no longer exists. A previously-"
                    f"resolved target must not silently drop out of the seed universe -- fix "
                    f"the crossref (mark it UNRESOLVED_SOURCE_GAP instead if the source truly "
                    f"regressed) rather than letting this build continue.",
                    file=sys.stderr,
                )
                sys.exit(1)
            parsed = parse_antigen_file(antigen_path)
            if not parsed["gene_symbol"]:
                print(
                    f"ERROR: antigen file '{antigen_path}' has no parseable Gene Name in its "
                    f"General Information table.",
                    file=sys.stderr,
                )
                sys.exit(1)
            antigen_cache[antigen_name] = parsed
        antigen = antigen_cache[antigen_name]
        gene = antigen["gene_symbol"]

        t = per_target.setdefault(gene, {
            "hgnc_id": antigen["hgnc_id"] or "UNKNOWN",
            "antigen_ids": set(),
            "asset_entity_ids": [],
            "asset_names": [],
            "stages": [],
            "indications": [],
            "payloads": set(),
        })
        t["antigen_ids"].add(antigen["antigen_id"] or "UNKNOWN")
        t["asset_entity_ids"].append(eid)
        t["asset_names"].append(cand["asset_name"])
        t["stages"].append(normalize_stage(cand["stage"]))
        t["indications"].append(cand.get("indications", ""))
        if cand.get("payload_if_known"):
            t["payloads"].add(payload_token(cand["payload_if_known"]))

    uniprot_map_path = REPO_ROOT / "DATA" / "reference" / "uniprot_accession_map.tsv"
    uniprot_map = {r["gene_symbol"]: r for r in load_tsv(uniprot_map_path)}
    missing_uniprot = sorted(g for g in per_target if g not in uniprot_map)
    if missing_uniprot:
        print(
            f"ERROR: {len(missing_uniprot)} resolved target gene(s) have no entry in "
            f"DATA/reference/uniprot_accession_map.tsv: {missing_uniprot}. Update that map "
            f"(see DATA/reference/README.md) rather than emitting UNKNOWN for a target this "
            f"build otherwise has real data for.",
            file=sys.stderr,
        )
        sys.exit(1)

    out_rows = []
    for gene in sorted(per_target):
        t = per_target[gene]
        highest_stage = max(t["stages"], key=lambda s: STAGE_RANK.get(s, 0))
        uniprot_id = uniprot_map[gene]["uniprot_accession"]
        cancer_types = distill_cancer_types(t["indications"])
        payload_precedent = "; ".join(sorted(t["payloads"])) if t["payloads"] else "UNKNOWN"
        target_id = f"tgt_{gene.lower()}"
        source_reference = (
            "adc_candidates.tsv:" + ";".join(t["asset_entity_ids"])
            + " | antigen:" + ";".join(sorted(t["antigen_ids"]))
        )
        # human_adc_exposure_evidence is deliberately decoupled from clinical stage: a
        # PHASE1/2/3 entry shows a trial exists, not that dosing is documented here.
        # Only APPROVED (which by definition means patients were dosed) sets YES.
        exposure = "YES" if "APPROVED" in t["stages"] else "UNKNOWN"
        notes = (
            "derisking_tier=A_CLINICAL per ADC_ATLAS_DATASET_CONTRACT.md Module A admission "
            "gate definition (a real ADC construct against this target is approved or has "
            "entered a human trial per adc_candidates.tsv, status=VALIDATED); this does not "
            "by itself establish CRC/mCRC relevance -- see adcdb_cancer_types_with_precedent "
            "for whether CRC-family terms are among the documented indications. "
            "human_adc_exposure_evidence=YES only when an approved asset exists for this "
            "target (approval implies documented dosing); a clinical-stage-only target gets "
            "UNKNOWN here even though its derisking_tier is still A_CLINICAL -- trial "
            "registration is not the same claim as documented human exposure."
        )
        out_rows.append({
            "target_id": target_id,
            "target_symbol": gene,
            "hgnc_id": t["hgnc_id"],
            "uniprot_id": uniprot_id,
            "adcdb_highest_clinical_stage": highest_stage,
            "adcdb_cancer_types_with_precedent": cancer_types,
            "adcdb_payload_precedent": payload_precedent,
            "human_adc_exposure_evidence": exposure,
            "derisking_tier": "A_CLINICAL",
            "repurposing_status": "ACTIVE",
            "source_id": "adcdb_claude_redo;adcdb_published",
            "source_reference": source_reference,
            "last_synced": as_of,
            "notes": notes,
        })

    out_path = REPO_ROOT / "DATA" / "registry" / "ADC_TARGET_SEED_UNIVERSE.tsv"
    header = [
        "target_id", "target_symbol", "hgnc_id", "uniprot_id",
        "adcdb_highest_clinical_stage", "adcdb_cancer_types_with_precedent",
        "adcdb_payload_precedent", "human_adc_exposure_evidence",
        "derisking_tier", "repurposing_status", "source_id", "source_reference",
        "last_synced", "notes",
    ]
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=header, delimiter="\t")
        w.writeheader()
        for r in out_rows:
            w.writerow(r)

    direct = sum(1 for r in crossref_rows if r["resolution_status"] == "RESOLVED_DIRECT")
    backlink = sum(1 for r in crossref_rows if r["resolution_status"] == "RESOLVED_BACKLINK")
    print(f"Wrote {len(out_rows)} target rows to {out_path}")
    print(
        f"Asset coverage: {direct} resolved via direct ADC-file antigen wikilink, "
        f"{backlink} resolved via antigen-file backlink, "
        f"{len(unresolved_gaps)} UNRESOLVED_SOURCE_GAP (excluded): {unresolved_gaps}"
    )


if __name__ == "__main__":
    main()
