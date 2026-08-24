# Module B data lock — `tgt_tacstd2`

Status: **`GSE178318` — LOCKED, QC-filtered, epithelial-proxy screened (NOT malignancy-confirmed). `GSE225857` — still blocked on data access.**

## `GSE178318` — same locked matrix/gene index/sample annotation as prior targets, re-scored for `TACSTD2`

- Same checksum-verified raw files as `tgt_ceacam5.md` — no new download.
- `TACSTD2` (`ENSG00000184292`) confirmed present in the gene index under its current HGNC symbol.
- Same QC (123,330 of 140,281 barcodes pass, target-independent) and EPCAM-alone epithelial identification as prior targets.
- **Malignancy is NOT confirmed** for this pass — no CNV-based confirmation attempted for `TACSTD2` in this PR, same reasoning as `tgt_erbb2.md`.

## `GSE225857` — still genuinely no local processed data

Unchanged from `tgt_ceacam5.md`.

## Both datasets remain `status=CANDIDATE`

Unchanged from `tgt_ceacam5.md`.
