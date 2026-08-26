#!/usr/bin/env python3
"""Module B: real gene-window InferCNV (via `infercnvpy`) for GSE178318's
epithelial-proxy cells, to distinguish malignancy-consistent (CNV_HIGH)
from not-confirmed (CNV_LOW) among the cells
scripts/annotate_gse178318_cell_types.py identifies as epithelial-proxy.

This is the higher-power follow-up Next-handoff item 1 named after
scripts/infercnv_lite_gse178318.py's own chromosome-arm-level attempt
(analysis_contracts/infercnv_lite_gse178318.md) came back with an
ambiguous, nonconfirmatory signal -- that method's own "Explicit
limitations" section named exactly two things a real InferCNV-style
method has that it did not: gene-order local structure (a moving window
along genes in true genomic order, not an arm-level bucket that discards
gene order entirely) and an explicit centering/reference-subtraction
step (not a coarser z-score stand-in). `infercnvpy` (pip-installed
2026-08-26; a real, actively-maintained scanpy-ecosystem reimplementation
of the Broad Institute's inferCNV algorithm -- confirmed installable and
network-reachable in this environment) provides both, so this script
uses that actual package rather than re-implementing gene-window
smoothing from scratch. Full method, locked choices, and results:
modules/module_b_mcrc_target_prevalence/analysis_contracts/
infercnv_gse178318.md.

**Population definitions are reused byte-for-byte from
infercnv_lite_gse178318.py's own build_populations()** -- same reference
(QC-passing, immune-classified, tumor-site, treated-cohort-only cells)
and same epithelial-proxy population (QC-passing, epithelial-classified,
tumor-site, treated-cohort-only cells), same fit/holdout reference split
(same seed). This is deliberate: the only thing this script changes
relative to the CNV-lite attempt is the CNV-inference algorithm itself
(arm-level z-score vs. real gene-window InferCNV) -- if the two methods'
results differ, that difference is attributable to the algorithm, not to
a different cell-selection pipeline being silently swapped in alongside
it.

QC/classification statistics (total UMI, detected genes, mitochondrial
fraction, EPCAM/marker-category sums) are computed by vectorized sparse-
matrix row/column sums over the full loaded expression matrix, not by
annotate_gse178318_cell_types.py's own streaming per-line loop -- but
using the exact same definitions (same MIN_DETECTED_GENES/
MAX_MITO_FRACTION/BATCH_OUTLIER_SD constants, same classify_cell()
function, imported directly, not reimplemented) and mathematically
identical results, since summing the same per-cell entries with a
vectorized reduction versus a streaming accumulator produces the same
numbers by construction. Reading and holding the full 166.7M-entry
sparse matrix in memory (unlike the streaming scripts) is a deliberate
choice here: `infercnvpy` itself needs the full expression matrix
in-memory for its smoothing step regardless, so streaming to avoid one
transient matrix construction would not have avoided the larger
in-memory requirement anyway.

Gene genomic positions: DATA/reference/ensembl_gene_positions_grch38_
release110.tsv (built by scripts/build_ensembl_gene_positions.py;
97.4%/32,807 of GSE178318's 33,694 genes resolve to a position -- the
remaining 2.6% are excluded from the CNV-window computation, not guessed
at). This is the one thing the coarser arm-level attempt could not do
with its existing HGNC reference (cytogenetic bands only, no base-pair
coordinates).

**Dependencies**: this is the first (and, as of 2026-08-26, only) script
in this repository that is not Python-standard-library-only -- see
scripts/requirements_infercnv.txt (pip3 install -r
scripts/requirements_infercnv.txt) before running this script or
scripts/build_ensembl_gene_positions.py. infercnvpy 0.6.1's internal
gene-window indexing breaks under pandas>=3.0's new default Arrow-backed
string dtype (ArrowInvalid: only handle 1-dimensional arrays); this
script works around that at runtime via
pd.set_option("future.infer_string", False), set before any
DataFrame/AnnData with string columns is constructed.

Usage: python3 scripts/infercnv_gse178318.py --gene CEACAM5
"""
import argparse
import csv
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import scipy.sparse as sp

