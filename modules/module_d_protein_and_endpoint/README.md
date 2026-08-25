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

**First real pass, 2026-08-25.** `PXD055821` and `HPA_CRC_cancer_tissue` now have real file-level inventories and real, checksummed evidence for all five `A_CLINICAL` targets — see `data_lock/tgt_ceacam5.md` (canonical) and `analysis_contracts/pxd055821_protein_abundance.md`/`analysis_contracts/hpa_cancer_ihc.md` for the full method and results. 10 new `target_evidence.tsv` rows (`TE032`-`TE041`), all `evidence_directness=UNCALIBRATED_PROXY`.

- `PXD055821`: raw `.raw`/`.pdResult`/`.msf` files are not usable in this environment (no proteomics search-engine software available) — but the project's own small, already-processed DIA-NN gene-group matrix (its 60 columns are the project's own "Sydney cohort" — 60 specimens from 51 patients, independently confirmed against the publication's own text, not 60 independent patients) gives real, gene-symbol-indexed protein abundance for all five targets.
- `HPA_CRC_cancer_tissue`: the classic HPA "Pathology Atlas" `cancer_data.tsv.zip` gives real colorectal-cancer-specific IHC data for all five targets — a cancer-cell-focused staining category (HPA's own methodology: intensity + fraction of positive cancer cells, not a bulk whole-section score), still not membrane-specific or quantitative, distinct from `HPA_normal_tissue` (Module E only).
- `PXD022613` — investigated and **deprioritized**: its only usable output would require downloading an 867 MB RAR archive (no partial-extraction path over HTTP; RAR has no central directory) purely to reach a likely `proteinGroups.txt`, and its own published supplementary "significantly expressed proteins" table (99 proteins) does not include any of the five `A_CLINICAL` targets. Not pursued further unless a future environment permits the ~900MB download or a processed table becomes available another way.
- `MCRC_liver_metastasis_PDO_2026`'s Data S3 (14-marker mIHC panel) was checked: only `ERBB2` is among the 14 markers (`ABCB1`/`ABCG2`/`CDH1`/`CDX2`/`CFTR`/`ERBB2`/`HSF1`/`KI67`/`KRT20`/`KRT7`/`RCC2`/`RIPK1`/`TP53`/`UGT1A`) — not usable as a primary Module D source for the other four targets, but real per-sample `ERBB2` mIHC data was downloaded and could serve as secondary corroboration if needed later; not yet incorporated into `target_evidence.tsv`.
- `CPTAC_COAD` remains `SUPPLEMENT` / `after_shortlist_named_uncertainty` — not activated in this pass.

None of the datasets in this module is `APPROVED` — the canonical registry `status` for every dataset here is `CANDIDATE`, and this pass does not change that.
