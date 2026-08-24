#!/usr/bin/env python3
"""Module B: chromosome-arm-level CNV score for GSE178318's epithelial-proxy
cells, to distinguish malignancy-consistent (CNV_HIGH) from not-confirmed
(CNV_LOW) among the cells scripts/annotate_gse178318_cell_types.py identifies
as epithelial-proxy. Method and every limitation are locked in
modules/module_b_mcrc_target_prevalence/analysis_contracts/
infercnv_lite_gse178318.md (written before this script ran) -- read that
file before trusting this script's output boundaries. This is NOT a
reproduction of GSE178318's own publication's fine-grained InferCNV; it is a
coarser, arm-level, independently-designed approximation, stated explicitly.

Reuses barcode/QC/classification logic from
scripts/annotate_gse178318_cell_types.py (same repo-relative gitignored raw
path, checksum-verified) so the epithelial-proxy population scored here is
defined identically to that script's own output. Adds one more input: the
gene->chromosome-arm mapping from this machine's local
DATA/1.Databases/HGNC_gene_id_mapping (already-fetched, read-only, not a new
download), resolved via a path_env_var like Module A/E's external sources.

Usage: python3 scripts/infercnv_lite_gse178318.py --gene CEACAM5
"""
import argparse
import csv
import gzip
import hashlib
import math
import os
import random
import re
import sys
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))
from annotate_gse178318_cell_types import (
    RAW_DIR, NON_EPITHELIAL_CATEGORIES, TREATED_PATIENTS, UNTREATED_PATIENTS,
    MIN_DETECTED_GENES, MAX_MITO_FRACTION, BATCH_OUTLIER_SD,
    resolve_files, read_lines, sample_key, load_sample_map, load_marker_set,
    classify_cell,
)

ARM_PATTERN = re.compile(r"^(\d{1,2}|X|Y)([pq])")
MIN_GENES_PER_ARM = 10
CNV_REFERENCE_PERCENTILE = 0.99


def parse_arm(chromosome_field):
    """Parse an HGNC 'Chromosome' cytogenetic-band string (e.g. '17p13.3')
    down to a coarse chromosome-arm bucket ('17p'). Returns None for
    non-standard values (withdrawn/reserved entries, unplaced/centromeric
    genes with no arm letter, multi-region strings like pseudoautosomal
    'Xp22.32 and Yp11.3') -- excluded from arm scoring rather than guessed."""
    m = ARM_PATTERN.match(chromosome_field)
    return f"{m.group(1)}{m.group(2)}" if m else None


def cell_arm_signal(arm_counts, total_umi, usable_arms):
    """Per-cell, per-arm CP10K-style normalized signal: log1p(arm raw count
    sum / total UMI * 10000). arm_counts: {arm: raw_count} for this cell."""
    return {arm: math.log1p(arm_counts.get(arm, 0) / total_umi * 10000) for arm in usable_arms}


def aggregate_cnv_score(signal, ref_mean, ref_sd, usable_arms):
    """Chi-square-like aggregate: mean of per-arm z^2 across usable arms, so
    the score isn't just proportional to the number of arms and a single
    wildly-different arm can't dominate an otherwise-flat cell."""
    z2 = [((signal[arm] - ref_mean[arm]) / ref_sd[arm]) ** 2 for arm in usable_arms]
    return sum(z2) / len(z2)


def build_populations(n_cells, passes_qc, cell_category, cell_keys, sample_map, patient_filter):
    """Reference (immune) and epithelial-proxy cell indices, tumor-site samples
    only (PRIMARY_CRC/LIVER_METASTASIS, never PBMC). patient_filter: a set of
    patient_ids to restrict to (e.g. TREATED_PATIENTS), or None for all
    patients pooled -- callers must not silently mix the two: a pooled
    population must never be reported under an indication_id that names one
    specific treatment cohort (PR #75 round-2 review; the same class of bug
    PR #74 round 1 caught for the epithelial-proxy screen itself)."""
    def keep(i):
        info = sample_map[cell_keys[i]]
        if info["specimen_type"] not in ("PRIMARY_CRC", "LIVER_METASTASIS"):
            return False
        if patient_filter is not None and info["patient_id"] not in patient_filter:
            return False
        return True
    reference_idx = [i for i in range(n_cells) if passes_qc[i] and cell_category[i] == "immune" and keep(i)]
    epithelial_idx = [i for i in range(n_cells) if passes_qc[i] and cell_category[i] == "epithelial" and keep(i)]
    return reference_idx, epithelial_idx


