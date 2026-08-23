#!/usr/bin/env python3
"""Regression tests for infercnv_lite_gse178318.py's chromosome-arm parsing
and CNV-score aggregation logic. No raw data needed -- pure unit tests.

Usage: python3 scripts/test_infercnv_lite_gse178318.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from infercnv_lite_gse178318 import parse_arm, cell_arm_signal, aggregate_cnv_score

failures = []


def check(label, cond):
    if not cond:
        failures.append(label)
        print(f"FAIL: {label}")
    else:
        print(f"ok: {label}")


# --- parse_arm ---
check("standard band parses to chr+arm", parse_arm("17p13.3") == "17p")
check("X chromosome band parses correctly", parse_arm("Xq22.1") == "Xq")
check("two-digit chromosome parses correctly", parse_arm("20q13.13") == "20q")
check("'reserved' (withdrawn HGNC entry) returns None", parse_arm("reserved") is None)
check("'mitochondria' returns None", parse_arm("mitochondria") is None)
check("bare chromosome number with no arm letter returns None", parse_arm("20") is None)

# --- cell_arm_signal ---
usable_arms = {"1p", "1q", "2p"}
sig = cell_arm_signal({"1p": 100, "1q": 0}, total_umi=1000, usable_arms=usable_arms)
check("cell_arm_signal covers every usable arm, missing arm defaults to 0 count",
      set(sig.keys()) == usable_arms)
check("cell_arm_signal is log1p(count/total*10000), not a raw ratio",
      abs(sig["1p"] - __import__("math").log1p(100 / 1000 * 10000)) < 1e-9)
check("an arm with zero counts has zero signal (log1p(0)=0)", sig["2p"] == 0.0)

# --- aggregate_cnv_score ---
ref_mean = {"1p": 1.0, "1q": 1.0, "2p": 1.0}
ref_sd = {"1p": 0.5, "1q": 0.5, "2p": 0.5}
check("a cell exactly at the reference mean on every arm scores 0",
      aggregate_cnv_score({"1p": 1.0, "1q": 1.0, "2p": 1.0}, ref_mean, ref_sd, usable_arms) == 0.0)
check("a cell 2 SD above the mean on every arm scores 4 (z^2=4 averaged over equal arms)",
      abs(aggregate_cnv_score({"1p": 2.0, "1q": 2.0, "2p": 2.0}, ref_mean, ref_sd, usable_arms) - 4.0) < 1e-9)
check("a single wildly-different arm doesn't dominate the aggregate for a 3-arm cell "
      "(one arm at z=10, two arms at z=0 -> mean z^2 = 100/3, not 100)",
      abs(aggregate_cnv_score({"1p": 6.0, "1q": 1.0, "2p": 1.0}, ref_mean, ref_sd, usable_arms) - 100 / 3) < 1e-6)

if failures:
    print(f"\n{len(failures)} test(s) FAILED: {failures}")
    sys.exit(1)
print("\nAll arm-parsing and CNV-score regression tests passed.")
