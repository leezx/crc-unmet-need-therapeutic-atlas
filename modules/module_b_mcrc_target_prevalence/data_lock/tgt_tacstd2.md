# Module B data lock — `tgt_tacstd2`

Status: **`GSE178318` — LOCKED, QC-filtered, epithelial-proxy screened (NOT malignancy-confirmed). `GSE225857` — LOCKED, non-immune tumor-cell screen complete (2026-08-24, PR #81); its CNSA raw-sequencing route remains `CONTROLLED_ACCESS` but was never needed.**

## `GSE178318` — same locked matrix/gene index/sample annotation as prior targets, re-scored for `TACSTD2`

- Same checksum-verified raw files as `tgt_ceacam5.md` — no new download.
- `TACSTD2` (`ENSG00000184292`) confirmed present in the gene index under its current HGNC symbol.
- Same QC (123,330 of 140,281 barcodes pass, target-independent) and EPCAM-alone epithelial identification as prior targets.
- **Malignancy is NOT confirmed** for this pass — no CNV-based confirmation attempted for `TACSTD2` in this PR, same reasoning as `tgt_erbb2.md`.

## `GSE225857` — non-immune tumor-cell screen complete (2026-08-24, PR #81)

Method, pre-flight checks, and full results table: `tgt_ceacam5.md` and `analysis_contracts/gse225857_tumor_cell_screen.md` — same run, re-scored for `TACSTD2` (`target_evidence.tsv` `TE031`, `evidence.tsv` `EV039`). `TACSTD2` reaches `RNA_high` in exactly one of the 10 patient x site strata (`s0115` LC, n=55 tumor cells in that stratum — a small sample), `RNA_low` in the other 9 strata, never `RNA_no`. `access_status=CONTROLLED_ACCESS` for the CNSA raw-sequencing route is unchanged and was never needed for this result.

## Both datasets remain `status=CANDIDATE`

Unchanged from `tgt_ceacam5.md`.
