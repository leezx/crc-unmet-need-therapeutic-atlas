#!/usr/bin/env python3
"""Module B: GSE178318 epithelial-proxy screen for one target's prevalence.

Corrected after web-ChatGPT round-1 review of PR #74, which independently
fetched GSE178318's own publication (Cell Discovery 2021, DOI
10.1038/s41421-021-00312-y -- the correct DOI; this repository's
DATA/registry/GSE178318/source_manifest.tsv previously recorded a
non-existent DOI, fixed alongside this script) and found the first version
of this script fell below that paper's own published standard:

  - No QC filtering was applied (all 140,281 raw barcodes used). The paper
    filters to <500 detected genes, per-batch (per-sample here) 3-SD
    outliers on log10(total UMI) and detected-gene count, and >15%
    mitochondrial UMI fraction. This script now applies the same four
    filters, using the paper's exact published thresholds.
  - The per-cell category score divided every category's raw marker-sum by
    the SAME total-UMI denominator, so the denominator cancelled out in the
    argmax comparison -- it was effectively comparing raw sums across
    marker panels of different sizes (a category with more marker genes had
    a structural advantage), with ties silently biased toward whichever
    category argmax saw first. Now: each category's score is its
    marker-average (sum / gene count in that category) as a fraction of
    total UMI, and the epithelial category itself follows the paper's own
    method (EPCAM alone, "EPCs were identified using the higher expression
    of EPCAM"), not a 5-gene panel that also includes hepatic-epithelium
    markers (KRT8/KRT18/CDH1 -- a real confound in liver-metastasis
    samples, per the review).
  - Still NOT malignancy calling -- the paper confirms EPCs are malignant
    via CNV inference (InferCNV-style, comparing transcriptome-inferred
    copy-number against a reference); that step is not reproduced here
    (would need a genomic gene-position reference and a chosen normal-cell
    reference population, a materially larger undertaking). This script
    stops at "EPCAM-high, QC-passing cell in a tumor-site specimen" --
    stated as an epithelial-proxy screen, not a confirmed malignant-cell
    result, in every output and in modules/module_b_mcrc_target_prevalence/
    README.md and reports/PROJECT_STATUS.md.
  - The treated (COL15/COL17/COL18) and treatment-naive (COL07/COL12/
    COL16) patients are now reported and keyed separately -- the prior
    version folded all 6 into one indication_id=mcrc_preop_chemotherapy_crlm
    dossier with only a notes-field caveat, which the review correctly
    called out as "notes cannot fix wrong cohort inclusion." Treated
    patients only are the primary result for that indication_id; the 3
    untreated matched pairs are separate context evidence under
    indication_id=mcrc_liver_metastasis (the anatomy-only parent node).

Reads the same fixed repo-relative gitignored raw path as before (this
repository's own DATA/registry/GSE178318/source_manifest.tsv, checksum-
verified) -- not an external path_env_var resource. Single streaming pass
over the 166.7M-entry matrix; no full matrix is materialized in memory.

Usage: python3 scripts/annotate_gse178318_cell_types.py --gene CEACAM5
"""
import argparse
import csv
import gzip
import hashlib
import math
import sys
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = (
    REPO_ROOT / "archive" / "phase2_fetal_state_track_v1" / "phase2"
    / "03_data" / "raw" / "GSE178318"
)

NON_EPITHELIAL_CATEGORIES = ("immune", "fibroblast", "endothelial")
TREATED_PATIENTS = {"COL15", "COL17", "COL18"}
UNTREATED_PATIENTS = {"COL07", "COL12", "COL16"}

# QC thresholds, taken verbatim from GSE178318's own publication (Cell
# Discovery 2021, DOI 10.1038/s41421-021-00312-y) Methods section.
MIN_DETECTED_GENES = 500
MAX_MITO_FRACTION = 0.15
BATCH_OUTLIER_SD = 3.0


def sha256(path):
    d = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            d.update(chunk)
    return d.hexdigest()


def resolve_files():
    manifest_path = REPO_ROOT / "DATA" / "registry" / "GSE178318" / "source_manifest.tsv"
    if not manifest_path.is_file():
        print(f"ERROR: {manifest_path} not found.", file=sys.stderr)
        sys.exit(1)
    with open(manifest_path, newline="") as f:
        manifest = {r["file_name"]: r for r in csv.DictReader(f, delimiter="\t")}
    files = {}
    for fname in ("GSE178318_barcodes.tsv.gz", "GSE178318_genes.tsv.gz", "GSE178318_matrix.mtx.gz"):
        path = RAW_DIR / fname
        if not path.is_file():
            print(f"ERROR: {path} not found.", file=sys.stderr)
            sys.exit(1)
        expected = manifest.get(fname, {}).get("checksum", "").replace("sha256:", "")
        if not expected:
            print(f"ERROR: no checksum recorded for {fname} in {manifest_path}.", file=sys.stderr)
            sys.exit(1)
        actual = sha256(path)
        if actual != expected:
            print(f"ERROR: checksum mismatch for {path}: manifest says {expected}, file is {actual}.", file=sys.stderr)
            sys.exit(1)
        files[fname] = path
    return files