def score_population(reference_idx, epithelial_idx, arm_signal, usable_arms, seed, label):
    """Fit/holdout split of `reference_idx`, threshold from the held-out
    half's own 99th percentile, score `epithelial_idx` against it. `label` is
    only for the stderr diagnostics below -- it does not change any number."""
    random.seed(seed)
    if len(reference_idx) < 200:
        print(f"ERROR: [{label}] reference population too small (<200 cells, n={len(reference_idx)}) "
              f"for a stable null distribution.", file=sys.stderr)
        sys.exit(1)

    shuffled = reference_idx[:]
    random.shuffle(shuffled)
    half = len(shuffled) // 2
    ref_fit_idx, ref_holdout_idx = shuffled[:half], shuffled[half:]

    ref_arm_values = defaultdict(list)
    for i in ref_fit_idx:
        sig = arm_signal(i)
        for arm, v in sig.items():
            ref_arm_values[arm].append(v)
    ref_mean = {arm: sum(vals) / len(vals) for arm, vals in ref_arm_values.items()}
    ref_sd = {
        arm: (sum((v - ref_mean[arm]) ** 2 for v in vals) / len(vals)) ** 0.5
        for arm, vals in ref_arm_values.items()
    }
    ref_sd = {arm: (sd if sd > 1e-9 else 1e-9) for arm, sd in ref_sd.items()}

    def cnv_score(i):
        return aggregate_cnv_score(arm_signal(i), ref_mean, ref_sd, usable_arms)

    holdout_scores = sorted(cnv_score(i) for i in ref_holdout_idx)
    n_holdout = len(holdout_scores)
    threshold_idx = int(n_holdout * CNV_REFERENCE_PERCENTILE)
    threshold = holdout_scores[min(threshold_idx, n_holdout - 1)]
    print(
        f"[{label}] Reference: n={len(reference_idx)} (fit n={len(ref_fit_idx)}, holdout n={n_holdout}); "
        f"CNV_HIGH threshold (held-out half's own {CNV_REFERENCE_PERCENTILE:.0%}ile): {threshold:.4f}",
        file=sys.stderr,
    )

    all_epi_scores = sorted(cnv_score(i) for i in epithelial_idx)
    n_epithelial = len(all_epi_scores)
    print(f"[{label}] Epithelial-proxy cells scored: {n_epithelial}", file=sys.stderr)

    def pct(sorted_vals, p):
        idx = min(int(len(sorted_vals) * p), len(sorted_vals) - 1)
        return sorted_vals[idx]

    if n_epithelial:
        print(
            f"[{label}] Epithelial-proxy CNV score distribution (n={n_epithelial}): "
            f"min={all_epi_scores[0]:.3f} p10={pct(all_epi_scores, 0.10):.3f} p25={pct(all_epi_scores, 0.25):.3f} "
            f"median={pct(all_epi_scores, 0.50):.3f} p75={pct(all_epi_scores, 0.75):.3f} p90={pct(all_epi_scores, 0.90):.3f} "
            f"p99={pct(all_epi_scores, 0.99):.3f} max={all_epi_scores[-1]:.3f}",
            file=sys.stderr,
        )
    print(
        f"[{label}] Held-out reference CNV score distribution (n={n_holdout}; the threshold above is "
        f"this half's own {CNV_REFERENCE_PERCENTILE:.0%}ile, so its own exceedance rate over that "
        f"threshold is the ~1% null rate by construction, not independent evidence -- reported below "
        f"only as the honest baseline the epithelial-proxy rate is compared against): "
        f"median={pct(holdout_scores, 0.50):.3f} p90={pct(holdout_scores, 0.90):.3f} "
        f"p99={pct(holdout_scores, 0.99):.3f} (threshold={threshold:.3f})",
        file=sys.stderr,
    )

    n_epi_high = sum(1 for s in all_epi_scores if s > threshold)
    n_holdout_high = sum(1 for s in holdout_scores if s > threshold)
    epi_high_frac = n_epi_high / n_epithelial if n_epithelial else 0.0
    holdout_high_frac = n_holdout_high / n_holdout if n_holdout else 0.0
    enrichment = (epi_high_frac / holdout_high_frac) if holdout_high_frac > 0 else float("inf")
    print(
        f"[{label}] CNV_HIGH (score > threshold): epithelial-proxy {n_epi_high}/{n_epithelial} "
        f"({epi_high_frac:.2%}) vs held-out reference's own {n_holdout_high}/{n_holdout} "
        f"({holdout_high_frac:.2%}) -- enrichment ratio {enrichment:.2f}x over the reference's own "
        f"null exceedance rate at this same threshold.",
        file=sys.stderr,
    )

    return {
        "threshold": threshold, "cnv_score": cnv_score,
        "n_reference": len(reference_idx), "n_fit": len(ref_fit_idx), "n_holdout": n_holdout,
        "holdout_median": pct(holdout_scores, 0.50), "holdout_p90": pct(holdout_scores, 0.90),
        "holdout_p99": pct(holdout_scores, 0.99),
        "n_epithelial": n_epithelial,
        "epi_median": pct(all_epi_scores, 0.50) if n_epithelial else None,
        "n_epi_high": n_epi_high, "n_holdout_high": n_holdout_high,
        "epi_high_frac": epi_high_frac, "holdout_high_frac": holdout_high_frac, "enrichment": enrichment,
    }


