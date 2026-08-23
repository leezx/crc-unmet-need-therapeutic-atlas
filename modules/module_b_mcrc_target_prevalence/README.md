# Module B — MCRC_TARGET_PREVALENCE

## Goal

> **mCRC 里到底有没有足够多能被 X 地址访问的癌细胞？**

## Inputs

- `GSE225857` — 6 CRLM patients, 27 matched primary/LM/adjacent/PB samples, all preoperative chemo and/or RT, scRNA + spatial.
- `GSE178318` — matched primary + CRLM scRNA, 6 patients, 3 with preoperative chemo.
- Refractory/clinical bulk datasets registered under this module in `../../DATA/registry/module_classification.tsv`.

## Per-target output

For each candidate X from Module A:

- malignant-cell detection
- X-high fraction
- patient-positive fraction
- between-patient heterogeneity
- within-patient heterogeneity
- metastatic lesion coverage

## Naming rule

Bucket output as `RNA_no / RNA_low / RNA_high`. This can **never** be upgraded to `surface-density high` — not even by a completed Module D protein calibration. Module D only provides protein-level support/concordance (whole-tissue MS ≠ malignant-cell membrane density, PDO protein ≠ tumor surface density); a real surface-density claim requires a target-specific quantitative surface assay or equivalent direct evidence, which is neither `RNA_high` nor a Module D result. Record `evidence_directness` accordingly in `../../schemas/target_evidence.tsv` (`UNCALIBRATED_PROXY` for RNA alone, `CALIBRATED_PROXY` at best once Module D protein concordance exists, never `DIRECT` from this module).

## Cannot prove

scRNA ≠ surface density. Small cohorts (n=6) are within-cohort descriptive statistics, not population prevalence claims until replicated.

Output rows `target_id`-keyed per `../../schemas/target_evidence.tsv`.

## Status

First real target attempt (2026-08-23, corrected round 1 of PR #73's review): `tgt_ceacam5` (`CEACAM5`), paired with the Module E run on the same target. **Blocked, not run — but not on missing data for `GSE178318`.** See `question/tgt_ceacam5.md` and `data_lock/tgt_ceacam5.md` for the per-dataset detail the first version of this file got wrong: `GSE178318`'s processed matrix, gene index and patient/sample-level treatment annotation are all physically present locally (SHA256-verified, per this repository's own `DATA/registry/GSE178318/source_manifest.tsv`) and `CEACAM5` is confirmed present in its gene index — what's actually missing is malignant/epithelial cell-type annotation, a real analysis step not yet done for any target. `GSE225857` genuinely has no local processed data (most of it is CNSA-hosted, access terms unreviewed). Both remain `status=CANDIDATE` in `../../DATA/registry/datasets.tsv`. No `target_evidence.tsv` row was written for Module B — an honest gap, not a fabricated result. **No live QC/cell-typing script exists for GSE178318 right now** — the previous `qc_gse178318.py` did structural QC only (barcode reconciliation, no malignant-cell calling) and defaulted to the old Fig1 marker set; it has been archived, see `../../archive/phase2_fetal_state_track_v1/ARCHIVE_NOTE.md`. A fresh script would need a target-specific marker list as an explicit input and a reviewed cell-typing method, neither of which exists yet.
