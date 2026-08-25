#!/usr/bin/env python3
"""Regression tests for analyze_pxd055821_abundance_percentile.py's
percentile_rank() -- pure function, no real matrix file needed.

Usage: python3 scripts/test_analyze_pxd055821_abundance_percentile.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from analyze_pxd055821_abundance_percentile import percentile_rank

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

if failures:
    print(f"\n{len(failures)} test(s) FAILED: {failures}")
    sys.exit(1)
print("\nAll percentile_rank regression tests passed.")
