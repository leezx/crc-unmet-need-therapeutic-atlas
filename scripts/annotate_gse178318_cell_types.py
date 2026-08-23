#!/usr/bin/env python3
"""Module B: marker-gene-score cell-compartment split for GSE178318, plus one
target's per-compartment expression prevalence. Method and thresholds are
locked in modules/module_b_mcrc_target_prevalence/analysis_contracts/tgt_ceacam5.md
(written before this script ran) -- read that file before trusting this
script's output boundaries.

This is NOT malignancy calling. See the analysis contract's first section.

Reads the same fixed repo-relative gitignored raw path as the archived
qc_gse178318.py (this repository's own DATA/registry/GSE178318/source_manifest.tsv
records these files as downloaded 2026-08-11, checksum-verified) -- not an
external path_env_var resource, since it is this repository's own tracked
(if gitignored) local cache. Single streaming pass over the 166.7M-entry
matrix; no full matrix is materialized in memory.

Usage: python3 scripts/annotate_gse178318_cell_types.py --gene CEACAM5
       [--marker-set modules/module_b_mcrc_target_prevalence/analysis_contracts/cell_type_marker_set_v1.tsv]
       [--out modules/module_b_mcrc_target_prevalence/results/tgt_ceacam5_cell_type_prevalence.tsv]
"""
import argparse
import csv
import gzip
import hashlib
import sys
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = (
    REPO_ROOT / "archive" / "phase2_fetal_state_track_v1" / "phase2"
    / "03_data" / "raw" / "GSE178318"
)

CATEGORIES = ("epithelial", "immune", "fibroblast", "endothelial")


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
            print(
                f"ERROR: {path} not found. DATA/registry/GSE178318/source_manifest.tsv records "
                f"this file as downloaded 2026-08-11 to this repository's own gitignored Phase 2 "
                f"raw cache. If it has genuinely been removed, that is a real state change -- "
                f"update modules/module_b_mcrc_target_prevalence/data_lock/*.md accordingly rather "
                f"than proceeding.",
                file=sys.stderr,
            )
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gene", required=True)
    ap.add_argument("--marker-set", default=str(
        REPO_ROOT / "modules" / "module_b_mcrc_target_prevalence" / "analysis_contracts" / "cell_type_marker_set_v1.tsv"
    ))
    ap.add_argument("--out", default=None)
    ap.add_argument("--rna-no-max", type=float, default=0.05, help="fraction below this = RNA_no")
    ap.add_argument("--rna-high-min", type=float, default=0.50, help="fraction at/above this = RNA_high")
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
        symbol_to_row.setdefault(sym, i + 1)  # Matrix Market rows are 1-indexed

    category_rows = {}
    for cat in CATEGORIES:
        missing = [g for g in marker_set[cat] if g not in symbol_to_row]
        if missing:
            print(f"ERROR: marker gene(s) not found in gene index: {missing}", file=sys.stderr)
            sys.exit(1)
        category_rows[cat] = {symbol_to_row[g] for g in marker_set[cat]}

    if gene not in symbol_to_row:
        print(f"ERROR: target gene '{gene}' not found in GSE178318 gene index.", file=sys.stderr)
        sys.exit(1)
    target_row = symbol_to_row[gene]

    n_cells = len(barcodes)
    total_counts = [0] * n_cells
    category_sums = {cat: [0] * n_cells for cat in CATEGORIES}
    target_counts = [0] * n_cells

    print(f"Streaming matrix ({files['GSE178318_matrix.mtx.gz']})...", file=sys.stderr)
    header = None
    entries = 0
    row_to_cats = {}
    for cat, rows in category_rows.items():
        for r in rows:
            row_to_cats.setdefault(r, []).append(cat)

    with gzip.open(files["GSE178318_matrix.mtx.gz"], "rt") as f:
        for raw_line in f:
            if raw_line.startswith("%"):
                continue
            if header is None:
                dims = raw_line.split()
                header = tuple(map(int, dims))
                continue
            row_s, col_s, val_s = raw_line.split()
            row = int(row_s)
            cell = int(col_s) - 1
            count = int(float(val_s))
            total_counts[cell] += count
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

    # Per-cell category assignment
    cell_category = [None] * n_cells
    for i in range(n_cells):
        tc = total_counts[i]
        if tc == 0:
            cell_category[i] = "Unassigned"
            continue
        scores = {cat: category_sums[cat][i] / tc for cat in CATEGORIES}
        best = max(scores, key=scores.get)
        cell_category[i] = best if scores[best] > 0 else "Unassigned"

    # Per-sample summary
    per_sample = defaultdict(lambda: {"n_cells": 0, "category_counts": defaultdict(int),
                                       "epithelial_target_pos": 0, "n_epithelial": 0})
    for i, key in enumerate(cell_keys):
        s = per_sample[key]
        s["n_cells"] += 1
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
            elif frac_target >= args.rna_high_min:
                bucket = "RNA_high"
            else:
                bucket = "RNA_low"
        out_rows.append({
            "sample_key": key, "patient_id": info["patient_id"], "specimen_type": info["specimen_type"],
            "n_cells": s["n_cells"],
            "n_epithelial": s["n_epithelial"],
            "n_immune": s["category_counts"]["immune"],
            "n_fibroblast": s["category_counts"]["fibroblast"],
            "n_endothelial": s["category_counts"]["endothelial"],
            "n_unassigned": s["category_counts"]["Unassigned"],
            "epithelial_fraction": round(s["n_epithelial"] / s["n_cells"], 4) if s["n_cells"] else None,
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
    print(f"\nPer-sample summary for {gene}:")
    for r in out_rows:
        print(f"  {r['sample_key']:14s} n_cells={r['n_cells']:6d} epithelial={r['n_epithelial']:6d} "
              f"({r['epithelial_fraction']:.1%})  {gene}+_frac_in_epi={r[f'{gene}_positive_fraction_in_epithelial']}  "
              f"bucket={r[f'{gene}_bucket']}")

    # PBMC validation check
    print(f"\nPBMC validation check (should be ~all immune):")
    for r in out_rows:
        if r["specimen_type"] == "PBMC":
            print(f"  {r['sample_key']:14s} n_cells={r['n_cells']:6d} immune={r['n_immune']:6d} ({r['n_immune']/r['n_cells']:.1%})  epithelial={r['n_epithelial']} ({r['n_epithelial']/r['n_cells']:.1%})")


if __name__ == "__main__":
    main()