def read_lines(path):
    with gzip.open(path, "rt") as f:
        return [line.rstrip("\n\r") for line in f]


def sample_key(barcode):
    parts = barcode.rsplit("_", 2)
    if len(parts) != 3:
        return "UNPARSEABLE"
    return f"{parts[1]}_{parts[2]}"


def load_sample_map(path):
    rows = {}
    material_map = {"PRIMARY_CRC": "CRC", "LIVER_METASTASIS": "LM", "PBMC": "PBMC"}
    with open(path, newline="") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            material = material_map.get(row["specimen_type"])
            if material:
                rows[f"{row['patient_id']}_{material}"] = row
    return rows


def load_marker_set(path):
    by_category = defaultdict(list)
    with open(path, newline="") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            by_category[row["category"]].append(row["gene"])
    return by_category


def classify_cell(total_umi, epcam_count, category_sums, category_gene_counts):
    """Score each category as (marker average) / total_umi, so panels of
    different sizes are comparable. epithelial uses EPCAM alone (the
    paper's own method), not a multi-gene panel. Returns the winning
    category, or 'Unassigned' if total_umi is 0 or all scores are 0."""
    if total_umi == 0:
        return "Unassigned"
    scores = {"epithelial": epcam_count / total_umi}
    for cat in NON_EPITHELIAL_CATEGORIES:
        n = category_gene_counts[cat]
        scores[cat] = (category_sums[cat] / n) / total_umi if n else 0.0
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "Unassigned"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gene", required=True)
    ap.add_argument("--marker-set", default=str(
        REPO_ROOT / "modules" / "module_b_mcrc_target_prevalence" / "analysis_contracts" / "cell_type_marker_set_v1.tsv"
    ))
    ap.add_argument("--out", default=None)
    ap.add_argument("--rna-no-max", type=float, default=0.05)
    ap.add_argument("--rna-high-min", type=float, default=0.50)
    args = ap.parse_args()
    gene = args.gene.strip()

    files = resolve_files()
    barcodes = read_lines(files["GSE178318_barcodes.tsv.gz"])
    genes_raw = read_lines(files["GSE178318_genes.tsv.gz"])
    gene_symbols = [g.split("\t")[-1] for g in genes_raw]

    sample_map_path = REPO_ROOT / "DATA" / "registry" / "GSE178318" / "sample_map.tsv"
    sample_map = load_sample_map(sample_map_path)
    cell_keys = [sample_key(b) for b in barcodes]
    if any(k == "UNPARSEABLE" for k in cell_keys):
        print("ERROR: at least one barcode is unparseable.", file=sys.stderr)
        sys.exit(1)
    unmapped = sorted({k for k in cell_keys if k not in sample_map})
    if unmapped:
        print(f"ERROR: unmapped sample keys: {unmapped}", file=sys.stderr)
        sys.exit(1)

    marker_set = load_marker_set(args.marker_set)
    symbol_to_row = {}
    for i, sym in enumerate(gene_symbols):
        symbol_to_row.setdefault(sym, i + 1)

    category_rows = {}
    for cat in NON_EPITHELIAL_CATEGORIES:
        missing = [g for g in marker_set[cat] if g not in symbol_to_row]
        if missing:
            print(f"ERROR: marker gene(s) not found: {missing}", file=sys.stderr)
            sys.exit(1)
        category_rows[cat] = {symbol_to_row[g] for g in marker_set[cat]}
    category_gene_counts = {cat: len(marker_set[cat]) for cat in NON_EPITHELIAL_CATEGORIES}

    if "EPCAM" not in symbol_to_row:
        print("ERROR: EPCAM not found in gene index.", file=sys.stderr)
        sys.exit(1)
    epcam_row = symbol_to_row["EPCAM"]

    mito_symbols = [s for s in gene_symbols if s.startswith("MT-")]
    mito_rows = {symbol_to_row[s] for s in mito_symbols if s in symbol_to_row}
    if len(mito_rows) < 10:
        print(f"WARNING: only {len(mito_rows)} MT- genes found in gene index; expected ~13.", file=sys.stderr)

    if gene not in symbol_to_row:
        print(f"ERROR: target gene '{gene}' not found in gene index.", file=sys.stderr)
        sys.exit(1)
    target_row = symbol_to_row[gene]

    n_cells = len(barcodes)
    total_counts = [0] * n_cells
    detected_genes = [0] * n_cells
    mito_counts = [0] * n_cells
    epcam_counts = [0] * n_cells
    target_counts = [0] * n_cells
    category_sums = {cat: [0] * n_cells for cat in NON_EPITHELIAL_CATEGORIES}

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
            entries += 1

    if header != (len(gene_symbols), n_cells, entries):
        print(f"ERROR: matrix dimension mismatch: header={header}, genes={len(gene_symbols)}, cells={n_cells}, entries={entries}", file=sys.stderr)
        sys.exit(1)

    # QC filter, per the paper's own thresholds. Batch = each of the 15
    # patient/specimen sample keys, matching how this dataset's own
    # sample_map.tsv already groups cells.
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
            if detected_genes[i] < MIN_DETECTED_GENES:
                continue
            if total_counts[i] == 0:
                continue
            mito_frac = mito_counts[i] / total_counts[i]
            if mito_frac > MAX_MITO_FRACTION:
                continue
            if sd_log_total > 0 and abs(log_total - mean_log_total) > BATCH_OUTLIER_SD * sd_log_total:
                continue
            if sd_genes > 0 and abs(detected_genes[i] - mean_genes) > BATCH_OUTLIER_SD * sd_genes:
                continue
            passes_qc[i] = True

    n_qc_pass = sum(passes_qc)
    print(f"QC: {n_qc_pass} of {n_cells} cells pass (paper reports 111,292 of 140,281 after its own QC pipeline; "
          f"batch definition and exact per-cell log/SD arithmetic may differ from the paper's, this is not "
          f"expected to match exactly).", file=sys.stderr)

    cell_category = [None] * n_cells
    for i in range(n_cells):
        if not passes_qc[i]:
            cell_category[i] = "QC_FAIL"
            continue
        cell_category[i] = classify_cell(
            total_counts[i], epcam_counts[i],
            {cat: category_sums[cat][i] for cat in NON_EPITHELIAL_CATEGORIES},
            category_gene_counts,
        )

    per_sample = defaultdict(lambda: {"n_cells": 0, "n_qc_pass": 0, "category_counts": defaultdict(int),
                                       "epithelial_target_pos": 0, "n_epithelial": 0})
    for i, key in enumerate(cell_keys):
        s = per_sample[key]
        s["n_cells"] += 1
        if passes_qc[i]:
            s["n_qc_pass"] += 1
            s["category_counts"][cell_category[i]] += 1
            if cell_category[i] == "epithelial":
                s["n_epithelial"] += 1
                if target_counts[i] > 0:
                    s["epithelial_target_pos"] += 1

    out_rows = []
    for key, s in sorted(per_sample.items()):
        info = sample_map[key]
        frac_target = (s["epithelial_target_pos"] / s["n_epithelial"]) if s["n_epithelial"] else None
        bucket = None
        if frac_target is not None:
            if frac_target < args.rna_no_max:
                bucket = "RNA_no"
            elif frac_target > args.rna_high_min:
                bucket = "RNA_high"
            else:
                bucket = "RNA_low"
        out_rows.append({
            "sample_key": key, "patient_id": info["patient_id"], "specimen_type": info["specimen_type"],
            "n_cells": s["n_cells"], "n_qc_pass": s["n_qc_pass"],
            "n_epithelial": s["n_epithelial"],
            "n_immune": s["category_counts"]["immune"],
            "n_fibroblast": s["category_counts"]["fibroblast"],
            "n_endothelial": s["category_counts"]["endothelial"],
            "n_unassigned": s["category_counts"]["Unassigned"],
            "epithelial_fraction_of_qc_pass": round(s["n_epithelial"] / s["n_qc_pass"], 4) if s["n_qc_pass"] else None,
            f"{gene}_positive_fraction_in_epithelial": round(frac_target, 4) if frac_target is not None else "NA",
            f"{gene}_bucket": bucket or "NA",
        })

    out_path = Path(args.out) if args.out else (
        REPO_ROOT / "modules" / "module_b_mcrc_target_prevalence" / "results"
        / f"tgt_{gene.lower()}_cell_type_prevalence.tsv"
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(out_rows[0].keys())
    with open(out_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t")
        w.writeheader()
        for r in out_rows:
            w.writerow(r)

    print(f"\nWrote {len(out_rows)} sample rows to {out_path}")
    print(f"\nPer-sample summary for {gene} (epithelial-proxy screen, QC-filtered, NOT malignancy-confirmed):")
    for r in out_rows:
        group = "TREATED" if r["patient_id"] in TREATED_PATIENTS else ("UNTREATED" if r["patient_id"] in UNTREATED_PATIENTS else "PBMC-n/a")
        print(f"  {r['sample_key']:14s} [{group:9s}] n_cells={r['n_cells']:6d} qc_pass={r['n_qc_pass']:6d} "
              f"epithelial={r['n_epithelial']:6d} ({r['epithelial_fraction_of_qc_pass']})  "
              f"{gene}+_frac_in_epi={r[f'{gene}_positive_fraction_in_epithelial']}  bucket={r[f'{gene}_bucket']}")

    print(f"\nPBMC validation check (should be ~all immune):")
    for r in out_rows:
        if r["specimen_type"] == "PBMC" and r["n_qc_pass"]:
            print(f"  {r['sample_key']:14s} qc_pass={r['n_qc_pass']:6d} immune={r['n_immune']:6d} ({r['n_immune']/r['n_qc_pass']:.1%})  epithelial={r['n_epithelial']} ({r['n_epithelial']/r['n_qc_pass']:.1%})")


if __name__ == "__main__":
    main()
