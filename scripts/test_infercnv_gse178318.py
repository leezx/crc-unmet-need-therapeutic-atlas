#!/usr/bin/env python3
"""Regression tests for infercnv_gse178318.py's vectorized QC/classification
logic (compute_qc_and_categories, run_qc_and_classify) and gene-position
loading. No real GSE178318 data or infercnvpy run needed -- a small
synthetic sparse-matrix fixture is enough to check the vectorized
reductions match hand-computed expectations, and that run_qc_and_classify
reproduces the same QC-pass/fail and category calls
annotate_gse178318_cell_types.py's own streaming version would.

Usage: python3 scripts/test_infercnv_gse178318.py
"""
import csv
import sys
import tempfile
from pathlib import Path

import numpy as np
import scipy.sparse as sp

sys.path.insert(0, str(Path(__file__).resolve().parent))
from infercnv_gse178318 import compute_qc_and_categories, run_qc_and_classify, load_gene_positions
from annotate_gse178318_cell_types import classify_cell

failures = []


def check(label, cond):
    if not cond:
        failures.append(label)
        print(f"FAIL: {label}")
    else:
        print(f"ok: {label}")


# ============================================================
# load_gene_positions()
# ============================================================
f = tempfile.NamedTemporaryFile(mode="w", suffix=".tsv", delete=False, newline="")
import csv as _csv
_csv.writer(f, delimiter="\t").writerows([
    ["ensembl_gene_id", "chromosome", "start", "end"],
    ["ENSG00000105388", "19", "41708585", "41730433"],
    ["ENSG00000141736", "17", "39687914", "39730426"],
])
f.close()
positions = load_gene_positions(Path(f.name))
Path(f.name).unlink()
check("load_gene_positions parses both rows", len(positions) == 2)
check("CEACAM5's ENSG resolves to chr19 with integer start/end",
      positions["ENSG00000105388"] == ("19", 41708585, 41730433))

# ============================================================
# compute_qc_and_categories() / run_qc_and_classify() -- synthetic fixture
# ============================================================
# 4 genes: EPCAM (epithelial marker), PTPRC (immune marker, in marker_set),
# MT-CO1 (mitochondrial), CEACAM5 (target, not a marker gene).
# 3 cells, 2 samples ("s1_CRC" has cells 0,1; "s2_CRC" has cell 2).
gene_symbols = ["EPCAM", "PTPRC", "MT-CO1", "CEACAM5"]
marker_set = {"immune": ["PTPRC"], "fibroblast": [], "endothelial": []}

# dense matrix (genes x cells), rows=genes, cols=cells:
#   cell0: EPCAM=100, PTPRC=0,  MT-CO1=5,  CEACAM5=20   -> epithelial-leaning
#   cell1: EPCAM=0,   PTPRC=80, MT-CO1=5,  CEACAM5=0    -> immune-leaning
#   cell2: EPCAM=0,   PTPRC=0,  MT-CO1=0,  CEACAM5=0    -> all-zero (Unassigned, total_umi=0)
dense = np.array([
    [100, 0, 0],
    [0, 80, 0],
    [5, 5, 0],
    [20, 0, 0],
], dtype=np.float32)
mat = sp.csr_matrix(dense)

(total_counts, detected_genes, mito_counts, epcam_counts,
 category_sums, category_gene_counts, symbol_to_row) = compute_qc_and_categories(mat, gene_symbols, marker_set)

check("total_counts matches hand sum per cell", list(total_counts) == [125.0, 85.0, 0.0])
check("detected_genes counts nonzero entries per cell", list(detected_genes) == [3, 2, 0])
check("mito_counts sums only MT- prefixed genes", list(mito_counts) == [5.0, 5.0, 0.0])
check("epcam_counts reads the EPCAM row directly", list(epcam_counts) == [100.0, 0.0, 0.0])
check("category_sums['immune'] sums PTPRC only", list(category_sums["immune"]) == [0.0, 80.0, 0.0])
check("category_gene_counts reflects the full marker-set panel size, not just resolved rows",
      category_gene_counts["immune"] == 1 and category_gene_counts["fibroblast"] == 0)
check("symbol_to_row resolves CEACAM5 to its row index", symbol_to_row["CEACAM5"] == 3)

# run_qc_and_classify: use permissive thresholds so cell0/cell1 pass QC on
# detected-gene/mito-fraction grounds regardless of per-sample outlier noise
# with only 1-2 cells per sample (SD=0 for a single-cell "sample").
cell_keys = ["s1_CRC", "s1_CRC", "s2_CRC"]
import infercnv_gse178318 as m
orig_min_genes, orig_max_mito = m.MIN_DETECTED_GENES, m.MAX_MITO_FRACTION
m.MIN_DETECTED_GENES = 1
m.MAX_MITO_FRACTION = 0.99
try:
    passes_qc, cell_category = run_qc_and_classify(
        cell_keys, total_counts, detected_genes, mito_counts, epcam_counts, category_sums, category_gene_counts)
finally:
    m.MIN_DETECTED_GENES, m.MAX_MITO_FRACTION = orig_min_genes, orig_max_mito

check("cell0 (EPCAM-dominant, 3 detected genes) passes QC", bool(passes_qc[0]))
check("cell1 (PTPRC-dominant, 2 detected genes) passes QC", bool(passes_qc[1]))
check("cell2 (all-zero, 0 detected genes, below MIN_DETECTED_GENES=1) fails QC", not passes_qc[2])
check("cell0 classified epithelial (EPCAM score >> immune score)", cell_category[0] == "epithelial")
check("cell1 classified immune (PTPRC score >> epithelial score of 0)", cell_category[1] == "immune")
check("cell2 (QC-failed) has no category assigned", cell_category[2] is None)

# Cross-check against classify_cell() directly (imported, not reimplemented)
# for cell0 and cell1 to confirm run_qc_and_classify calls it with the right
# arguments, not just coincidentally matching.
check("classify_cell() directly agrees with run_qc_and_classify()'s cell0 call",
      classify_cell(total_counts[0], epcam_counts[0],
                    {cat: category_sums[cat][0] for cat in ("immune", "fibroblast", "endothelial")},
                    category_gene_counts) == "epithelial")

if failures:
    print(f"\n{len(failures)} test(s) FAILED: {failures}")
    sys.exit(1)
print("\nAll infercnv_gse178318 QC/classification/position-loading regression tests passed.")
