# Module C — REFRACTORY_PERSISTENCE

This is the module that most distinguishes this Atlas from a generic CRC Atlas.

## Goal

> **即使 target 在 CRC 中很高，到了真正要抢的 2/3L refractory patient 身上还剩多少？**

## Three axes, not one — do not collapse them

Round 3 review (2026-08-21) caught that a single `persistence` axis was itself a proxy-upgrade risk: several of these datasets are single-timepoint biopsies in refractory/treated tissue, not paired pre/post-treatment measurements, and labeling them `persistence` silently upgraded "still present in refractory disease" to "retained across treatment." The axis is split three ways instead:

**`longitudinal_persistence`** — a genuine paired pre/post-treatment measurement on the same patient/lesion. Only one dataset in this module actually qualifies:
- `GSE84267` — 2 mCRC patients, matched liver biopsy, pre-cetuximab → acquired resistance (`activation_context = ANTI_EGFR_REFRACTORY`).

**`refractory_or_treated_presence`** — single-timepoint presence of a candidate in treated/refractory/metastatic tissue. Real evidence, but it proves presence, not retention:
- `GSE274551` — refractory RAS-WT mCRC, 35 RNA-seq samples with PD/PR/SD clinical-response context (`activation_context = RAS_WT`). Per its official GEO design, this is a single baseline biopsy per patient (post-prior-anti-EGFR, pre-trial-treatment), not a pre/post pair.
- `GSE178318`, `GSE225857` — shared with Module B (matched primary/LM/adjacent/PB in preoperative-chemo patients). Cross-sectional primary-vs-metastasis comparison within treated patients, not a paired longitudinal design.
- `GSE294385` — macro-/micrometastatic presence, MRD/DFS/chemo-resistance context (`activation_context = MRD_RECURRENCE`, activate only after shortlist). Not a classic pre/post cohort either.

**`clinical_endpoint_context`** (added round 3 as well) — response-association only, no presence-vs-absence or persistence claim at all:
- `GSE196576` (CALGB-SWOG 80405, first-line, `activation_context = FIRST_LINE_VALIDATION`)
- `GSE235919` (first-line RAS-mutant, `activation_context = RAS_MUTANT`)
- `GSE5851` (pretreatment cetuximab-monotherapy response, `activation_context = ANTI_EGFR_REFRACTORY`)

Target-specific clinical literature (acquired-resistance, longitudinal/resistance papers — see Module F for the literature-extraction contract) can support any of the three axes depending on its actual design; classify by what was actually measured, not by which axis sounds strongest.

## Per-target output

`longitudinal_persistence`:
- acquired-resistance direction
- retention/loss across a real pre/post-treatment pair

`refractory_or_treated_presence`:
- presence/absence in refractory or treated-disease tissue
- primary→metastasis retention (cross-sectional)
- recurrent/micrometastatic lesion presence

`clinical_endpoint_context`:
- response/outcome association (not a presence or persistence claim)

Every output row records `adc_decision_axis` exactly as one of the three — never write a `refractory_or_treated_presence` or `clinical_endpoint_context` finding as if it were `longitudinal_persistence`.

## Cannot prove

`GSE84267` is n=2: paired within-patient direction only, never a population-level claim. `refractory_or_treated_presence` datasets prove presence in a treated/refractory state, not that treatment caused retention — a single baseline biopsy cannot distinguish "target was always there" from "target persisted through treatment." Response association in `GSE196576`, `GSE235919`, `GSE5851` (and in `GSE274551`'s outcome-association use) is not causality, and none of the `clinical_endpoint_context` cohorts (first-line/pretreatment) may be read as persistence or even as refractory-tissue presence.

## Status

Not started. `GSE274551`, `GSE84267`, `GSE178318`, `GSE225857` are registered `CANDIDATE` rows in `../../DATA/registry/datasets.tsv` with a minimal `source_manifest.tsv` (added 2026-08-21), but none have completed the Phase 1 source-verification workflow in `../../CONTRIBUTING.md` yet — that verification, not registry admission, is what still blocks any data lock here. Output rows must be `target_id x indication_id`-keyed per `../../schemas/target_evidence.tsv`.
