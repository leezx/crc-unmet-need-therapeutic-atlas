#!/usr/bin/env python3
"""Module D: PXD055821 tumor-tissue protein abundance for one target.

PXD055821 (152 CRLM samples, 3 proteomic phenotypes, Mol Cell Proteomics
2025, DOI 10.1016/J.MCPRO.2025.101026) is a Proteome Discoverer/DIA-NN
mixed-search project. Most of its raw data is either multi-GB .raw files
or multi-GB .pdResult/.msf Proteome Discoverer result files -- neither
has a search engine available in this environment and neither is
reproduced or reprocessed here.

One DIA-NN output file from the project's "Sydney DIA" sub-cohort is a
small (3.48 MB), already-processed, gene-symbol-indexed protein
abundance matrix:
`220920_PN_CRC_LM_all_63_LM_DIANN.gg_matrix.tsv`. Its filename says
"all_63_LM" but the matrix itself has exactly 60 sample columns, not 63
-- a real filename/content discrepancy, recorded honestly rather than
"corrected" to match the name. This script reads that file only; it
does not touch the raw .raw/.pdResult/.msf files, which remain
unprocessed and are not claimed to contribute to this evidence.

Sample columns are the full Windows file paths DIA-NN recorded for each
run (e.g. "H:\\Paula\\CRC_LM\\...\\220624_CRCLM_PN_S24.mzML") -- these
are not resolved to patient IDs here; this is an aggregate,
across-samples read (n detected / median / range), not a per-patient
breakdown, unlike Module B's screens.

This is whole-tissue (not malignant-cell-specific) mass-spec protein
abundance -- per this repository's own Module D contract
(modules/module_d_protein_and_endpoint/README.md), it does NOT
establish malignant-cell-specific membrane/surface density on its own.
evidence_directness stays UNCALIBRATED_PROXY.

Usage: python3 scripts/extract_pxd055821_protein_abundance.py --gene CEACAM5
"""
import argparse
import csv
import hashlib
import statistics
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = (
    REPO_ROOT / "modules" / "module_d_protein_and_endpoint"
    / "data_lock" / "raw" / "PXD055821"
)
MATRIX_FILE = "220920_PN_CRC_LM_all_63_LM_DIANN.gg_matrix.tsv"


def sha256(path):
    d = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            d.update(chunk)
    return d.hexdigest()


def summarize_detection(values):
    """Blank/whitespace-only strings are missing values (DIA-NN's own
    convention in this matrix); everything else parses as a float. Returns
    (n_detected, n_total, fraction_detected, (median, min, max) or None)."""
    detected = [float(v) for v in values if v.strip()]
    n_detected = len(detected)
    n_total = len(values)
    frac = n_detected / n_total if n_total else None
    stats = (statistics.median(detected), min(detected), max(detected)) if detected else None
    return n_detected, n_total, frac, stats


def resolve_file():
    inventory_path = REPO_ROOT / "DATA" / "registry" / "PXD055821" / "file_inventory.tsv"
    if not inventory_path.is_file():
        print(f"ERROR: {inventory_path} not found.", file=sys.stderr)
        sys.exit(1)
    with open(inventory_path, newline="") as f:
        inventory = {r["file_name"]: r for r in csv.DictReader(f, delimiter="\t")}
    path = RAW_DIR / MATRIX_FILE
    if not path.is_file():
        print(f"ERROR: {path} not found.", file=sys.stderr)
        sys.exit(1)
    expected = inventory.get(MATRIX_FILE, {}).get("checksum", "").replace("sha256:", "")
    if not expected:
        print(f"ERROR: no checksum recorded for {MATRIX_FILE} in {inventory_path}.", file=sys.stderr)
        sys.exit(1)
    actual = sha256(path)
    if actual != expected:
        print(f"ERROR: checksum mismatch for {path}: inventory says {expected}, file is {actual}.", file=sys.stderr)
        sys.exit(1)
    return path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gene", required=True)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    gene = args.gene.strip()

    path = resolve_file()
    with open(path, newline="") as f:
        reader = csv.reader(f, delimiter="\t")
        header = next(reader)
        n_samples = len(header) - 1
        target_row = None
        n_rows = 0
        for row in reader:
            n_rows += 1
            if row[0] == gene:
                target_row = row
    print(f"Matrix: {n_rows} genes x {n_samples} sample columns.", file=sys.stderr)

    if target_row is None:
        print(f"ERROR: gene '{gene}' not found in {path.name} (checked exact-match on column 1, "
              f"{n_rows} gene rows scanned).", file=sys.stderr)
        sys.exit(1)

    values = target_row[1:]
    n_detected, _n_total, frac_detected, stats = summarize_detection(values)

    out_rows = []
    for sample_path, v in zip(header[1:], values):
        out_rows.append({"sample_path": sample_path, "value": v if v.strip() else "NA"})

    out_path = Path(args.out) if args.out else (
        REPO_ROOT / "modules" / "module_d_protein_and_endpoint" / "results"
        / f"tgt_{gene.lower()}_pxd055821_protein_abundance.tsv"
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["sample_path", "value"], delimiter="\t")
        w.writeheader()
        for r in out_rows:
            w.writerow(r)

    print(f"\nWrote {len(out_rows)} sample rows to {out_path}")
    if stats:
        median, lo, hi = stats
        print(f"\n{gene} protein abundance (DIA-NN gene-group intensity, arbitrary units) across "
              f"{n_samples} samples: detected in {n_detected}/{n_samples} ({frac_detected:.1%}); "
              f"median={median:.4g}, min={lo:.4g}, max={hi:.4g}.")
    else:
        print(f"\n{gene}: detected in 0/{n_samples} samples.")


if __name__ == "__main__":
    main()
