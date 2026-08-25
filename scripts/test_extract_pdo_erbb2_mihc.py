#!/usr/bin/env python3
"""Regression tests for extract_pdo_erbb2_mihc.py's summarize_values()
-- the numeric-value summary logic (NOT a detection/prevalence
function -- the source publication states no assay-detection
threshold, so this script only ever reports numeric-value counts and
summary statistics). No real Mendeley Data xlsx needed -- pure unit
tests on synthetic value rows (openpyxl returns floats/None from a real
workbook, so these tests use float/None inputs, not strings, matching
actual usage).

Usage: python3 scripts/test_extract_pdo_erbb2_mihc.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from extract_pdo_erbb2_mihc import summarize_values, PANEL_MARKERS, EXCLUDED_MARKERS

failures = []


def check(label, cond):
    if not cond:
        failures.append(label)
        print(f"FAIL: {label}")
    else:
        print(f"ok: {label}")


# --- all rows carry a nonzero numeric value (real openpyxl values: floats) ---
n_nonzero, n_tot, frac, stats = summarize_values([0.1, 0.2, 0.3])
check("all-nonzero row: n_nonzero == 3", n_nonzero == 3)
check("all-nonzero row: n_total == 3", n_tot == 3)
check("all-nonzero row: fraction == 1.0", frac == 1.0)
check("all-nonzero row: median == 0.2", abs(stats[0] - 0.2) < 1e-9)
check("all-nonzero row: min/max == 0.1/0.3", stats[1] == 0.1 and stats[2] == 0.3)

# --- some rows missing (None = missing cell, matching openpyxl's own convention) ---
n_nonzero, n_tot, frac, stats = summarize_values([0.1, None, 0.4])
check("partial row: n_nonzero == 2 (None excluded)", n_nonzero == 2)
check("partial row: n_total == 3", n_tot == 3)
check("partial row: median of [0.1, 0.4] == 0.25", abs(stats[0] - 0.25) < 1e-9)

# --- all rows missing ---
n_nonzero, n_tot, frac, stats = summarize_values([None, None])
check("all-missing row: n_nonzero == 0", n_nonzero == 0)
check("all-missing row: fraction == 0.0", frac == 0.0)
check("all-missing row: no stats computed (empty nonzero list, not a division-by-zero)", stats is None)

# --- empty row list (edge case: no rows at all for a marker) ---
n_nonzero, n_tot, frac, stats = summarize_values([])
check("empty row list: fraction is None, not a division-by-zero crash", frac is None)

# --- a literal 0 value is excluded from the nonzero count/stats -- this function reports
# nonzero-value counts, not a "detected" claim (round 1 review of PR #84: a numeric value
# > 0 is not evidence of biological detection; this repo does not claim it is). ---
n_nonzero, n_tot, frac, stats = summarize_values([0.1, 0, 0.2])
check("a literal 0 value is excluded from the nonzero count", n_nonzero == 2)
check("0 does not appear in the computed stats (median of [0.1, 0.2] == 0.15, not affected by 0)",
      abs(stats[0] - 0.15) < 1e-9)
n_nonzero, n_tot, frac, stats = summarize_values([0, 0.0, 0])
check("all-zero row: n_nonzero == 0", n_nonzero == 0)
check("all-zero row: no stats computed", stats is None)

# --- string values also parse correctly (defensive -- in case a future source file
# uses strings instead of openpyxl floats) ---
n_nonzero, n_tot, frac, stats = summarize_values(["0.1", "", "0.3"])
check("string values: blank string excluded, numeric strings parsed", n_nonzero == 2)

# --- panel constants: ERBB2 is the only A_CLINICAL target in the 14-marker panel. ---
check("ERBB2 is in the 14-marker panel", "ERBB2" in PANEL_MARKERS)
check("panel has exactly 14 markers", len(PANEL_MARKERS) == 14)
check("none of the other four A_CLINICAL targets are in this panel",
      not {"CEACAM5", "F3", "NECTIN4", "TACSTD2"} & PANEL_MARKERS)

# --- EXCLUDED_MARKERS preserves the source publication's own "respectively" --
# KRT7 and ERBB2 were excluded for two DIFFERENT reasons, not the same shared string
# (round 1 review of PR #84 caught an earlier version collapsing both into one string,
# erasing "respectively"). ---
check("ERBB2 is flagged as excluded by the source publication", "ERBB2" in EXCLUDED_MARKERS)
check("KRT7 is also flagged as excluded (the other marker named in the same sentence)",
      "KRT7" in EXCLUDED_MARKERS)
check("ERBB2's exclusion reason is marker-specific: 'very low expression levels'",
      EXCLUDED_MARKERS["ERBB2"] == "very low expression levels")
check("KRT7's exclusion reason is marker-specific and DIFFERENT from ERBB2's: 'no expression'",
      EXCLUDED_MARKERS["KRT7"] == "no expression")
check("KRT7 and ERBB2 do not share the same exclusion-reason string ('respectively' preserved)",
      EXCLUDED_MARKERS["KRT7"] != EXCLUDED_MARKERS["ERBB2"])

if failures:
    print(f"\n{len(failures)} test(s) FAILED: {failures}")
    sys.exit(1)
print("\nAll numeric-value-summary and panel-constant regression tests passed.")
