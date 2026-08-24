# Module B data lock — `tgt_f3`

Status: **`GSE178318` — LOCKED, QC-filtered, epithelial-proxy screened (NOT malignancy-confirmed). `GSE225857` — LOCKED, non-immune tumor-cell screen complete (2026-08-24, PR #81); its CNSA raw-sequencing route remains `CONTROLLED_ACCESS` but was never needed.**

## `GSE178318` — same locked matrix/gene index/sample annotation as `tgt_ceacam5`, re-scored for `F3`

- Same checksum-verified raw files as `tgt_ceacam5.md` — no new download.
- `F3` (`ENSG00000117525`) confirmed present in the gene index under its current HGNC symbol.
- Same QC (123,330 of 140,281 barcodes pass, target-independent) and EPCAM-alone epithelial identification as `tgt_ceacam5`/`tgt_erbb2`.
- **Malignancy is NOT confirmed** for this pass — no CNV-based confirmation attempted for `F3` in this PR, same reasoning as `tgt_erbb2.md`.

## `GSE225857` — non-immune tumor-cell screen complete (2026-08-24, PR #81)

Method, pre-flight checks, and full results table: `tgt_ceacam5.md` and `analysis_contracts/gse225857_tumor_cell_screen.md` — same run, re-scored for `F3` (`target_evidence.tsv` `TE029`, `evidence.tsv` `EV037`). `F3` reaches `RNA_no` in the two lowest-yield patients (`s0115` CC, `s0920` both sites), `RNA_low` elsewhere, never `RNA_high` in this cohort. `access_status=CONTROLLED_ACCESS` for the CNSA raw-sequencing route is unchanged and was never needed for this result.

## Both datasets remain `status=CANDIDATE`

Unchanged from `tgt_ceacam5.md`.
