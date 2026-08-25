#!/usr/bin/env python3
"""Regression tests for analyze_pxd055821_abundance_percentile.py's
percentile_rank() and load_all_gene_stats() -- percentile_rank() is a
pure function; load_all_gene_stats() is tested against a small synthetic
fixture matrix (not the real PXD055821 file, which isn't needed here).

Usage: python3 scripts/test_analyze_pxd055821_abundance_percentile.py
"""
import csv
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from analyze_pxd055821_abundance_percentile import percentile_rank, load_all_gene_stats, A_CLINICAL_TARGETS

failures = []


def check(label, cond):
    if not cond:
        failures.append(label)
        print(f"FAIL: {label}")
    else:
        print(f"ok: {label}")


# --- basic rank behavior ---
sorted_vals = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
check("value below all: percentile == 0", percentile_rank(sorted_vals, 0) == 0.0)
check("value above all: percentile == 100", percentile_rank(sorted_vals, 11) == 100.0)
check("value at first element: percentile == 0 (0 elements strictly less)",
      percentile_rank(sorted_vals, 1) == 0.0)
check("value at last element: percentile == 90 (9/10 elements strictly less)",
      percentile_rank(sorted_vals, 10) == 90.0)
check("value at median-ish position: percentile == 50",
      percentile_rank(sorted_vals, 6) == 50.0)

# --- ties: bisect_left counts strictly-less, matching "N of M genes rank below this one" ---
sorted_with_ties = [1, 2, 2, 2, 3, 4]
check("value tied with a run: percentile counts only strictly-less elements",
      percentile_rank(sorted_with_ties, 2) == (1 / 6 * 100))

# --- empty list: no crash, returns None rather than a division-by-zero ---
check("empty sorted list: returns None, not a crash", percentile_rank([], 5) is None)

# --- single-element list ---
check("single-element list, value equals it: percentile == 0",
      percentile_rank([5], 5) == 0.0)
check("single-element list, value above it: percentile == 100",
      percentile_rank([5], 6) == 100.0)

# --- load_all_gene_stats() against a small synthetic fixture matrix ---
# Header + 4 gene rows, 3 specimen columns. GENE_A: all nonzero. GENE_B: one
# blank cell (missing, not detected). GENE_C: a literal 0 (not detected,
# same "0 != detected" rule as extract_pxd055821_protein_abundance.py's
# summarize_detection()). GENE_D: all blank (never detected).
fixture_rows = [
    ["Genes", "col1", "col2", "col3"],
    ["GENE_A", "10", "20", "30"],
    ["GENE_B", "5", "", "15"],
    ["GENE_C", "0", "8", "0"],
    ["GENE_D", "", "", ""],
]
with tempfile.NamedTemporaryFile(mode="w", suffix=".tsv", delete=False, newline="") as f:
    csv.writer(f, delimiter="\t").writerows(fixture_rows)
    fixture_path = Path(f.name)

stats = load_all_gene_stats(fixture_path)
fixture_path.unlink()

check("fixture: all 4 genes present", set(stats.keys()) == {"GENE_A", "GENE_B", "GENE_C", "GENE_D"})
check("GENE_A: 3/3 detected, median == 20", stats["GENE_A"] == (3, 3, 1.0, 20.0))
check("GENE_B: n_total counts all columns including the blank one "
      "(2/3 detected, matching summarize_detection()'s own n_total=len(values) convention)",
      stats["GENE_B"] == (2, 3, 2 / 3, 10.0))
check("GENE_C: literal 0 values excluded from detected count (1/3 detected, not 3/3)",
      stats["GENE_C"] == (1, 3, 1 / 3, 8.0))
check("GENE_D: 0 detected, median is None (not a division-by-zero)",
      stats["GENE_D"][0] == 0 and stats["GENE_D"][3] is None)

# --- A_CLINICAL_TARGETS sanity: the five gene symbols main() looks up ---
check("A_CLINICAL_TARGETS has exactly the five repository targets",
      set(A_CLINICAL_TARGETS) == {"CEACAM5", "ERBB2", "F3", "NECTIN4", "TACSTD2"})

if failures:
    print(f"\n{len(failures)} test(s) FAILED: {failures}")
    sys.exit(1)
print("\nAll percentile_rank / load_all_gene_stats regression tests passed.")
