#!/usr/bin/env python3
"""Regression tests for extract_pxd055821_protein_abundance.py's
summarize_detection() -- the detection/summary-statistics logic. No real
PRIDE data needed -- pure unit tests on synthetic value rows.

Usage: python3 scripts/test_extract_pxd055821_protein_abundance.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from extract_pxd055821_protein_abundance import summarize_detection

failures = []


def check(label, cond):
    if not cond:
        failures.append(label)
        print(f"FAIL: {label}")
    else:
        print(f"ok: {label}")


# --- fully detected row ---
n_det, n_tot, frac, stats = summarize_detection(["10", "20", "30"])
check("fully-detected row: n_detected == 3", n_det == 3)
check("fully-detected row: n_total == 3", n_tot == 3)
check("fully-detected row: fraction == 1.0", frac == 1.0)
check("fully-detected row: median == 20", stats[0] == 20)
check("fully-detected row: min/max == 10/30", stats[1] == 10 and stats[2] == 30)

# --- partially detected row (blank strings = missing, matching DIA-NN's own convention) ---
n_det, n_tot, frac, stats = summarize_detection(["10", "", "  ", "40"])
check("partially-detected row: n_detected == 2 (blanks and whitespace-only excluded)", n_det == 2)
check("partially-detected row: n_total == 4", n_tot == 4)
check("partially-detected row: fraction == 0.5", frac == 0.5)
check("partially-detected row: median of [10, 40] == 25", stats[0] == 25)

# --- fully undetected row ---
n_det, n_tot, frac, stats = summarize_detection(["", "", ""])
check("fully-undetected row: n_detected == 0", n_det == 0)
check("fully-undetected row: fraction == 0.0", frac == 0.0)
check("fully-undetected row: no stats computed (empty detected list, not a division-by-zero)", stats is None)

# --- scientific-notation values parse correctly (real DIA-NN output uses this format) ---
n_det, n_tot, frac, stats = summarize_detection(["5.04E+07", "3.61E+07"])
check("scientific-notation values parse as floats", n_det == 2)
check("scientific-notation median is correct", abs(stats[0] - 4.325e7) < 1)

# --- empty column list (edge case: no sample columns at all) ---
n_det, n_tot, frac, stats = summarize_detection([])
check("empty column list: fraction is None, not a division-by-zero crash", frac is None)

if failures:
    print(f"\n{len(failures)} test(s) FAILED: {failures}")
    sys.exit(1)
print("\nAll detection/summary-statistics regression tests passed.")
