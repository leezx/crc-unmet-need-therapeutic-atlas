# Module B data lock — `tgt_ceacam5`

Status: **BLOCKED — required inputs not locally available, not authorized to fetch in this pass**

## What is required

Module B's naming rule (`../README.md`) requires per-cell malignant-epithelial-annotated scRNA data to compute `RNA_no/RNA_low/RNA_high`, X-high fraction, patient-positive fraction, and between/within-patient heterogeneity for `CEACAM5`. `GSE225857` and `GSE178318` are this module's two `CORE_ACTIVE`/`every_target` datasets (`DATA/registry/module_classification.tsv`) and the only registered datasets covering `mcrc_preop_chemotherapy_crlm`.

## Why this is blocked, not just slow

- Unlike Module E's normal-tissue bulk RNA (already-fetched local copies of HPA/GTEx, read via `config/external_sources.yaml`, no new download), **no processed scRNA expression matrix for `GSE225857` or `GSE178318` is present anywhere on the machine that ran this pass.** Their `DATA/registry/<id>/` directories hold only `source_manifest.tsv` / `file_inventory.tsv` / `no_file_inventory_disposition.tsv` metadata (Phase 1 source-verification artifacts), never expression values -- consistent with this repository's own "no biological data" policy.
- Both datasets remain `status=CANDIDATE` in `DATA/registry/datasets.tsv`. Per `CONTRIBUTING.md`, moving a dataset to `APPROVED` (the point at which real data would actually be fetched) requires a dataset directory and verifiable `source_manifest.tsv` already exist (both do) **and** explicit human review of priority/download scope -- this pass does not have that authorization, and fetching a bulk scRNA processed matrix on its own initiative would cross that gate rather than work within it.

## What would unblock this

A human-reviewed decision to promote `GSE225857` and/or `GSE178318` from `CANDIDATE` to `APPROVED` and authorize fetching their processed expression matrix (not raw FASTQ -- `GSE225857`'s single-cell data is largely hosted at CNSA, `CNP0002540`/`CNP0003321`, per its `source_manifest.tsv`, whose CNSA access terms are recorded as `SOURCE_INDEXED_REVIEW_REQUIRED` and not yet independently reviewed -- see `reports/PROJECT_STATUS.md`'s Next-handoff item on this). Until then, this file stands as the honest record of what Module B needs and why it hasn't run, rather than a fabricated or estimated `target_evidence.tsv` row.
