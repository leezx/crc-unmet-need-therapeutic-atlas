# Module D — PROTEIN_AND_ENDPOINT

This is the layer the old (pre-pivot) Atlas was weakest on.

## Goal

> **把"漂亮的 RNA target"砍掉一大批。**

## Inputs

- `PXD055821` — 152 human CRLM, mass-spec proteomics + outcome.
- `PXD022613` — CRLM proteomics, resection→recurrence <12 vs >12 months (poor/good prognosis).
- `MCRC_liver_metastasis_PDO_2026` (mCRC PDO 2026 / Mendeley `hr94h42xdc.3`) — 213 CRLM PDOs / 102 patients, RNA + mutation + 14-marker mIHC + drug screen. **The mIHC panel covers only 14 markers.** Before activating protein analysis for any given target, first do a `target_observable` coverage check against that panel — do not assume RNA→protein calibration is available by default for an arbitrary ADCdb target.
- `HPA_CRC_cancer_tissue` — HPA colorectal-cancer tumor IHC + CPTAC-MS layer (added 2026-08-21; distinct dataset from `HPA_normal_tissue`, which only serves Module E).
- `CPTAC_COAD` as a supplementary orthogonal check (primary, not metastatic — see `../../DATA/registry/module_classification.tsv`).

## Per-target output

- tumor protein evidence
- protein prevalence
- RNA↔protein concordance
- recurrence/PFS/OS association
- cross-platform consistency

All rows `target_id`-keyed per `../../schemas/target_evidence.tsv`.

## Cannot prove

Whole-tissue MS ≠ malignant-cell-specific membrane density. Association ≠ "removing X-high cells prevents recurrence." PDO protein ≠ tumor surface density; drug sensitivity ≠ ADC efficacy.

## Status

Not started. `PXD055821`, `PXD022613`, and `HPA_CRC_cancer_tissue` are registered `CANDIDATE` rows with only a minimal `source_manifest.tsv` + `no_file_inventory_disposition.tsv` (added 2026-08-21) — no actual file inventory yet — and none have completed Phase 1 source verification. `MCRC_liver_metastasis_PDO_2026` is the one dataset in this module with an existing `file_inventory.tsv`, further along than most other candidates; that is still not `APPROVED` — the canonical registry `status` for every dataset in this module is `CANDIDATE`, and none should be described as approved.
