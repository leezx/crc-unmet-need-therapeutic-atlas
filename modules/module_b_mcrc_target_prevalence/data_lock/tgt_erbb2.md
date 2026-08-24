# Module B data lock — `tgt_erbb2`

Status: **`GSE178318` — LOCKED, QC-filtered, epithelial-proxy screened (NOT malignancy-confirmed). `GSE225857` — LOCKED, non-immune tumor-cell screen complete (2026-08-24, PR #81); its CNSA raw-sequencing route remains `CONTROLLED_ACCESS` but was never needed.**

## `GSE178318` — same locked matrix/gene index/sample annotation as `tgt_ceacam5`, re-scored for `ERBB2`

- Same checksum-verified `GSE178318_barcodes.tsv.gz`/`GSE178318_genes.tsv.gz`/`GSE178318_matrix.mtx.gz` as `tgt_ceacam5.md` — no new download.
- `ERBB2` (`ENSG00000141736`) confirmed present in the gene index under its current HGNC symbol.
- Same `DATA/registry/GSE178318/sample_map.tsv` patient/sample annotation.
- **QC**: identical paper-aligned operationalization as `tgt_ceacam5` (`scripts/annotate_gse178318_cell_types.py`, unchanged): 123,330 of 140,281 barcodes pass — this is a QC pass over the matrix itself, not target-dependent, so the count is identical across all targets scored against this dataset.
- **Epithelial-proxy identification**: EPCAM alone, unchanged, same identification across all targets — only the target-gene positivity readout differs.
- **Malignancy is NOT confirmed** for this pass, same as `tgt_ceacam5` before its CNV-lite attempt (PR #75) — no CNV-based confirmation attempted for `ERBB2` in this PR (see `reports/PROJECT_STATUS.md`'s Next handoff on why: `tgt_ceacam5`'s own CNV-lite reviewer recommended against repeating that method per-target before deciding whether a higher-power method is worth investing in).

## `GSE225857` — still genuinely no local processed data

Method, pre-flight checks, and full results table: `tgt_ceacam5.md` and `analysis_contracts/gse225857_tumor_cell_screen.md` — same run, re-scored for `ERBB2` (`target_evidence.tsv` `TE028`, `evidence.tsv` `EV036`). `ERBB2` is the flattest of the five targets in this cohort: every patient x site cell buckets `RNA_low` (7.3%-30.9%), never `RNA_high` or `RNA_no` — a consistently mid-range detection pattern across all 5 patients and both sites, unlike `CEACAM5`'s wide spread. `access_status=CONTROLLED_ACCESS` for the CNSA raw-sequencing route is unchanged and was never needed for this result.

## Both datasets remain `status=CANDIDATE`

Unchanged from `tgt_ceacam5.md` — running the QC/epithelial-proxy analysis over `GSE178318`'s already-present, already-checksum-verified files is a real analysis step, not a new download, and does not promote either dataset to `APPROVED`.
