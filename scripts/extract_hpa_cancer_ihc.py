#!/usr/bin/env python3
"""Module D: HPA Pathology Atlas tumor-tissue IHC for one target, colorectal
cancer specifically (and, for context, all other cancer types HPA scores).

Reads `cancer_data.tsv.zip` (the classic HPA "Pathology Atlas" product:
Gene, Gene name, Cancer, High, Medium, Low, Not detected -- patient
counts by IHC staining level, one row per gene x cancer type), a small
(1.72 MB), already-processed, gene-symbol-indexed file. Distinct from
DATA/registry/HPA_normal_tissue (normal-tissue IHC, Module E only) --
this is HPA_CRC_cancer_tissue, tumor-tissue IHC, Module D.

This is a cancer-cell-focused categorical IHC annotation, not a bulk
whole-tumor-section score -- HPA's own cancer-methods page
(https://www.proteinatlas.org/humanproteome/cancer/method, independently
fetched and confirmed 2026-08-25, PR #82 round 1 review) states:
"All images were then analyzed by pathologists and annotated with
respect to staining intensity and fraction of positive cancer cells for
all approved antibodies. The result of immunohistochemistry-based
protein expression was then summarized as high, medium, low or not
detected." Still NOT membrane-specific, NOT quantitative antigen
density, and NOT a calibrated surface assay -- typical HPA Pathology
Atlas cohorts are small (n~10-12 patients per cancer type) -- per this
repository's own Module D contract, this does NOT establish
surface-density on its own. evidence_directness stays
UNCALIBRATED_PROXY, measurement_layer=IHC.

Usage: python3 scripts/extract_hpa_cancer_ihc.py --gene CEACAM5
"""
import argparse
import csv
import hashlib
import io
import sys
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = (
    REPO_ROOT / "modules" / "module_d_protein_and_endpoint"
    / "data_lock" / "raw" / "HPA_CRC_cancer_tissue"
)
ZIP_FILE = "cancer_data.tsv.zip"
INNER_FILE = "cancer_data.tsv"
TARGET_CANCER = "colorectal cancer"


def sha256(path):
    d = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            d.update(chunk)
    return d.hexdigest()


def resolve_file():
    inventory_path = REPO_ROOT / "DATA" / "registry" / "HPA_CRC_cancer_tissue" / "file_inventory.tsv"
    if not inventory_path.is_file():
        print(f"ERROR: {inventory_path} not found.", file=sys.stderr)
        sys.exit(1)
    with open(inventory_path, newline="") as f:
        inventory = {r["file_name"]: r for r in csv.DictReader(f, delimiter="\t")}
    path = RAW_DIR / ZIP_FILE
    if not path.is_file():
        print(f"ERROR: {path} not found.", file=sys.stderr)
        sys.exit(1)
    expected = inventory.get(ZIP_FILE, {}).get("checksum", "").replace("sha256:", "")
    if not expected:
        print(f"ERROR: no checksum recorded for {ZIP_FILE} in {inventory_path}.", file=sys.stderr)
        sys.exit(1)
    actual = sha256(path)
    if actual != expected:
        print(f"ERROR: checksum mismatch for {path}: inventory says {expected}, file is {actual}.", file=sys.stderr)
        sys.exit(1)
    return path


def load_rows(zip_path, gene_symbol):
    rows = []
    with zipfile.ZipFile(zip_path) as z:
        with z.open(INNER_FILE) as f:
            tr = io.TextIOWrapper(f, encoding="utf-8")
            reader = csv.DictReader(tr, delimiter="\t")
            for row in reader:
                if row["Gene name"] == gene_symbol:
                    rows.append(row)
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gene", required=True)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    gene = args.gene.strip()

    path = resolve_file()
    rows = load_rows(path, gene)
    if not rows:
        print(f"ERROR: gene symbol '{gene}' not found in {INNER_FILE}.", file=sys.stderr)
        sys.exit(1)

    out_path = Path(args.out) if args.out else (
        REPO_ROOT / "modules" / "module_d_protein_and_endpoint" / "results"
        / f"tgt_{gene.lower()}_hpa_cancer_ihc.tsv"
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["Gene", "Gene name", "Cancer", "High", "Medium", "Low", "Not detected"]
    with open(out_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t")
        w.writeheader()
        for r in sorted(rows, key=lambda r: r["Cancer"]):
            w.writerow({k: r[k] for k in fieldnames})

    print(f"\nWrote {len(rows)} cancer-type rows to {out_path}")

    target_row = next((r for r in rows if r["Cancer"] == TARGET_CANCER), None)
    if target_row is None:
        print(f"\nWARNING: '{TARGET_CANCER}' not among the {len(rows)} cancer types scored for {gene}.",
              file=sys.stderr)
    else:
        high, med, low, none_ = (int(target_row[k]) for k in ("High", "Medium", "Low", "Not detected"))
        n = high + med + low + none_
        print(f"\n{gene} in {TARGET_CANCER} (n={n} patients): High={high}, Medium={med}, "
              f"Low={low}, Not detected={none_}.")

    print(f"\nAll {len(rows)} cancer types scored for {gene}:")
    for r in sorted(rows, key=lambda r: r["Cancer"]):
        print(f"  {r['Cancer']:22s} High={r['High']:>3s} Medium={r['Medium']:>3s} "
              f"Low={r['Low']:>3s} NotDetected={r['Not detected']:>3s}")


if __name__ == "__main__":
    main()