# infercnvpy 0.6.1's internal windowing code indexes a gene-name Index with a
# 2D numpy array of convolution indices -- this only works with numpy's
# legacy object-dtype string storage, not pandas 3.x's new default
# Arrow-backed string dtype (ArrowStringArray.take() only accepts 1D
# indices, raising "ArrowInvalid: only handle 1-dimensional arrays").
# Confirmed 2026-08-26: pandas 3.0.2 was the version pip installed in this
# environment; this option must be set before any AnnData/DataFrame with
# string columns is constructed, not just before calling infercnvpy.
pd.set_option("future.infer_string", False)

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))
from annotate_gse178318_cell_types import (  # noqa: E402
    resolve_files, read_lines, sample_key, load_sample_map, load_marker_set,
    classify_cell, NON_EPITHELIAL_CATEGORIES, TREATED_PATIENTS, UNTREATED_PATIENTS,
    MIN_DETECTED_GENES, MAX_MITO_FRACTION, BATCH_OUTLIER_SD,
)
from infercnv_lite_gse178318 import build_populations  # noqa: E402

GENE_POSITIONS_PATH = REPO_ROOT / "DATA" / "reference" / "ensembl_gene_positions_grch38_release110.tsv"
CNV_REFERENCE_PERCENTILE = 0.99


def load_gene_positions(path):
    positions = {}
    with open(path, newline="") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            positions[row["ensembl_gene_id"]] = (row["chromosome"], int(row["start"]), int(row["end"]))
    return positions


def compute_qc_and_categories(mat, gene_symbols, marker_set):
    """Vectorized equivalent of annotate_gse178318_cell_types.py's own
    per-cell streaming accumulation (total UMI, detected genes,
    mitochondrial UMI, EPCAM count, marker-category sums) -- same
    definitions, same numbers, computed as sparse-matrix reductions
    instead of a Python line-by-line loop, since the full matrix is
    already resident in memory for infercnvpy's own needs regardless."""
    n_cells = mat.shape[1]
    total_counts = np.asarray(mat.sum(axis=0)).flatten()
    detected_genes = mat.getnnz(axis=0)

    symbol_to_row = {}
    for i, sym in enumerate(gene_symbols):
        symbol_to_row.setdefault(sym, i)

    mito_rows = [i for i, s in enumerate(gene_symbols) if s.startswith("MT-")]
    mito_counts = np.asarray(mat[mito_rows, :].sum(axis=0)).flatten() if mito_rows else np.zeros(n_cells)
    epcam_counts = np.asarray(mat[symbol_to_row["EPCAM"], :].todense()).flatten()

    category_sums = {}
    category_gene_counts = {}
    for cat in NON_EPITHELIAL_CATEGORIES:
        rows = [symbol_to_row[g] for g in marker_set[cat] if g in symbol_to_row]
        category_gene_counts[cat] = len(marker_set[cat])
        category_sums[cat] = np.asarray(mat[rows, :].sum(axis=0)).flatten() if rows else np.zeros(n_cells)

    return total_counts, detected_genes, mito_counts, epcam_counts, category_sums, category_gene_counts, symbol_to_row


