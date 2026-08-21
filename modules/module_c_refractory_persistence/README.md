# Module C — REFRACTORY_PERSISTENCE

This is the module that most distinguishes this Atlas from a generic CRC Atlas.

## Goal

> **即使 target 在 CRC 中很高，到了真正要抢的 2/3L refractory patient 身上还剩多少？**

## Inputs

- `GSE274551` — refractory RAS-WT mCRC, 35 RNA-seq samples with PD/PR/SD clinical-response context.
- `GSE84267` — 2 mCRC patients, matched liver biopsy, pre-cetuximab → acquired resistance.
- `GSE178318`, `GSE225857` — shared with Module B (treatment-exposed CRLM).
- Target-specific clinical literature (acquired-resistance, longitudinal/resistance papers — see Module F for the literature-extraction contract).

## Per-target output

- post-treatment persistence
- acquired-resistance direction
- primary→metastasis retention
- CRLM retention
- recurrent lesion retention

## Cannot prove

`GSE84267` is n=2: paired within-patient direction only, never a population-level claim. Response association in `GSE274551` is not causality.

## Status

Not started. `GSE274551` and `GSE84267` are not yet in `../../DATA/registry/datasets.tsv` — add as `CANDIDATE` rows and run the Phase 1 source-verification workflow in `../../CONTRIBUTING.md` before any data lock here.
