#!/usr/bin/env python3
"""Regression tests for extract_pdo_erbb2_mihc.py's summarize_detection()
-- the detection/summary-statistics logic. No real Mendeley Data xlsx
needed -- pure unit tests on synthetic value rows (openpyxl returns
floats/None from a real workbook, so these tests use float/None inputs,
not strings, matching actual usage).

Usage: python3 scripts/test_extract_pdo_erbb2_mihc.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from extract_pdo_erbb2_mihc import summarize_detection, PANEL_MARKERS, EXCLUDED_MARKERS

failures = []


def check(label, cond):
    if not cond:
        failures.append(label)
        print(f"FAIL: {label}")
    else:
        print(f"ok: {label}")


# --- fully detected row (real openpyxl values: floats) ---
n_det, n_tot, frac, stats = summarize_detection([0.1, 0.2, 0.3])
check("fully-detected row: n_detected == 3", n_det == 3)
check("fully-detected row: n_total == 3", n_tot == 3)
check("fully-detected row: fraction == 1.0", frac == 1.0)
check("fully-detected row: median == 0.2", abs(stats[0] - 0.2) < 1e-9)
check("fully-detected row: min/max == 0.1/0.3", stats[1] == 0.1 and stats[2] == 0.3)

# --- partially detected row (None = missing cell, matching openpyxl's own convention) ---
n_det, n_tot, frac, stats = summarize_detection([0.1, None, 0.4])
check("partially-detected row: n_detected == 2 (None excluded)", n_det == 2)
check("partially-detected row: n_total == 3", n_tot == 3)
check("partially-detected row: median of [0.1, 0.4] == 0.25", abs(stats[0] - 0.25) < 1e-9)

# --- fully undetected row (all missing) ---
n_det, n_tot, frac, stats = summarize_detection([None, None])
check("fully-undetected row: n_detected == 0", n_det == 0)
check("fully-undetected row: fraction == 0.0", frac == 0.0)
check("fully-undetected row: no stats computed (empty detected list, not a division-by-zero)", stats is None)

# --- empty row list (edge case: no rows at all for a marker) ---
n_det, n_tot, frac, stats = summarize_detection([])
check("empty row list: fraction is None, not a division-by-zero crash", frac is None)

# --- a literal 0 value is NOT detected -- matches this script's own claim text
# ("detected (nonzero)"), not just "non-missing". ---
n_det, n_tot, frac, stats = summarize_detection([0.1, 0, 0.2])
check("a literal 0 value is excluded from detected (not just None)", n_det == 2)
check("0 does not appear in the computed stats (median of [0.1, 0.2] == 0.15, not affected by 0)",
      abs(stats[0] - 0.15) < 1e-9)
n_det, n_tot, frac, stats = summarize_detection([0, 0.0, 0])
check("all-zero row: n_detected == 0 (zero is not detection, even though it's non-missing)", n_det == 0)
check("all-zero row: no stats computed", stats is None)

# --- string values also parse correctly (defensive -- in case a future source file
# uses strings instead of openpyxl floats) ---
n_det, n_tot, frac, stats = summarize_detection(["0.1", "", "0.3"])
check("string values: blank string excluded, numeric strings parsed", n_det == 2)

# --- panel/exclusion constants: ERBB2 is the only A_CLINICAL target in the 14-marker
# panel, and it is one of the two markers the source publication's own methods text
# says were excluded from analysis. ---
check("ERBB2 is in the 14-marker panel", "ERBB2" in PANEL_MARKERS)
check("panel has exactly 14 markers", len(PANEL_MARKERS) == 14)
check("ERBB2 is flagged as excluded by the source publication's own QC", "ERBB2" in EXCLUDED_MARKERS)
check("KRT7 is also flagged as excluded (the other marker named in the same sentence)",
      "KRT7" in EXCLUDED_MARKERS)
check("none of the other four A_CLINICAL targets are in this panel",
      not {"CEACAM5", "F3", "NECTIN4", "TACSTD2"} & PANEL_MARKERS)

if failures:
    print(f"\n{len(failures)} test(s) FAILED: {failures}")
    sys.exit(1)
print("\nAll detection/summary-statistics and panel-constant regression tests passed.")