def sha256(path):
    d = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            d.update(chunk)
    return d.hexdigest()


def load_gene_position_source_config(path):
    """Minimal, targeted extraction of the module_b_gene_position_reference.sources
    list's id: hgnc_gene_id_mapping / path_env_var: pair from config/external_sources.yaml
    -- same narrow, dependency-free parsing pattern as build_target_seed_universe.py's
    load_external_sources_config() (not shared as a common helper; each script's copy is
    scoped to the one block it actually reads, matching existing repo precedent). This is
    the source of truth for the env var name -- it must never be duplicated as a hardcoded
    string literal in this script."""
    if not path.is_file():
        print(f"ERROR: {path} not found.", file=sys.stderr)
        sys.exit(1)
    var_name = None
    current_id = None
    for line in path.read_text().splitlines():
        m_id = re.match(r"\s*-\s*id:\s*(\S+)", line)
        if m_id:
            current_id = m_id.group(1)
            continue
        m_var = re.match(r"\s*path_env_var:\s*(\S+)", line)
        if m_var and current_id == "hgnc_gene_id_mapping":
            var_name = m_var.group(1)
            break
    if not var_name:
        print(
            f"ERROR: could not find a 'path_env_var' for source id 'hgnc_gene_id_mapping' in "
            f"{path} -- the YAML structure may have changed; update this parser.",
            file=sys.stderr,
        )
        sys.exit(1)
    return var_name


def resolve_hgnc_path():
    var_name = load_gene_position_source_config(REPO_ROOT / "config" / "external_sources.yaml")
    val = os.environ.get(var_name)
    if not val:
        print(
            f"ERROR: {var_name} is not set. This script resolves the local HGNC gene-position "
            f"reference only via config/external_sources.yaml's path_env_var -- it will not "
            f"fall back to any example_local_path. Set {var_name} to the directory containing "
            f"raw/hgnc_custom_download.tsv and re-run.",
            file=sys.stderr,
        )
        sys.exit(1)
    p = Path(val) / "raw" / "hgnc_custom_download.tsv"
    if not p.is_file():
        print(f"ERROR: {p} not found.", file=sys.stderr)
        sys.exit(1)
    lock_path = REPO_ROOT / "DATA" / "reference" / "hgnc_gene_id_mapping_source_lock.tsv"
    if not lock_path.is_file():
        print(f"ERROR: {lock_path} not found.", file=sys.stderr)
        sys.exit(1)
    with open(lock_path, newline="") as f:
        lock = {r["file_name"]: r for r in csv.DictReader(f, delimiter="\t")}
    expected = lock.get(p.name, {}).get("sha256", "")
    if not expected:
        print(f"ERROR: no checksum recorded for {p.name} in {lock_path}.", file=sys.stderr)
        sys.exit(1)
    actual = sha256(p)
    if actual != expected:
        print(
            f"ERROR: checksum mismatch for {p}: lock file says {expected}, file is {actual}. "
            f"The external HGNC reference has changed since this analysis was locked -- "
            f"re-verify before proceeding, do not silently rescore against a different file.",
            file=sys.stderr,
        )
        sys.exit(1)
    return p


