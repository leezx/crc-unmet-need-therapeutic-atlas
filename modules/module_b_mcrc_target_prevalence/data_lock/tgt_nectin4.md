# Module B data lock — `tgt_nectin4`

Status: **`GSE178318` — LOCKED, QC-filtered, epithelial-proxy screened (NOT malignancy-confirmed). `GSE225857` — still blocked on data access.**

## `GSE178318` — same locked matrix/gene index/sample annotation as prior targets, re-scored for `NECTIN4` via its dataset-index alias `PVRL4`

- Same checksum-verified raw files as `tgt_ceacam5.md` — no new download.
- **`NECTIN4` is not present under its current symbol in this dataset's gene index.** `GSE178318_genes.tsv.gz` indexes `ENSG00000143217` (confirmed the correct, current Ensembl gene ID for `NECTIN4` via `DATA/1.Databases/HGNC_gene_id_mapping`) under the row label `PVRL4` — `NECTIN4`'s prior HGNC-approved symbol before a gene-symbol rename. This is a real property of this dataset's own (older) gene annotation, not a data-entry error in this repository.
- `scripts/annotate_gse178318_cell_types.py --gene PVRL4 --out modules/module_b_mcrc_target_prevalence/results/tgt_nectin4_cell_type_prevalence.tsv` was the actual invocation — `--gene NECTIN4` against this dataset would fail with "not in gene index" despite the gene genuinely being measured. `--out` was set explicitly so the output filename still matches this repository's `tgt_nectin4_*` convention rather than inheriting `tgt_pvrl4_*` from the `--gene` value.
- Same QC (123,330 of 140,281 barcodes pass, target-independent) and EPCAM-alone epithelial identification as prior targets.
- **Malignancy is NOT confirmed** for this pass — no CNV-based confirmation attempted for `NECTIN4` in this PR, same reasoning as `tgt_erbb2.md`.

## `GSE225857` — still genuinely no local processed data

Unchanged from `tgt_ceacam5.md`.

## Both datasets remain `status=CANDIDATE`

Unchanged from `tgt_ceacam5.md`.
