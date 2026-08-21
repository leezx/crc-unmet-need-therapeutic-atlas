# Module D — PROTEIN_AND_ENDPOINT

This is the layer the old (pre-pivot) Atlas was weakest on.

## Goal

> **把"漂亮的 RNA target"砍掉一大批。**

## Inputs

- `PXD055821` — 152 human CRLM, mass-spec proteomics + outcome.
- `PXD022613` — CRLM proteomics, resection→recurrence <12 vs >12 months (poor/good prognosis).
- `MCRC_liver_metastasis_PDO_2026` (mCRC PDO 2026 / Mendeley `hr94h42xdc.3`) — 213 CRLM PDOs / 102 patients, RNA + mutation + 14-marker mIHC + drug screen.
- HPA / CPTAC as supportive orthogonal protein layers (shared with Module E for HPA).

## Per-target output

- tumor protein evidence
- protein prevalence
- RNA↔protein concordance
- recurrence/PFS/OS association
- cross-platform consistency

## Cannot prove

Whole-tissue MS ≠ malignant-cell-specific membrane density. Association ≠ "removing X-high cells prevents recurrence." PDO protein ≠ tumor surface density; drug sensitivity ≠ ADC efficacy.

## Status

Not started. `PXD055821` and `PXD022613` are not yet in `../../DATA/registry/datasets.tsv` — add as `CANDIDATE` rows first. `MCRC_liver_metastasis_PDO_2026` is already `APPROVED`-track in the registry and can be reused directly once a target list exists.