def build_ensg_to_arm(hgnc_path):
    ensg_to_arm = {}
    with open(hgnc_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            ensg = row.get("Ensembl gene ID", "").strip()
            chrom = row.get("Chromosome", "").strip()
            if not ensg or not chrom:
                continue
            arm = parse_arm(chrom)
            if arm:
                ensg_to_arm[ensg] = arm
    return ensg_to_arm


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gene", required=True)
    ap.add_argument("--marker-set", default=str(
        REPO_ROOT / "modules" / "module_b_mcrc_target_prevalence" / "analysis_contracts" / "cell_type_marker_set_v1.tsv"
    ))
    ap.add_argument("--seed", type=int, default=42, help="RNG seed for the reference-population split")
    args = ap.parse_args()
    gene = args.gene.strip()
    random.seed(args.seed)

    hgnc_path = resolve_hgnc_path()
    ensg_to_arm = build_ensg_to_arm(hgnc_path)
    print(f"Loaded {len(ensg_to_arm)} ENSG->arm mappings from {hgnc_path}", file=sys.stderr)

    files = resolve_files()
    barcodes = read_lines(files["GSE178318_barcodes.tsv.gz"])
    genes_raw = read_lines(files["GSE178318_genes.tsv.gz"])
    ensg_ids = [g.split("\t")[0] for g in genes_raw]
    gene_symbols = [g.split("\t")[-1] for g in genes_raw]

    sample_map_path = REPO_ROOT / "DATA" / "registry" / "GSE178318" / "sample_map.tsv"
    sample_map = load_sample_map(sample_map_path)
    cell_keys = [sample_key(b) for b in barcodes]
    if any(k == "UNPARSEABLE" for k in cell_keys):
        print("ERROR: unparseable barcode.", file=sys.stderr)
        sys.exit(1)

    marker_set = load_marker_set(args.marker_set)
    symbol_to_row = {}
    for i, sym in enumerate(gene_symbols):
        symbol_to_row.setdefault(sym, i + 1)
    category_rows = {cat: {symbol_to_row[g] for g in marker_set[cat] if g in symbol_to_row} for cat in NON_EPITHELIAL_CATEGORIES}
    category_gene_counts = {cat: len(marker_set[cat]) for cat in NON_EPITHELIAL_CATEGORIES}
    epcam_row = symbol_to_row["EPCAM"]
    mito_rows = {symbol_to_row[s] for s in gene_symbols if s.startswith("MT-") and s in symbol_to_row}
    if gene not in symbol_to_row:
        print(f"ERROR: '{gene}' not in gene index.", file=sys.stderr)
        sys.exit(1)
    target_row = symbol_to_row[gene]

    # row -> arm bucket, restricted to genes present in this dataset's index
    row_to_arm = {}
    for i, ensg in enumerate(ensg_ids):
        arm = ensg_to_arm.get(ensg)
        if arm:
            row_to_arm[i + 1] = arm
    arm_gene_counts = defaultdict(int)
    for arm in row_to_arm.values():
        arm_gene_counts[arm] += 1
    usable_arms = {arm for arm, n in arm_gene_counts.items() if n >= MIN_GENES_PER_ARM}
    print(f"{len(row_to_arm)} of {len(genes_raw)} genes resolve to an arm; {len(usable_arms)} arms have >= {MIN_GENES_PER_ARM} genes.", file=sys.stderr)

    n_cells = len(barcodes)
    total_counts = [0] * n_cells
    detected_genes = [0] * n_cells
    mito_counts = [0] * n_cells
    epcam_counts = [0] * n_cells
    target_counts = [0] * n_cells
    category_sums = {cat: [0] * n_cells for cat in NON_EPITHELIAL_CATEGORIES}
    arm_sums = {arm: [0] * n_cells for arm in usable_arms}

    row_to_cats = {}
    for cat, rows in category_rows.items():
        for r in rows:
            row_to_cats.setdefault(r, []).append(cat)

    print(f"Streaming matrix ({files['GSE178318_matrix.mtx.gz']})...", file=sys.stderr)
    header = None
    entries = 0
    with gzip.open(files["GSE178318_matrix.mtx.gz"], "rt") as f:
        for raw_line in f:
            if raw_line.startswith("%"):
                continue
            if header is None:
                header = tuple(map(int, raw_line.split()))
                continue
            row_s, col_s, val_s = raw_line.split()
            row = int(row_s)
            cell = int(col_s) - 1
            count = int(float(val_s))
            total_counts[cell] += count
            detected_genes[cell] += 1
            if row in mito_rows:
                mito_counts[cell] += count
            if row == epcam_row:
                epcam_counts[cell] = count
            if row == target_row:
                target_counts[cell] = count
            cats = row_to_cats.get(row)
            if cats:
                for cat in cats:
                    category_sums[cat][cell] += count
            arm = row_to_arm.get(row)
            if arm in usable_arms:
                arm_sums[arm][cell] += count
            entries += 1

    if header != (len(gene_symbols), n_cells, entries):
        print(f"ERROR: matrix dimension mismatch.", file=sys.stderr)
        sys.exit(1)

    # QC (identical to annotate_gse178318_cell_types.py)
    by_sample_indices = defaultdict(list)
    for i, key in enumerate(cell_keys):
        by_sample_indices[key].append(i)
    passes_qc = [False] * n_cells
    for key, idxs in by_sample_indices.items():
        log_totals = [math.log10(total_counts[i]) if total_counts[i] > 0 else 0.0 for i in idxs]
        mean_log_total = sum(log_totals) / len(log_totals)
        sd_log_total = (sum((x - mean_log_total) ** 2 for x in log_totals) / len(log_totals)) ** 0.5
        gene_vals = [detected_genes[i] for i in idxs]
        mean_genes = sum(gene_vals) / len(gene_vals)
        sd_genes = (sum((x - mean_genes) ** 2 for x in gene_vals) / len(gene_vals)) ** 0.5
        for i, log_total in zip(idxs, log_totals):
            if detected_genes[i] < MIN_DETECTED_GENES or total_counts[i] == 0:
                continue
            if mito_counts[i] / total_counts[i] > MAX_MITO_FRACTION:
                continue
            if sd_log_total > 0 and abs(log_total - mean_log_total) > BATCH_OUTLIER_SD * sd_log_total:
                continue
            if sd_genes > 0 and abs(detected_genes[i] - mean_genes) > BATCH_OUTLIER_SD * sd_genes:
                continue
            passes_qc[i] = True

    cell_category = [None] * n_cells
    for i in range(n_cells):
        if passes_qc[i]:
            cell_category[i] = classify_cell(
                total_counts[i], epcam_counts[i],
                {cat: category_sums[cat][i] for cat in NON_EPITHELIAL_CATEGORIES},
                category_gene_counts,
            )

    def arm_signal(i):
        return cell_arm_signal({arm: arm_sums[arm][i] for arm in usable_arms}, total_counts[i], usable_arms)

    # Canonical, treated-only pipeline: TE006/EV014 are keyed to
    # indication_id=mcrc_preop_chemotherapy_crlm (the same territory as
    # TE004), so both the reference population and the epithelial-proxy
    # population scored against it must be restricted to TREATED_PATIENTS
    # (COL15/COL17/COL18) -- pooling all six patients here and reporting it
    # under a treated-only indication_id was the round-2 review's blocker
    # (the same class of cohort-mismatch bug PR #74 round 1 caught).
    print("\n=== Canonical treated-only run (COL15/COL17/COL18, indication_id=mcrc_preop_chemotherapy_crlm) ===",
          file=sys.stderr)
    treated_reference_idx, treated_epithelial_idx = build_populations(
        n_cells, passes_qc, cell_category, cell_keys, sample_map, TREATED_PATIENTS)
    canonical = score_population(treated_reference_idx, treated_epithelial_idx, arm_signal, usable_arms,
                                  args.seed, "treated-only")

    # Pooled six-patient run: kept ONLY as a method diagnostic (larger n,
    # general sanity check of the score's behavior) -- never written to the
    # output TSV or used for TE006/EV014's canonical numbers, since it mixes
    # treated and treatment-naive patients under a treated-only indication_id.
    print("\n=== Pooled six-patient diagnostic (method sanity check only, NOT canonical) ===", file=sys.stderr)
    all_reference_idx, all_epithelial_idx = build_populations(
        n_cells, passes_qc, cell_category, cell_keys, sample_map, None)
    score_population(all_reference_idx, all_epithelial_idx, arm_signal, usable_arms, args.seed, "pooled-diagnostic")

    threshold = canonical["threshold"]
    cnv_score = canonical["cnv_score"]

    per_sample = defaultdict(lambda: {"n_epithelial": 0, "n_cnv_high": 0, "n_cnv_high_target_pos": 0,
                                       "n_cnv_low": 0, "n_cnv_low_target_pos": 0})
    for i in treated_epithelial_idx:
        key = cell_keys[i]
        s = per_sample[key]
        s["n_epithelial"] += 1
        score = cnv_score(i)
        if score > threshold:
            s["n_cnv_high"] += 1
            if target_counts[i] > 0:
                s["n_cnv_high_target_pos"] += 1
        else:
            s["n_cnv_low"] += 1
            if target_counts[i] > 0:
                s["n_cnv_low_target_pos"] += 1

    out_rows = []
    for key, s in sorted(per_sample.items()):
        info = sample_map[key]
        frac_high = s["n_cnv_high_target_pos"] / s["n_cnv_high"] if s["n_cnv_high"] else None
        frac_low = s["n_cnv_low_target_pos"] / s["n_cnv_low"] if s["n_cnv_low"] else None
        out_rows.append({
            "sample_key": key, "patient_id": info["patient_id"], "specimen_type": info["specimen_type"],
            "n_epithelial_proxy": s["n_epithelial"],
            "n_cnv_high": s["n_cnv_high"], "n_cnv_low": s["n_cnv_low"],
            f"{gene}_pos_frac_cnv_high": round(frac_high, 4) if frac_high is not None else "NA",
            f"{gene}_pos_frac_cnv_low": round(frac_low, 4) if frac_low is not None else "NA",
        })

    # Filename and console text deliberately avoid "confirmed" -- this method
    # is exploratory and its signal is ambiguous, not confirmatory (see the
    # analysis contract), and a filename claiming otherwise is more likely to
    # mislead a future reader than any amount of prose disclaimer.
    out_path = REPO_ROOT / "modules" / "module_b_mcrc_target_prevalence" / "results" / f"tgt_{gene.lower()}_cnv_lite_attempt.tsv"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out_rows[0].keys()), delimiter="\t")
        w.writeheader()
        for r in out_rows:
            w.writerow(r)
    print(f"\nWrote {len(out_rows)} sample rows to {out_path}")

    print(f"\nCNV_HIGH exploratory subset per sample (NOT confirmatory -- see analysis contract):")
    for r in out_rows:
        group = "TREATED" if r["patient_id"] in TREATED_PATIENTS else ("UNTREATED" if r["patient_id"] in UNTREATED_PATIENTS else "PBMC-n/a")
        print(f"  {r['sample_key']:14s} [{group:9s}] n_epi={r['n_epithelial_proxy']:5d} "
              f"CNV_HIGH={r['n_cnv_high']:5d} ({r[f'{gene}_pos_frac_cnv_high']})  "
              f"CNV_LOW={r['n_cnv_low']:5d} ({r[f'{gene}_pos_frac_cnv_low']})")


if __name__ == "__main__":
    main()
