# Module B data lock — `tgt_ceacam5`

Status: **BLOCKED on malignant/epithelial cell-type annotation, NOT on missing data**

Revised 2026-08-23 (PR #73 round 1 review): the first version of this file said "no processed scRNA expression matrix for `GSE225857` or `GSE178318` is present anywhere," which was wrong for `GSE178318` and contradicted this repository's own canonical `DATA/registry/GSE178318/source_manifest.tsv`. Corrected below, split per dataset since their actual states differ.

## `GSE178318` — matrix, gene index, and patient/sample annotation ARE present locally

- `DATA/registry/GSE178318/source_manifest.tsv` and `file_inventory.tsv` record `GSE178318_barcodes.tsv.gz`, `GSE178318_genes.tsv.gz`, and `GSE178318_matrix.mtx.gz` (520.7 MB, 33,694 genes x 140,281 cells, SHA256-verified) as downloaded 2026-08-11. All three files are physically present (gitignored, never deleted) at `archive/phase2_fetal_state_track_v1/phase2/03_data/raw/GSE178318/`.
- `CEACAM5` (`ENSG00000105388`) is confirmed present in the gene index (row 31446 of `GSE178318_genes.tsv.gz`) — checked directly, not assumed.
- `DATA/registry/GSE178318/sample_map.tsv` already carries real patient/sample-level annotation for all 15 barcode groups: `specimen_type` (`PRIMARY_CRC`/`LIVER_METASTASIS`/`PBMC`), `treatment_context` (`TREATMENT_NAIVE` vs `PREOPERATIVE_CHEMOTHERAPY`), and per-patient `regimen_context` (`CAPEOX_3_CYCLES`, `CAPEOX_4_CYCLES`, `FOLFOX_BEV_8_CYCLES` for the 3 treated patients; the other 3 patients are treatment-naive). The archived `GSE178318_QC.md` (2026-08-11 run) confirms all 140,281 barcodes were parsed and reconciled to these 15 patient/specimen keys.
- **What is actually missing**: per-cell malignant/epithelial-cell-type annotation. The archived QC report's own "Next gate" section is explicit that cell-level QC rules and malignant-cell labeling were never done — `data_lock_GSE178318.tsv`'s `inclusion_rule` for the matrix says "Use only after sample-level cell annotation and patient-level aggregation contract passes," and that has not happened. Computing an `RNA_no/RNA_low/RNA_high` bucket, X-high fraction or patient-positive fraction for `CEACAM5` requires knowing which of the 140,281 cells are malignant epithelium versus stroma/immune/other — that classification does not exist yet, for any target, not just this one.
- This is a real analysis task (cell-type calling from a locked expression matrix), not a data-access blocker. It has not been attempted in this pass — see "Not next" below for why.

## `GSE225857` — genuinely no local processed data

- Unlike `GSE178318`, no raw or processed file for `GSE225857` exists anywhere on the machine that ran this pass. `DATA/registry/GSE225857/source_manifest.tsv` records most of its single-cell data as hosted at CNSA (`CNP0002540`/`CNP0003321`), with `access_status=SOURCE_INDEXED_REVIEW_REQUIRED` — CNSA access terms have not been independently reviewed (see `reports/PROJECT_STATUS.md`'s Next-handoff item on this). GEO itself only carries 8 GSM records for this series, not the full processed matrix.

## Both datasets remain `status=CANDIDATE`

Neither has been promoted to `APPROVED` in `DATA/registry/datasets.tsv`. `GSE178318`'s files being physically present on this machine is a historical fact from the pre-pivot phase2 track, not a retroactive `APPROVED` designation — using them for a real target-level analysis (cell-type calling, not just structural QC) is still a real analysis decision this pass has not made, consistent with `CONTRIBUTING.md`'s review gate.

## What would unblock this

For `GSE178318`: a malignant/epithelial cell-type annotation pass over the locked matrix (real scRNA analysis work, e.g. marker-gene-based or reference-mapped cell typing), reviewed the same way the archived pre-pivot QC work was. For `GSE225857`: CNSA access-terms review, then a real fetch. Neither is attempted in this PR — per the reviewing conversation's own guidance, this round only requires the blocker itself to be described accurately, not resolved. No `target_evidence.tsv` row is written for Module B.