def run_qc_and_classify(cell_keys, total_counts, detected_genes, mito_counts, epcam_counts, category_sums, category_gene_counts):
    """Same QC thresholds and per-sample-batch outlier logic as
    annotate_gse178318_cell_types.py's main(), and the same classify_cell()
    function -- reimplemented as a per-cell loop (not vectorized: the
    per-sample-batch mean/SD computation is simplest to get right this way,
    and 140,281 iterations of simple arithmetic is not a performance
    concern)."""
    n_cells = len(cell_keys)
    by_sample_indices = {}
    for i, key in enumerate(cell_keys):
        by_sample_indices.setdefault(key, []).append(i)

    passes_qc = np.zeros(n_cells, dtype=bool)
    for key, idxs in by_sample_indices.items():
        log_totals = [np.log10(total_counts[i]) if total_counts[i] > 0 else 0.0 for i in idxs]
        mean_log_total = sum(log_totals) / len(log_totals)
        sd_log_total = (sum((x - mean_log_total) ** 2 for x in log_totals) / len(log_totals)) ** 0.5
        gene_vals = [detected_genes[i] for i in idxs]
        mean_genes = sum(gene_vals) / len(gene_vals)
        sd_genes = (sum((x - mean_genes) ** 2 for x in gene_vals) / len(gene_vals)) ** 0.5
        for i, log_total in zip(idxs, log_totals):
            if detected_genes[i] < MIN_DETECTED_GENES or total_counts[i] == 0:
                continue
            if mito_counts[i] / total_counts[i] > MAX_MITO_FRACTION:
                continue
            if sd_log_total > 0 and abs(log_total - mean_log_total) > BATCH_OUTLIER_SD * sd_log_total:
                continue
            if sd_genes > 0 and abs(detected_genes[i] - mean_genes) > BATCH_OUTLIER_SD * sd_genes:
                continue
            passes_qc[i] = True

    cell_category = [None] * n_cells
    for i in range(n_cells):
        if passes_qc[i]:
            cell_category[i] = classify_cell(
                total_counts[i], epcam_counts[i],
                {cat: category_sums[cat][i] for cat in NON_EPITHELIAL_CATEGORIES},
                category_gene_counts,
            )
    return passes_qc, cell_category


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gene", required=True)
    ap.add_argument("--marker-set", default=str(
        REPO_ROOT / "modules" / "module_b_mcrc_target_prevalence" / "analysis_contracts" / "cell_type_marker_set_v1.tsv"
    ))
    ap.add_argument("--seed", type=int, default=42, help="RNG seed for the reference fit/holdout split (same default as infercnv_lite_gse178318.py)")
    args = ap.parse_args()
    gene = args.gene.strip()

    if not GENE_POSITIONS_PATH.is_file():
        print(f"ERROR: {GENE_POSITIONS_PATH} not found. Run scripts/build_ensembl_gene_positions.py first.", file=sys.stderr)
        sys.exit(1)
    gene_positions = load_gene_positions(GENE_POSITIONS_PATH)
    print(f"Loaded {len(gene_positions)} gene positions from {GENE_POSITIONS_PATH.name}", file=sys.stderr)

    files = resolve_files()
    barcodes = read_lines(files["GSE178318_barcodes.tsv.gz"])
    genes_raw = read_lines(files["GSE178318_genes.tsv.gz"])
    ensg_ids = [g.split("\t")[0] for g in genes_raw]
    gene_symbols = [g.split("\t")[-1] for g in genes_raw]
    n_genes, n_cells = len(genes_raw), len(barcodes)

    sample_map_path = REPO_ROOT / "DATA" / "registry" / "GSE178318" / "sample_map.tsv"
    sample_map = load_sample_map(sample_map_path)
    cell_keys = [sample_key(b) for b in barcodes]
    if any(k == "UNPARSEABLE" for k in cell_keys):
        print("ERROR: unparseable barcode.", file=sys.stderr)
        sys.exit(1)

    n_resolved = sum(1 for e in ensg_ids if e in gene_positions)
    print(f"{n_resolved}/{n_genes} ({n_resolved/n_genes:.1%}) of GSE178318's genes resolve to a genomic position.", file=sys.stderr)

    marker_set = load_marker_set(args.marker_set)
    symbol_to_row_check = {}
    for i, sym in enumerate(gene_symbols):
        symbol_to_row_check.setdefault(sym, i)
    if gene not in symbol_to_row_check:
        print(f"ERROR: '{gene}' not in gene index.", file=sys.stderr)
        sys.exit(1)

    print("Streaming full matrix into memory (needed by infercnvpy regardless)...", file=sys.stderr)
    df = pd.read_csv(files["GSE178318_matrix.mtx.gz"], sep=" ", skiprows=3, header=None,
                      names=["gene_row", "cell_col", "count"],
                      dtype={"gene_row": np.int32, "cell_col": np.int32, "count": np.float32},
                      engine="c")
    mat = sp.coo_matrix((df["count"].values, (df["gene_row"].values - 1, df["cell_col"].values - 1)),
                         shape=(n_genes, n_cells)).tocsr()
    del df
    print(f"Matrix loaded: {mat.shape[0]} genes x {mat.shape[1]} cells, nnz={mat.nnz}", file=sys.stderr)

    (total_counts, detected_genes, mito_counts, epcam_counts,
     category_sums, category_gene_counts, symbol_to_row) = compute_qc_and_categories(mat, gene_symbols, marker_set)
    passes_qc, cell_category = run_qc_and_classify(
        cell_keys, total_counts, detected_genes, mito_counts, epcam_counts, category_sums, category_gene_counts)
    print(f"QC-passing cells: {passes_qc.sum()}/{n_cells}", file=sys.stderr)

    # Same population definitions as infercnv_lite_gse178318.py, treated
    # cohort only (COL15/COL17/COL18) -- see that script's build_populations()
    # docstring for the full reasoning (tumor-site samples only, never PBMC;
    # patient_filter=TREATED_PATIENTS so a treated-cohort dossier is never
    # scored against a pooled or treatment-naive reference).
    reference_idx, epithelial_idx = build_populations(
        n_cells, passes_qc.tolist(), cell_category, cell_keys, sample_map, TREATED_PATIENTS)
    print(f"Reference (immune, tumor-site, treated): {len(reference_idx)} cells", file=sys.stderr)
    print(f"Epithelial-proxy (tumor-site, treated): {len(epithelial_idx)} cells", file=sys.stderr)

    if len(reference_idx) < 200:
        print("ERROR: reference population too small (<200 cells) for a stable null distribution.", file=sys.stderr)
        sys.exit(1)

    import random
    random.seed(args.seed)
    shuffled = reference_idx[:]
    random.shuffle(shuffled)
    half = len(shuffled) // 2
    ref_fit_idx, ref_holdout_idx = shuffled[:half], shuffled[half:]
    print(f"Reference fit/holdout split (seed={args.seed}): fit n={len(ref_fit_idx)}, holdout n={len(ref_holdout_idx)}", file=sys.stderr)

    # Restrict to genes with a resolved position AND present in gene_positions,
    # and to the cells actually needed (fit + holdout + epithelial-proxy) --
    # smaller AnnData, faster infercnvpy run, same result as running on the
    # full 140,281-cell matrix (infercnvpy processes cells independently).
    keep_gene_mask = np.array([e in gene_positions for e in ensg_ids])
    kept_gene_idx = np.nonzero(keep_gene_mask)[0]
    print(f"Genes retained for the CNV window computation: {len(kept_gene_idx)}/{n_genes}", file=sys.stderr)

    all_cell_idx = sorted(set(ref_fit_idx) | set(ref_holdout_idx) | set(epithelial_idx))
    cell_pos_in_subset = {c: i for i, c in enumerate(all_cell_idx)}

    sub = mat[kept_gene_idx, :][:, all_cell_idx]  # genes x cells, subset
    sub = sub.T.tocsr()  # cells x genes, for AnnData (obs=cells, var=genes)
    print(f"Subset matrix for infercnvpy: {sub.shape[0]} cells x {sub.shape[1]} genes", file=sys.stderr)

    import anndata
    import scanpy as sc
    import infercnvpy as cnv

    var = pd.DataFrame(index=[ensg_ids[i] for i in kept_gene_idx])
    var["gene_symbol"] = [gene_symbols[i] for i in kept_gene_idx]
    chroms, starts, ends = [], [], []
    for i in kept_gene_idx:
        c, s, e = gene_positions[ensg_ids[i]]
        chroms.append(f"chr{c}")
        starts.append(s)
        ends.append(e)
    var["chromosome"] = chroms
    var["start"] = starts
    var["end"] = ends

    obs = pd.DataFrame(index=[str(c) for c in all_cell_idx])
    obs["sample_key"] = [cell_keys[c] for c in all_cell_idx]
    role = []
    for c in all_cell_idx:
        if c in set(ref_fit_idx):
            role.append("reference_fit")
        elif c in set(ref_holdout_idx):
            role.append("reference_holdout")
        else:
            role.append("epithelial_proxy")
    obs["role"] = role

    adata = anndata.AnnData(X=sub, obs=obs, var=var)
    print(f"AnnData built: {adata.shape}", file=sys.stderr)

    # Standard scanpy preprocessing (library-size normalization + log1p) before
    # gene-window CNV smoothing -- the standard infercnvpy/inferCNV precondition
    # (raw counts are not directly comparable across cells of different depth).
    sc.pp.normalize_total(adata, target_sum=1e4)
    sc.pp.log1p(adata)

    # Reference vector: mean of the FIT half of the reference population only
    # (never the holdout half, never epithelial-proxy cells) -- passed directly
    # via infercnvpy's `reference=` parameter so it is not silently
    # re-estimated from cells this script needs to score against it.
    fit_mask = (adata.obs["role"] == "reference_fit").values
    reference_vector = np.asarray(adata.X[fit_mask, :].mean(axis=0)).flatten()

    print("Running infercnvpy.tl.infercnv() (package defaults: window_size=100, "
          "step=10, lfc_clip=3, dynamic_threshold=1.5, exclude_chromosomes=(chrX,chrY))...",
          file=sys.stderr)
    cnv.tl.infercnv(adata, reference=reference_vector)
    print("infercnv() complete.", file=sys.stderr)

    # Per-cell CNV score: mean(|X_cnv|) across all windows for that cell --
    # the same aggregate infercnvpy's own cnv.tl.cnv_score() uses per Leiden
    # cluster, applied per-cell instead (no clustering step introduced here,
    # which would need its own locked hyperparameters).
    X_cnv = adata.obsm["X_cnv"]
    cnv_score_per_cell = np.asarray(np.abs(X_cnv).mean(axis=1)).flatten()
    adata.obs["cnv_score"] = cnv_score_per_cell

    holdout_scores = np.sort(cnv_score_per_cell[(adata.obs["role"] == "reference_holdout").values])
    fit_scores = np.sort(cnv_score_per_cell[(adata.obs["role"] == "reference_fit").values])
    epi_scores_arr = cnv_score_per_cell[(adata.obs["role"] == "epithelial_proxy").values]
    epi_scores = np.sort(epi_scores_arr)

    threshold_idx = min(int(len(holdout_scores) * CNV_REFERENCE_PERCENTILE), len(holdout_scores) - 1)
    threshold = holdout_scores[threshold_idx]

    def pct(sorted_vals, p):
        idx = min(int(len(sorted_vals) * p), len(sorted_vals) - 1)
        return sorted_vals[idx]

    print(f"\nFit-half reference CNV score (n={len(fit_scores)}): median={pct(fit_scores, 0.5):.5f}", file=sys.stderr)
    print(f"Held-out reference CNV score (n={len(holdout_scores)}; threshold = this half's own "
          f"{CNV_REFERENCE_PERCENTILE:.0%}ile, so its own exceedance rate is the ~1% null rate by "
          f"construction, not independent evidence): median={pct(holdout_scores, 0.5):.5f} "
          f"p90={pct(holdout_scores, 0.9):.5f} p99={pct(holdout_scores, 0.99):.5f} (threshold={threshold:.5f})",
          file=sys.stderr)
    if len(epi_scores):
        print(f"Epithelial-proxy CNV score (n={len(epi_scores)}): min={epi_scores[0]:.5f} "
              f"p10={pct(epi_scores,0.10):.5f} p25={pct(epi_scores,0.25):.5f} median={pct(epi_scores,0.5):.5f} "
              f"p75={pct(epi_scores,0.75):.5f} p90={pct(epi_scores,0.9):.5f} p99={pct(epi_scores,0.99):.5f} "
              f"max={epi_scores[-1]:.5f}", file=sys.stderr)

    n_holdout_high = int((holdout_scores > threshold).sum())
    n_epi_high = int((epi_scores > threshold).sum())
    holdout_high_frac = n_holdout_high / len(holdout_scores) if len(holdout_scores) else 0.0
    epi_high_frac = n_epi_high / len(epi_scores) if len(epi_scores) else 0.0
    enrichment = (epi_high_frac / holdout_high_frac) if holdout_high_frac > 0 else float("inf")
    print(f"CNV_HIGH (score > threshold): epithelial-proxy {n_epi_high}/{len(epi_scores)} "
          f"({epi_high_frac:.2%}) vs held-out reference's own {n_holdout_high}/{len(holdout_scores)} "
          f"({holdout_high_frac:.2%}) -- enrichment ratio {enrichment:.2f}x", file=sys.stderr)

    # Per-sample CEACAM5-positive fraction within CNV_HIGH / CNV_LOW
    # epithelial-proxy cells -- same output shape as infercnv_lite_gse178318.py
    # for direct side-by-side comparison.
    target_row = symbol_to_row[gene]
    target_counts_full = np.asarray(mat[target_row, :].todense()).flatten()

    per_sample = {}
    epi_mask = (adata.obs["role"] == "epithelial_proxy").values
    epi_cell_ids = [int(x) for x in adata.obs.index[epi_mask]]
    for c, score in zip(epi_cell_ids, cnv_score_per_cell[epi_mask]):
        key = cell_keys[c]
        s = per_sample.setdefault(key, {"n_epithelial": 0, "n_cnv_high": 0, "n_cnv_high_target_pos": 0,
                                         "n_cnv_low": 0, "n_cnv_low_target_pos": 0})
        s["n_epithelial"] += 1
        is_pos = target_counts_full[c] > 0
        if score > threshold:
            s["n_cnv_high"] += 1
            if is_pos:
                s["n_cnv_high_target_pos"] += 1
        else:
            s["n_cnv_low"] += 1
            if is_pos:
                s["n_cnv_low_target_pos"] += 1

    out_rows = []
    for key, s in sorted(per_sample.items()):
        info = sample_map[key]
        frac_high = s["n_cnv_high_target_pos"] / s["n_cnv_high"] if s["n_cnv_high"] else None
        frac_low = s["n_cnv_low_target_pos"] / s["n_cnv_low"] if s["n_cnv_low"] else None
        out_rows.append({
            "sample_key": key, "patient_id": info["patient_id"], "specimen_type": info["specimen_type"],
            "n_epithelial_proxy": s["n_epithelial"],
            "n_cnv_high": s["n_cnv_high"], "n_cnv_low": s["n_cnv_low"],
            f"{gene}_pos_frac_cnv_high": round(frac_high, 4) if frac_high is not None else "NA",
            f"{gene}_pos_frac_cnv_low": round(frac_low, 4) if frac_low is not None else "NA",
        })

    out_path = REPO_ROOT / "modules" / "module_b_mcrc_target_prevalence" / "results" / f"tgt_{gene.lower()}_infercnv_attempt.tsv"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out_rows[0].keys()), delimiter="\t")
        w.writeheader()
        for r in out_rows:
            w.writerow(r)
    print(f"\nWrote {len(out_rows)} sample rows to {out_path}")

    print("\nCNV_HIGH subset per sample (real gene-window InferCNV, see analysis contract for interpretation):")
    for r in out_rows:
        print(f"  {r['sample_key']:14s} n_epi={r['n_epithelial_proxy']:5d} "
              f"CNV_HIGH={r['n_cnv_high']:5d} ({r[f'{gene}_pos_frac_cnv_high']})  "
              f"CNV_LOW={r['n_cnv_low']:5d} ({r[f'{gene}_pos_frac_cnv_low']})")


if __name__ == "__main__":
    main()
