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

**Second pass, 2026-08-25 (`ERBB2` only).** `MCRC_liver_metastasis_PDO_2026`'s `Data S3.xlsx` (114.6 KB) downloaded and checksummed — source-provided processed per-PDO mIHC values for `ERBB2` (the only one of the five `A_CLINICAL` targets in this dataset's 14-marker panel). **Carries a critical caveat, worded exactly as the source states it, not clean corroboration**: the source publication's own methods text states, verbatim, that `ERBB2` "was excluded from analysis due to ... very low expression levels" (`KRT7`, the panel's other excluded marker, was excluded for "no expression" — a different reason, per the source text's own "respectively") — excluded from downstream analyses of this specific multiplex panel (polyclonal antibody, catalog `A0485`), not the whole paper. This repository does not characterize that as "reagent failure" or "assay noise" — the source publication makes neither claim, and this repository cannot determine whether it reflects true low `ERBB2` protein abundance, an assay-sensitivity limit, or both. See `analysis_contracts/pdo_erbb2_mihc.md` and `data_lock/tgt_erbb2.md` for the full caveat, which must accompany every use of this evidence, worded this precisely. One new `target_evidence.tsv` row (`TE042`, `evidence_level=EXPLORATORY_UNDERPOWERED`, `confidence=LOW`).

- `PXD055821`: raw `.raw`/`.pdResult`/`.msf` files are not usable in this environment (no proteomics search-engine software available) — but the project's own small, already-processed DIA-NN gene-group matrix (its 60 columns are the project's own "Sydney cohort" — 60 specimens from 51 patients, independently confirmed against the publication's own text, not 60 independent patients) gives real, gene-symbol-indexed protein abundance for all five targets.
- `HPA_CRC_cancer_tissue`: the classic HPA "Pathology Atlas" `cancer_data.tsv.zip` gives real colorectal-cancer-specific IHC data for all five targets — a cancer-cell-focused staining category (HPA's own methodology: intensity + fraction of positive cancer cells, not a bulk whole-section score), still not membrane-specific or quantitative, distinct from `HPA_normal_tissue` (Module E only).
- `PXD022613` — investigated and **deprioritized**: its only usable output would require downloading an 867 MB RAR archive (no partial-extraction path over HTTP; RAR has no central directory) purely to reach a likely `proteinGroups.txt`, and its own published supplementary "significantly expressed proteins" table (99 proteins) does not include any of the five `A_CLINICAL` targets. Not pursued further unless a future environment permits the ~900MB download or a processed table becomes available another way.
- `MCRC_liver_metastasis_PDO_2026`'s `Data S3.xlsx` (14-marker mIHC panel) — only `ERBB2` is among the 14 markers (`ABCB1`/`ABCG2`/`CDH1`/`CDX2`/`CFTR`/`ERBB2`/`HSF1`/`KI67`/`KRT20`/`KRT7`/`RCC2`/`RIPK1`/`TP53`/`UGT1A`), so not usable as a primary Module D source for the other four targets; real per-sample `ERBB2` mIHC data is now downloaded, checksummed, and incorporated into `target_evidence.tsv` (`TE042`) — with the reliability caveat above.
- `CPTAC_COAD` remains `SUPPLEMENT` / `after_shortlist_named_uncertainty` — not activated in this pass.

**`ERBB2`/`TACSTD2` MS-vs-IHC discrepancy investigation, 2026-08-25 (revised in round 1 review of PR #86).** Per Next-handoff item `3e(a)`: `analysis_contracts/erbb2_tacstd2_ms_ihc_discrepancy.md` investigates why `PXD055821` MS (frequent nonzero detection) and `HPA_CRC_cancer_tissue` IHC (mostly `Low`/`Not detected`) disagree for these two targets. **Does not resolve it.** Cohort composition (`PXD055821` is liver-metastasis-specific, HPA's cohort is not documented as such) stays genuinely unresolved — HPA's own documentation doesn't publish primary-vs-metastatic cohort composition for its cancer atlas. HPA antibody attribution was investigated and corrected: HPA's colorectal-cancer pathology pages DO expose per-antibody staining tallies, and independently re-parsing them found `TE038`'s vector (ERBB2, n=11) exactly matches antibody `CAB020416`'s own tally, and `TE041`'s vector (TACSTD2, n=12) exactly matches `HPA043104`'s — though `cancer_data.tsv`'s own antibody-selection rule for that single aggregate row is not independently confirmed. New `scripts/analyze_pxd055821_abundance_percentile.py` computes `ERBB2`/`TACSTD2`'s same-matrix DIA-NN signal-rank (35th/45th percentile of median intensity among the matrix's 9,263 genes) — reported strictly as an **assay-internal signal-rank descriptor, not a calibrated cross-protein biological-abundance claim** (this repository's own Module D contract already forbids treating raw DIA-NN intensity as cross-protein-comparable, even within one matrix). No `target_evidence.tsv` field changes; TE033/TE036/TE038/TE041 notes cross-reference this file.

None of the datasets in this module is `APPROVED` — the canonical registry `status` for every dataset here is `CANDIDATE`, and this pass does not change that.
