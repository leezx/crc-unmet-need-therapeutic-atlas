#!/usr/bin/env python3
"""Regression tests for compare_pxd055821_pg_vs_gg_matrix.py.

validate_target() is tested directly (pure function, no file I/O) --
including that the two ambiguity cases (shared Genes field, multi-
accession Protein.Group/Protein.Ids) are actually flagged as FAILURES,
not merely parsed without crashing (round 1 review of PR #87 caught an
earlier version of this test file that only checked the parser could
read a shared-gene fixture, never that the main validation logic would
reject it). load_pg_rows()/load_gg_rows() are tested against small
synthetic fixture files, not the real PXD055821 matrices.

Usage: python3 scripts/test_compare_pxd055821_pg_vs_gg_matrix.py
"""
import csv
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from compare_pxd055821_pg_vs_gg_matrix import load_pg_rows, load_gg_rows, validate_target

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


# ============================================================
# validate_target() -- the actual pass/fail decision logic
# ============================================================

# --- clean case: exactly one row, unshared gene, single accession, matching values ---
clean_match = (["ERBB2"], ["P04626"], ["P04626"], ["5", "8"])
ok, detail = validate_target("ERBB2", [clean_match], ["5", "8"])
check("clean single-accession, matching-values case: OK", ok and detail == "P04626")

# --- gg_matrix missing the gene entirely ---
ok, detail = validate_target("ERBB2", [clean_match], None)
check("gene missing from gg_matrix: FAILS, not silently skipped", not ok)

# --- zero matching pg rows ---
ok, detail = validate_target("ERBB2", [], ["5", "8"])
check("zero matching pg rows: FAILS (not silently treated as OK/0)", not ok)

# --- two matching pg rows (ambiguous row count) ---
ok, detail = validate_target("ERBB2", [clean_match, clean_match], ["5", "8"])
check("two matching pg rows: FAILS, not silently passed", not ok)

# --- shared Genes field: this is the exact scenario round 1 review of PR #87
# caught the OLD validation logic silently passing (Protein.Group=P00000;P00001,
# Genes=ERBB2;OTHER_GENE would still show len(groups)==1 and matching values). ---
shared_gene_match = (["ERBB2", "OTHER_GENE"], ["P00000", "P00001"], ["P00000", "P00001"], ["5", "8"])
ok, detail = validate_target("ERBB2", [shared_gene_match], ["5", "8"])
check("Genes field shared with another gene: validate_target() FAILS "
      "(not just readable by the parser -- this is the actual bug round 1 caught)",
      not ok)
check("failure reason names the sharing", "shared" in detail.lower())

# --- multi-accession Protein.Group, but Genes field is NOT shared ---
multi_pg_match = (["ERBB2"], ["P04626", "P04626-2"], ["P04626"], ["5", "8"])
ok, detail = validate_target("ERBB2", [multi_pg_match], ["5", "8"])
check("multi-accession Protein.Group (even with an unshared Genes field): FAILS",
      not ok)

# --- multi-accession Protein.Ids, single-accession Protein.Group ---
multi_pids_match = (["ERBB2"], ["P04626"], ["P04626", "P04626-2"], ["5", "8"])
ok, detail = validate_target("ERBB2", [multi_pids_match], ["5", "8"])
check("multi-accession Protein.Ids: FAILS", not ok)

# --- values differ from gg_matrix ---
ok, detail = validate_target("ERBB2", [clean_match], ["5", "9"])
check("value mismatch vs gg_matrix: FAILS", not ok)
check("failure reason names the mismatch", "differ" in detail.lower())

# ============================================================
# load_pg_rows() / load_gg_rows() -- parsing, kept faithful to raw fields
# ============================================================

pg_fixture = write_tsv([
    ["Protein.Group", "Protein.Ids", "Protein.Names", "Genes", "First.Protein.Description", "col1", "col2"],
    ["P06731", "P06731", "CEA5_HUMAN", "CEACAM5", "desc", "10", "20"],
    ["P00000;P00001", "P00000;P00001", "X_HUMAN", "ERBB2;OTHER_GENE", "desc", "5", "8"],
])
pg_header, pg_rows = load_pg_rows(pg_fixture, ["CEACAM5", "ERBB2", "F3"])
pg_fixture.unlink()

check("specimen header excludes the 5 metadata columns", pg_header == ["col1", "col2"])
check("CEACAM5 parses to exactly one match", len(pg_rows["CEACAM5"]) == 1)
check("CEACAM5's full genes_list is [CEACAM5], not discarded", pg_rows["CEACAM5"][0][0] == ["CEACAM5"])
check("F3 (absent from fixture): zero matches, not a KeyError", pg_rows["F3"] == [])
check("the shared-gene row's full genes_list [ERBB2, OTHER_GENE] is preserved for ERBB2 "
      "(not collapsed to just [ERBB2] -- this is what lets validate_target() catch it)",
      pg_rows["ERBB2"][0][0] == ["ERBB2", "OTHER_GENE"])

gg_fixture = write_tsv([
    ["Genes", "col1", "col2"],
    ["CEACAM5", "10", "20"],
])
gg_header, gg_rows = load_gg_rows(gg_fixture, ["CEACAM5", "ERBB2"])
gg_fixture.unlink()
check("load_gg_rows() specimen header excludes only the gene-id column", gg_header == ["col1", "col2"])
check("load_gg_rows() finds the present gene", gg_rows["CEACAM5"] == ["10", "20"])
check("load_gg_rows() omits the absent gene rather than inserting a placeholder",
      "ERBB2" not in gg_rows)

if failures:
    print(f"\n{len(failures)} test(s) FAILED: {failures}")
    sys.exit(1)
print("\nAll validate_target / load_pg_rows / load_gg_rows regression tests passed.")
