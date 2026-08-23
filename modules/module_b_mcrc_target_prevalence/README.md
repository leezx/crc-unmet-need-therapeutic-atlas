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

First real target result (2026-08-23): `tgt_ceacam5` (`CEACAM5`) against `GSE178318`, closing the vertical slice PR #73's own reviewer recommended finishing before running the other four CRC-precedented targets. New `../../scripts/annotate_gse178318_cell_types.py` does a marker-gene-score cell-compartment split (`analysis_contracts/cell_type_marker_set_v1.tsv`, 17 canonical markers) over the locked matrix — **not malignancy calling** (no CNV inference; "epithelial cell in a tumor-site specimen" is the closest available proxy for malignant epithelium, stated explicitly in every output). Validated against the 3 `PBMC` samples (89.5-94.4% correctly typed immune, ~0% epithelial) before trusting the tumor-tissue result. Result: 11 of 12 `PRIMARY_CRC`/`LIVER_METASTASIS` samples bucket `RNA_low`, one (`COL12_LM`) `RNA_high`, none `RNA_no` — every one of the 6 patients has a detectable CEACAM5-positive epithelial subpopulation in both primary and metastatic tissue, with substantial between-patient heterogeneity (12.8%-66.7%) and no consistent primary-to-LM direction (3-vs-3 split). One real `target_evidence.tsv` row (`TE004`, `evidence_directness=UNCALIBRATED_PROXY`), backed by `EV012`. See `question/tgt_ceacam5.md`, `data_lock/tgt_ceacam5.md`, `analysis_contracts/tgt_ceacam5.md` (full per-sample result TSV is gitignored, not committed — regenerable). `GSE225857` (this module's other `CORE_ACTIVE` dataset) remains genuinely blocked on CNSA access — this result covers `GSE178318` only, not the full module for this target.
