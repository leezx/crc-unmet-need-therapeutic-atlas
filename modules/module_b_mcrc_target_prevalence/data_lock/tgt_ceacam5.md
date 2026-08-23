# Module B data lock — `tgt_ceacam5`

Status: **`GSE178318` — LOCKED and analyzed. `GSE225857` — still blocked on data access.**

Updated 2026-08-23 (closing the vertical slice PR #73's own reviewer recommended finishing): `GSE178318`'s cell-type annotation gap is now resolved by `../../scripts/annotate_gse178318_cell_types.py` (marker-gene-score cell-compartment split — see `analysis_contracts/tgt_ceacam5.md` for the locked method and real results, and `analysis_contracts/cell_type_marker_set_v1.tsv` for the marker panel). `GSE225857` remains blocked exactly as before.

## `GSE178318` — matrix, gene index, patient/sample annotation, and now cell-type split are all present

- `DATA/registry/GSE178318/source_manifest.tsv` and `file_inventory.tsv` record `GSE178318_barcodes.tsv.gz`, `GSE178318_genes.tsv.gz`, and `GSE178318_matrix.mtx.gz` (520.7 MB, 33,694 genes x 140,281 cells, SHA256-verified) as downloaded 2026-08-11. All three files are physically present (gitignored, never deleted) at `archive/phase2_fetal_state_track_v1/phase2/03_data/raw/GSE178318/`.
- `CEACAM5` (`ENSG00000105388`) is confirmed present in the gene index (row 31446 of `GSE178318_genes.tsv.gz`).
- `DATA/registry/GSE178318/sample_map.tsv` carries real patient/sample-level annotation for all 15 barcode groups.
- **Cell-type annotation**: `scripts/annotate_gse178318_cell_types.py` reads the locked matrix in a single streaming pass (166,681,072 entries, ~85s) and assigns each cell to `epithelial`/`immune`/`fibroblast`/`endothelial`/`Unassigned` by highest normalized marker-category score, per the locked marker panel. **This is marker-gene-score cell-compartment typing, not malignancy calling** — no CNV inference or matched-normal comparison distinguishes malignant from normal/reactive epithelium within these tumor-site specimens. Validated against the 3 `PBMC` samples (89.5-94.4% correctly typed immune, ~0% epithelial) before being trusted on tumor tissue. See `analysis_contracts/tgt_ceacam5.md` for the full results and every caveat.

## `GSE225857` — still genuinely no local processed data

- Unchanged from the previous version of this file: no raw or processed file for `GSE225857` exists anywhere on the machine that ran this pass. `DATA/registry/GSE225857/source_manifest.tsv` records most of its single-cell data as hosted at CNSA (`CNP0002540`/`CNP0003321`), with `access_status=SOURCE_INDEXED_REVIEW_REQUIRED` — CNSA access terms have not been independently reviewed (see `reports/PROJECT_STATUS.md`'s Next-handoff item on this). GEO itself only carries 8 GSM records for this series, not the full processed matrix.

## Both datasets remain `status=CANDIDATE`

Neither has been promoted to `APPROVED` in `DATA/registry/datasets.tsv`. Running the cell-typing analysis over `GSE178318`'s already-present, already-checksum-verified files is a real analysis step, not a new download — the same class of action the reviewing conversation explicitly endorsed as the recommended next step for this vertical slice.

## What would still unblock `GSE225857`

CNSA access-terms review, then a real fetch — not attempted in this pass, and not required to close the `GSE178318` half of this dossier.
