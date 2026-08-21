# Module C — REFRACTORY_PERSISTENCE

This is the module that most distinguishes this Atlas from a generic CRC Atlas.

## Goal

> **即使 target 在 CRC 中很高，到了真正要抢的 2/3L refractory patient 身上还剩多少？**

## Inputs

**`persistence` axis** (paired/longitudinal, actually measures post-treatment retention): `GSE274551` — refractory RAS-WT mCRC, 35 RNA-seq samples with PD/PR/SD clinical-response context (`activation_context = RAS_WT`). `GSE84267` — 2 mCRC patients, matched liver biopsy, pre-cetuximab → acquired resistance (`activation_context = ANTI_EGFR_REFRACTORY`). `GSE178318`, `GSE225857` — shared with Module B (treatment-exposed CRLM). `GSE294385` — MRD/micrometastatic retention (`activation_context = MRD_RECURRENCE`, activate only after shortlist).

**`clinical_endpoint_context` axis** (response-association only, added 2026-08-21 round 3 — distinct from `persistence` because none of these are a paired pre/post-treatment design): `GSE196576` (CALGB-SWOG 80405, first-line, `activation_context = FIRST_LINE_VALIDATION`), `GSE235919` (first-line RAS-mutant, `activation_context = RAS_MUTANT`), `GSE5851` (pretreatment cetuximab-monotherapy response, `activation_context = ANTI_EGFR_REFRACTORY`). These support a target/response association claim; they do **not** support a persistence claim.

Target-specific clinical literature (acquired-resistance, longitudinal/resistance papers — see Module F for the literature-extraction contract).

## Per-target output

`persistence` axis:
- post-treatment persistence
- acquired-resistance direction
- primary→metastasis retention
- CRLM retention
- recurrent lesion retention

`clinical_endpoint_context` axis:
- response/outcome association (not a persistence direction)

Every output row records `adc_decision_axis` exactly as `persistence` or `clinical_endpoint_context` — never write a `clinical_endpoint_context` finding as if it were `persistence`.

## Cannot prove

`GSE84267` is n=2: paired within-patient direction only, never a population-level claim. Response association in `GSE274551`, `GSE196576`, `GSE235919`, `GSE5851` is not causality, and none of the `clinical_endpoint_context` cohorts (first-line/pretreatment) may be read as post-treatment persistence.

## Status

Not started. `GSE274551`, `GSE84267`, `GSE178318`, `GSE225857` are registered `CANDIDATE` rows in `../../DATA/registry/datasets.tsv` with a minimal `source_manifest.tsv` (added 2026-08-21), but none have completed the Phase 1 source-verification workflow in `../../CONTRIBUTING.md` yet — that verification, not registry admission, is what still blocks any data lock here. Output rows must be `target_id`-keyed per `../../schemas/target_evidence.tsv`.
