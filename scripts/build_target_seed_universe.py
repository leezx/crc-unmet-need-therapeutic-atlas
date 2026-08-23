#!/usr/bin/env python3
"""Build DATA/registry/ADC_TARGET_SEED_UNIVERSE.tsv (Module A output) per schemas/target_seed.tsv.

Source: the two Module A source locations declared in config/external_sources.yaml,
resolved per-machine via their path_env_var (ADCDB_PUBLISHED_PATH, ADCDB_CLAUDE_REDO_PATH).
Fails closed if either env var is unset -- never falls back to the example_local_path.

Inputs joined:
  - $ADCDB_CLAUDE_REDO_PATH/DATA/feasibility/adc_candidates.tsv
      curated, VALIDATED-confidence known-ADC-asset registry (approved + clinical-stage).
  - DATA/reference/adcdb_asset_antigen_crossref.tsv (checked in, see DATA/reference/README.md)
      each asset's antigen (surface target), manually cross-referenced against
      $ADCDB_PUBLISHED_PATH/ADCs/*.md 'antigen:' wikilinks -- not re-derived here.
  - $ADCDB_PUBLISHED_PATH/Antigens/<antigen_display_name>.md
      per-antigen General Information table: Gene Name, HGNC ID, Uniprot Entry, Antigen ID.
  - DATA/reference/uniprot_accession_map.tsv (checked in)
      gene_symbol -> UniProt accession, since the antigen pages carry a UniProt *entry name*
      (e.g. ERBB2_HUMAN) but not the accession number itself.

Scope of this v1 build: only assets present in adc_candidates.tsv (an ADC construct already
approved or dosed in a human trial). This yields derisking_tier=A_CLINICAL for every row --
it does NOT enumerate ADCdb's broader ~300-antigen universe (B_PRECLINICAL_ADC /
C_ANTIBODY_OR_BIOLOGY_ONLY tier candidates), which is future work. See notes column and
reports/PROJECT_STATUS.md.

Usage: python3 scripts/build_target_seed_universe.py [--as-of YYYY-MM-DD]
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
    # a few known long-form-only payloads have no short acronym in this source
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


CRC_RELEVANT = re.compile(r"colorectal|colon cancer|colon carcinoma|rectal", re.IGNORECASE)


def distill_cancer_types(indication_strings, cap=8):
    """Collapse a raw NCI-thesaurus-style indication list to a capped set of root cancer
    types by stripping staging/treatment-history qualifier prefixes and deduping
    case-insensitively, keeping the shortest surviving surface form per root. Any
    colorectal/colon/rectal-relevant root term is always surfaced first (this repo's
    scope is a CRC atlas -- alphabetical truncation must not silently hide CRC precedent),
    with remaining cap slots filled alphabetically from the rest."""
    seen = {}
    total_raw = set()
    for s in indication_strings:
        for term in s.split(";"):
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
    crc_terms = [t for t in distinct if CRC_RELEVANT.search(t)]
    other_terms = [t for t in distinct if t not in crc_terms]
    shown = crc_terms + other_terms[: max(0, cap - len(crc_terms))]
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


def load_tsv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--as-of", default=None, help="last_synced date stamp, default: today")
    args = ap.parse_args()
    import datetime

    as_of = args.as_of or datetime.date.today().isoformat()

    adcdb_published = resolve_env_path("ADCDB_PUBLISHED_PATH")
    adcdb_claude_redo = resolve_env_path("ADCDB_CLAUDE_REDO_PATH")

    candidates_path = adcdb_claude_redo / "DATA" / "feasibility" / "adc_candidates.tsv"
    if not candidates_path.is_file():
        print(f"ERROR: {candidates_path} not found.", file=sys.stderr)
        sys.exit(1)
    candidates = {r["entity_id"]: r for r in load_tsv(candidates_path)}

    crossref_path = REPO_ROOT / "DATA" / "reference" / "adcdb_asset_antigen_crossref.tsv"
    crossref = load_tsv(crossref_path)

    uniprot_map_path = REPO_ROOT / "DATA" / "reference" / "uniprot_accession_map.tsv"
    uniprot_map = {r["gene_symbol"]: r for r in load_tsv(uniprot_map_path)}

    antigen_cache = {}
    per_target = {}
    unresolved = []

    for row in crossref:
        eid = row["asset_entity_id"]
        cand = candidates.get(eid)
        if cand is None:
            print(f"WARNING: crossref row for {eid} has no matching adc_candidates.tsv row, skipping", file=sys.stderr)
            continue
        antigen_name = row["antigen_display_name"].strip()
        if not antigen_name:
            unresolved.append(row["asset_name"])
            continue
        if antigen_name not in antigen_cache:
            antigen_path = adcdb_published / "Antigens" / f"{antigen_name}.md"
            if not antigen_path.is_file():
                print(f"WARNING: antigen file not found for '{antigen_name}' ({antigen_path}), skipping asset {row['asset_name']}", file=sys.stderr)
                unresolved.append(row["asset_name"])
                continue
            antigen_cache[antigen_name] = parse_antigen_file(antigen_path)
        antigen = antigen_cache[antigen_name]
        gene = antigen["gene_symbol"]
        if not gene:
            unresolved.append(row["asset_name"])
            continue

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

    out_rows = []
    for gene in sorted(per_target):
        t = per_target[gene]
        highest_stage = max(t["stages"], key=lambda s: STAGE_RANK.get(s, 0))
        uni = uniprot_map.get(gene)
        uniprot_id = uni["uniprot_accession"] if uni else "UNKNOWN"
        cancer_types = distill_cancer_types(t["indications"])
        payload_precedent = "; ".join(sorted(t["payloads"])) if t["payloads"] else "UNKNOWN"
        target_id = f"tgt_{gene.lower()}"
        source_reference = (
            "adc_candidates.tsv:" + ";".join(t["asset_entity_ids"])
            + " | antigen:" + ";".join(sorted(t["antigen_ids"]))
        )
        notes = (
            "derisking_tier=A_CLINICAL per ADC_ATLAS_DATASET_CONTRACT.md Module A admission "
            "gate definition (a real ADC construct against this target is approved or has been "
            "dosed in a human trial per adc_candidates.tsv, status=VALIDATED); this does not by "
            "itself establish CRC/mCRC relevance -- see adcdb_cancer_types_with_precedent for "
            "whether CRC-family terms are among the documented indications."
        )
        out_rows.append({
            "target_id": target_id,
            "target_symbol": gene,
            "hgnc_id": t["hgnc_id"],
            "uniprot_id": uniprot_id,
            "adcdb_highest_clinical_stage": highest_stage,
            "adcdb_cancer_types_with_precedent": cancer_types,
            "adcdb_payload_precedent": payload_precedent,
            "human_adc_exposure_evidence": "YES",
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

    print(f"Wrote {len(out_rows)} target rows to {out_path}")
    if unresolved:
        print(f"UNRESOLVED assets (target not assigned, excluded): {unresolved}")


if __name__ == "__main__":
    main()
