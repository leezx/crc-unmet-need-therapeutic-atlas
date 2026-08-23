# Module B data lock — `tgt_ceacam5`

Status: **`GSE178318` — LOCKED, QC-filtered, epithelial-proxy screened (NOT malignancy-confirmed). `GSE225857` — still blocked on data access.**

Revised 2026-08-23 (PR #74 round 1 review): the previous version of this file described `GSE178318`'s cell-type split as resolved without QC and without acknowledging the gap versus the dataset's own published malignancy-confirmation method. Corrected below — see `analysis_contracts/tgt_ceacam5.md` for the full method, results, and every caveat. `GSE225857` remains blocked exactly as before.

## `GSE178318` — matrix, gene index, patient/sample annotation, QC, and epithelial-proxy split are all present; malignancy is NOT confirmed

- `DATA/registry/GSE178318/source_manifest.tsv` and `file_inventory.tsv` record `GSE178318_barcodes.tsv.gz`, `GSE178318_genes.tsv.gz`, and `GSE178318_matrix.mtx.gz` (520.7 MB, 33,694 genes x 140,281 cells, SHA256-verified) as downloaded 2026-08-11. All three files are physically present (gitignored, never deleted) at `archive/phase2_fetal_state_track_v1/phase2/03_data/raw/GSE178318/`. `source_manifest.tsv`'s DOI was corrected 2026-08-23 (round 1 review): the previously-recorded `10.1038/s41598-021-96568-3` does not resolve; the real paper is `10.1038/s41421-021-00312-y` (Cell Discovery 2021).
- `CEACAM5` (`ENSG00000105388`) confirmed present in the gene index (row 31446).
- `DATA/registry/GSE178318/sample_map.tsv` carries real patient/sample-level annotation for all 15 barcode groups, including which 3 of 6 patients (`COL15`/`COL17`/`COL18`) actually received preoperative chemotherapy.
- **QC**: `scripts/annotate_gse178318_cell_types.py` applies the source publication's own thresholds (>=500 detected genes, <=15% mitochondrial UMI, per-sample 3-SD outlier removal on log-total-UMI and gene count) — 123,330 of 140,281 barcodes pass (paper: 111,292 of 140,281 via its own pipeline; not expected to match exactly, batch definition differs).
- **Epithelial-proxy identification**: EPCAM expression alone (matching the paper's own stated method), scored as a marker-average fraction of total UMI to avoid the earlier version's bug where categories with more marker genes were structurally favored.
- **What is still not done, and is not attempted in this pass**: the source publication confirms EPCs are malignant via InferCNV (transcriptome-inferred copy-number variation). That step needs a genomic gene-position reference and a chosen normal-cell reference population — real additional engineering, not reproduced here. This screen stops at "EPCAM-high, QC-passing cell in a tumor-site specimen," stated as an epithelial-proxy, not a malignancy-confirmed result, everywhere it is used.

## `GSE225857` — still genuinely no local processed data

- Unchanged from the previous version of this file: no raw or processed file for `GSE225857` exists anywhere on the machine that ran this pass. `DATA/registry/GSE225857/source_manifest.tsv` records most of its single-cell data as hosted at CNSA (`CNP0002540`/`CNP0003321`), with `access_status=SOURCE_INDEXED_REVIEW_REQUIRED` — CNSA access terms have not been independently reviewed (see `reports/PROJECT_STATUS.md`'s Next-handoff item on this). GEO itself only carries 8 GSM records for this series, not the full processed matrix.

## Both datasets remain `status=CANDIDATE`

Neither has been promoted to `APPROVED` in `DATA/registry/datasets.tsv`. Running the QC/epithelial-proxy analysis over `GSE178318`'s already-present, already-checksum-verified files is a real analysis step, not a new download.

## What would close Module B's actual malignant-cell prevalence question for this target

Reproducing the source publication's InferCNV-based malignancy confirmation on the epithelial-proxy cells identified here (or a comparably rigorous CNV-inference method) — not attempted in this pass. For `GSE225857`: CNSA access-terms review, then a real fetch.
