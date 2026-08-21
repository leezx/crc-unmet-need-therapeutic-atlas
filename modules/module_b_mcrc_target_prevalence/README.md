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

Bucket output as `RNA_no / RNA_low / RNA_high`. Never write `surface-density high` — that requires Module D protein calibration first.

## Cannot prove

scRNA ≠ surface density. Small cohorts (n=6) are within-cohort descriptive statistics, not population prevalence claims until replicated.

Output rows `target_id`-keyed per `../../schemas/target_evidence.tsv`.

## Status

Not started. First step is a data lock + analysis contract under `analysis_contracts/`, following the same review discipline as the archived `phase2/03_data/data_lock_v0.md` / `phase2/04_analysis_contracts/` pattern — but scoped to per-target prevalence, not a global cell-state discovery question. **No live QC script exists for GSE178318 right now** — the previous `qc_gse178318.py` defaulted to the old Fig1 marker set and has been archived; see `../../archive/phase2_fetal_state_track_v1/ARCHIVE_NOTE.md`. A fresh script must take a target-specific marker list as an explicit input, not a hardcoded constant.
