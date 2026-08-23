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


def resolve_hgnc_path():
    var_name = "HGNC_GENE_ID_MAPPING_PATH"
    val = os.environ.get(var_name)
    if not val:
        print(
            f"ERROR: {var_name} is not set. This script resolves the local HGNC gene-position "
            f"reference only via this env var -- it will not guess a path. Set {var_name} to the "
            f"directory containing raw/hgnc_custom_download.tsv and re-run.",
            file=sys.stderr,
        )
        sys.exit(1)
    p = Path(val) / "raw" / "hgnc_custom_download.tsv"
    if not p.is_file():
        print(f"ERROR: {p} not found.", file=sys.stderr)
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

    # Reference: QC-passing, immune-classified cells in PRIMARY_CRC/LIVER_METASTASIS only (not PBMC).
    reference_idx = [
        i for i in range(n_cells)
        if passes_qc[i] and cell_category[i] == "immune"
        and sample_map[cell_keys[i]]["specimen_type"] in ("PRIMARY_CRC", "LIVER_METASTASIS")
    ]
    print(f"Reference (tumor-site immune) cells: {len(reference_idx)}", file=sys.stderr)
    if len(reference_idx) < 200:
        print("ERROR: reference population too small (<200 cells) for a stable null distribution.", file=sys.stderr)
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
    threshold_idx = int(len(holdout_scores) * CNV_REFERENCE_PERCENTILE)
    threshold = holdout_scores[min(threshold_idx, len(holdout_scores) - 1)]
    print(f"CNV_HIGH threshold (holdout-reference {CNV_REFERENCE_PERCENTILE:.0%}ile): {threshold:.4f}", file=sys.stderr)

    epithelial_idx = [
        i for i in range(n_cells)
        if passes_qc[i] and cell_category[i] == "epithelial"
        and sample_map[cell_keys[i]]["specimen_type"] in ("PRIMARY_CRC", "LIVER_METASTASIS")
    ]
    print(f"Epithelial-proxy cells scored: {len(epithelial_idx)}", file=sys.stderr)

    # Diagnostic transparency: report the full score distribution, not just
    # counts above/below the pre-registered threshold, so the write-up can
    # honestly characterize how the population sits relative to it rather
    # than only reporting a binary pass/fail count.
    all_epi_scores = sorted(cnv_score(i) for i in epithelial_idx)

    def pct(p):
        idx = min(int(len(all_epi_scores) * p), len(all_epi_scores) - 1)
        return all_epi_scores[idx]

    print(
        f"Epithelial-proxy CNV score distribution: "
        f"min={all_epi_scores[0]:.3f} p10={pct(0.10):.3f} p25={pct(0.25):.3f} "
        f"median={pct(0.50):.3f} p75={pct(0.75):.3f} p90={pct(0.90):.3f} "
        f"p99={pct(0.99):.3f} max={all_epi_scores[-1]:.3f}  (threshold={threshold:.3f})",
        file=sys.stderr,
    )
    print(
        f"Reference (fit-half) CNV score distribution for comparison: "
        + ", ".join(f"{p:.0%}ile={sorted(cnv_score(i) for i in ref_fit_idx)[min(int(len(ref_fit_idx)*p), len(ref_fit_idx)-1)]:.3f}"
                     for p in (0.5, 0.9, 0.99)),
        file=sys.stderr,
    )

    per_sample = defaultdict(lambda: {"n_epithelial": 0, "n_cnv_high": 0, "n_cnv_high_target_pos": 0,
                                       "n_cnv_low": 0, "n_cnv_low_target_pos": 0})
    for i in epithelial_idx:
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

    out_path = REPO_ROOT / "modules" / "module_b_mcrc_target_prevalence" / "results" / f"tgt_{gene.lower()}_cnv_confirmed_prevalence.tsv"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out_rows[0].keys()), delimiter="\t")
        w.writeheader()
        for r in out_rows:
            w.writerow(r)
    print(f"\nWrote {len(out_rows)} sample rows to {out_path}")

    print(f"\nCNV-confirmed CEACAM5 prevalence per sample:")
    for r in out_rows:
        group = "TREATED" if r["patient_id"] in TREATED_PATIENTS else ("UNTREATED" if r["patient_id"] in UNTREATED_PATIENTS else "PBMC-n/a")
        print(f"  {r['sample_key']:14s} [{group:9s}] n_epi={r['n_epithelial_proxy']:5d} "
              f"CNV_HIGH={r['n_cnv_high']:5d} ({r[f'{gene}_pos_frac_cnv_high']})  "
              f"CNV_LOW={r['n_cnv_low']:5d} ({r[f'{gene}_pos_frac_cnv_low']})")


if __name__ == "__main__":
    main()
