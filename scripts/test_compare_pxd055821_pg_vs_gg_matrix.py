#!/usr/bin/env python3
"""Regression tests for compare_pxd055821_pg_vs_gg_matrix.py's
load_pg_rows() -- tested against small synthetic fixture files, not the
real PXD055821 matrices.

Usage: python3 scripts/test_compare_pxd055821_pg_vs_gg_matrix.py
"""
import csv
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from compare_pxd055821_pg_vs_gg_matrix import load_pg_rows, load_gg_rows

failures = []


def check(label, cond):
    if not cond:
        failures.append(label)
        print(f"FAIL: {label}")
    else:
        print(f"ok: {label}")


def write_tsv(rows):
    f = tempfile.NamedTemporaryFile(mode="w", suffix=".tsv", delete=False, newline="")
    csv.writer(f, delimiter="\t").writerows(rows)
    f.close()
    return Path(f.name)


# --- unambiguous case: each target gene has exactly one protein group ---
pg_fixture = write_tsv([
    ["Protein.Group", "Protein.Ids", "Protein.Names", "Genes", "First.Protein.Description", "col1", "col2"],
    ["P06731", "P06731", "CEA5_HUMAN", "CEACAM5", "desc", "10", "20"],
    ["P04626", "P04626", "ERBB2_HUMAN", "ERBB2", "desc", "5", "8"],
])
pg_rows = load_pg_rows(pg_fixture, ["CEACAM5", "ERBB2", "F3"])
pg_fixture.unlink()

check("CEACAM5 has exactly one protein group", len(pg_rows["CEACAM5"]) == 1)
check("CEACAM5's protein group id is P06731", pg_rows["CEACAM5"][0][0] == "P06731")
check("CEACAM5's values are the two specimen columns", pg_rows["CEACAM5"][0][2] == ["10", "20"])
check("F3 (absent from fixture) has zero protein groups, not a KeyError", pg_rows["F3"] == [])

# --- ambiguous case: a gene shared across two protein groups (isoform/proteoform split) ---
pg_ambiguous = write_tsv([
    ["Protein.Group", "Protein.Ids", "Protein.Names", "Genes", "First.Protein.Description", "col1"],
    ["P04626", "P04626", "ERBB2_HUMAN", "ERBB2", "desc", "5"],
    ["P04626-2", "P04626-2", "ERBB2_HUMAN_ISO2", "ERBB2", "desc", "3"],
])
pg_rows2 = load_pg_rows(pg_ambiguous, ["ERBB2"])
pg_ambiguous.unlink()
check("a gene split across two protein groups is NOT silently collapsed to one",
      len(pg_rows2["ERBB2"]) == 2)

# --- a protein group shared across two genes (protein-inference ambiguity) ---
pg_shared = write_tsv([
    ["Protein.Group", "Protein.Ids", "Protein.Names", "Genes", "First.Protein.Description", "col1"],
    ["P00000;P00001", "P00000;P00001", "X_HUMAN", "GENE_A;GENE_B", "desc", "7"],
])
pg_rows3 = load_pg_rows(pg_shared, ["GENE_A", "GENE_B"])
pg_shared.unlink()
check("a protein group shared across two genes is attributed to both, not dropped",
      len(pg_rows3["GENE_A"]) == 1 and len(pg_rows3["GENE_B"]) == 1)
check("both genes see the same shared protein group's values",
      pg_rows3["GENE_A"][0][2] == pg_rows3["GENE_B"][0][2] == ["7"])

# --- load_gg_rows() sanity ---
gg_fixture = write_tsv([
    ["Genes", "col1", "col2"],
    ["CEACAM5", "10", "20"],
])
gg_rows = load_gg_rows(gg_fixture, ["CEACAM5", "ERBB2"])
gg_fixture.unlink()
check("load_gg_rows() finds the present gene", gg_rows["CEACAM5"] == ["10", "20"])
check("load_gg_rows() omits the absent gene rather than inserting a placeholder",
      "ERBB2" not in gg_rows)

if failures:
    print(f"\n{len(failures)} test(s) FAILED: {failures}")
    sys.exit(1)
print("\nAll load_pg_rows / load_gg_rows regression tests passed.")
