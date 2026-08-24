# Module B data lock — `tgt_f3`

Status: **`GSE178318` — LOCKED, QC-filtered, epithelial-proxy screened (NOT malignancy-confirmed). `GSE225857` — still blocked on data access.**

## `GSE178318` — same locked matrix/gene index/sample annotation as `tgt_ceacam5`, re-scored for `F3`

- Same checksum-verified raw files as `tgt_ceacam5.md` — no new download.
- `F3` (`ENSG00000117525`) confirmed present in the gene index under its current HGNC symbol.
- Same QC (123,330 of 140,281 barcodes pass, target-independent) and EPCAM-alone epithelial identification as `tgt_ceacam5`/`tgt_erbb2`.
- **Malignancy is NOT confirmed** for this pass — no CNV-based confirmation attempted for `F3` in this PR, same reasoning as `tgt_erbb2.md`.

## `GSE225857` — still genuinely no local processed data

Unchanged from `tgt_ceacam5.md`.

## Both datasets remain `status=CANDIDATE`

Unchanged from `tgt_ceacam5.md`.
