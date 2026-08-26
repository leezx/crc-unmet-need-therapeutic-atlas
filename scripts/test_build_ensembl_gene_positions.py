#!/usr/bin/env python3
"""Regression tests for the committed output of build_ensembl_gene_positions.py
-- checks the actual committed DATA/reference/ table, not a synthetic
fixture, since this is a one-time-built, checked-in reference table (same
spirit as validate_registry.py checking committed registry files).

Usage: python3 scripts/test_build_ensembl_gene_positions.py
"""
import csv
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
TABLE_PATH = REPO_ROOT / "DATA" / "reference" / "ensembl_gene_positions_grch38_release110.tsv"

failures = []


def check(label, cond):
    if not cond:
        failures.append(label)
        print(f"FAIL: {label}")
    else:
        print(f"ok: {label}")


check(f"{TABLE_PATH.name} exists", TABLE_PATH.is_file())
if not TABLE_PATH.is_file():
    print(f"\n{len(failures)} test(s) FAILED: {failures}")
    sys.exit(1)

with open(TABLE_PATH, newline="") as f:
    rows = list(csv.DictReader(f, delimiter="\t"))

check("header is exactly [ensembl_gene_id, chromosome, start, end]",
      list(rows[0].keys()) == ["ensembl_gene_id", "chromosome", "start", "end"] if rows else False)
check("has a substantial number of rows (>50,000, standard-contig genes only)", len(rows) > 50000)

ids = [r["ensembl_gene_id"] for r in rows]
check("ensembl_gene_id has no duplicates", len(ids) == len(set(ids)))

STANDARD_CHROMS = {str(i) for i in range(1, 23)} | {"X", "Y", "MT"}
bad_chroms = {r["chromosome"] for r in rows} - STANDARD_CHROMS
check("every row's chromosome is one of 1-22/X/Y/MT (no scaffolds/patches)", not bad_chroms)

bad_coords = [r for r in rows if not (r["start"].isdigit() and r["end"].isdigit() and int(r["start"]) <= int(r["end"]))]
check("every row has start <= end, both numeric", not bad_coords)

# --- the five A_CLINICAL targets resolve to their well-known chromosome arms ---
by_id = {r["ensembl_gene_id"]: r for r in rows}
EXPECTED_CHROM = {
    "ENSG00000105388": "19",  # CEACAM5
    "ENSG00000141736": "17",  # ERBB2
    "ENSG00000117525": "1",   # F3
    "ENSG00000143217": "1",   # NECTIN4 (GSE178318's own ID, deposited under the prior symbol PVRL4)
    "ENSG00000184292": "1",   # TACSTD2
}
for ensg, expected_chrom in EXPECTED_CHROM.items():
    row = by_id.get(ensg)
    check(f"{ensg} resolves to chromosome {expected_chrom}", row is not None and row["chromosome"] == expected_chrom)

if failures:
    print(f"\n{len(failures)} test(s) FAILED: {failures}")
    sys.exit(1)
print("\nAll ensembl_gene_positions table regression tests passed.")
