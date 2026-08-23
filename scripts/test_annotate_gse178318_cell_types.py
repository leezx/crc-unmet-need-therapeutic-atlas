#!/usr/bin/env python3
"""Regression tests for annotate_gse178318_cell_types.py's barcode parsing.

No raw data needed -- pure unit tests on sample_key().

Usage: python3 scripts/test_annotate_gse178318_cell_types.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from annotate_gse178318_cell_types import sample_key

failures = []


def check(label, cond):
    if not cond:
        failures.append(label)
        print(f"FAIL: {label}")
    else:
        print(f"ok: {label}")


check("primary CRC barcode parses to PATIENT_CRC",
      sample_key("AAACCTGAGAAACCTA_COL07_CRC") == "COL07_CRC")
check("liver metastasis barcode parses to PATIENT_LM",
      sample_key("CTGATCCAGGGAACGG_COL07_LM") == "COL07_LM")
check("PBMC barcode parses to PATIENT_PBMC",
      sample_key("TTCGGTCGTCGCGGTT_COL18_PBMC") == "COL18_PBMC")
check("barcode with no underscore is UNPARSEABLE",
      sample_key("AAACCTGAGAAACCTA") == "UNPARSEABLE")
check("barcode with only one underscore is UNPARSEABLE",
      sample_key("AAACCTGAGAAACCTA_COL07") == "UNPARSEABLE")

if failures:
    print(f"\n{len(failures)} test(s) FAILED: {failures}")
    sys.exit(1)
print("\nAll barcode-parsing regression tests passed.")
