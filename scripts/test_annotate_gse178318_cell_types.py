#!/usr/bin/env python3
"""Regression tests for annotate_gse178318_cell_types.py's barcode parsing
and per-cell classification logic. No raw data needed -- pure unit tests.

Added/extended after web-ChatGPT round-1 review of PR #74 caught that the
first version only tested barcode parsing, not the classification math
(which had a real bug: dividing every category's raw marker-sum by the
same total-UMI denominator meant the denominator cancelled out of the
argmax comparison, so categories with more marker genes had a structural
size advantage).

Usage: python3 scripts/test_annotate_gse178318_cell_types.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from annotate_gse178318_cell_types import sample_key, classify_cell

failures = []


def check(label, cond):
    if not cond:
        failures.append(label)
        print(f"FAIL: {label}")
    else:
        print(f"ok: {label}")


# --- barcode parsing ---
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

# --- classification: category_gene_counts intentionally uneven (5 vs 1
# marker genes) to catch the exact bug the review found: without dividing
# by gene count, "fibroblast" (1 marker, count=6) would lose to "immune"
# (5 markers, raw sum=10) purely because immune has more marker genes, even
# though fibroblast's single marker is proportionally much more expressed.
GENE_COUNTS = {"immune": 5, "fibroblast": 1, "endothelial": 3}

check("category score is marker-average, not raw sum -- fibroblast wins on a per-gene basis",
      classify_cell(
          total_umi=100, epcam_count=0,
          category_sums={"immune": 10, "fibroblast": 6, "endothelial": 0},
          category_gene_counts=GENE_COUNTS,
      ) == "fibroblast")  # immune avg=10/5/100=0.02, fibroblast avg=6/1/100=0.06

check("epithelial (EPCAM alone) beats immune when EPCAM count is proportionally higher",
      classify_cell(
          total_umi=100, epcam_count=8,
          category_sums={"immune": 10, "fibroblast": 0, "endothelial": 0},
          category_gene_counts=GENE_COUNTS,
      ) == "epithelial")  # epcam=8/100=0.08 > immune avg=10/5/100=0.02

check("all-zero counts -> Unassigned, not a default category",
      classify_cell(
          total_umi=100, epcam_count=0,
          category_sums={"immune": 0, "fibroblast": 0, "endothelial": 0},
          category_gene_counts=GENE_COUNTS,
      ) == "Unassigned")

check("zero total UMI -> Unassigned (no division by zero)",
      classify_cell(
          total_umi=0, epcam_count=0,
          category_sums={"immune": 0, "fibroblast": 0, "endothelial": 0},
          category_gene_counts=GENE_COUNTS,
      ) == "Unassigned")

check("a category with zero marker genes registered never wins by division-by-zero",
      classify_cell(
          total_umi=100, epcam_count=0,
          category_sums={"immune": 5, "fibroblast": 0, "endothelial": 0},
          category_gene_counts={"immune": 5, "fibroblast": 0, "endothelial": 3},
      ) == "immune")

if failures:
    print(f"\n{len(failures)} test(s) FAILED: {failures}")
    sys.exit(1)
print("\nAll barcode-parsing and classification regression tests passed.")
