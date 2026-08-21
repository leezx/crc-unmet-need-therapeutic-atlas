# Knowledge/review layer — source-only skeleton

This directory links clinical-indication ontology nodes to registry datasets without storing biological measurements or target conclusions.

**Target-first, as of 2026-08-21** (revised after web-ChatGPT review of PR #70, `REQUEST_CHANGES` items 1 and 3). The evidence chain here previously read `patient population → malignant cell state → surface target → functional dependency/payload vulnerability → normal-tissue therapeutic window`, which treats an unsupervised malignant-cell-state discovery step as a required intermediary between patient population and target. That framing is the old, now-archived Phase 2 fetal-state/plasticity direction (see `../archive/phase2_fetal_state_track_v1/ARCHIVE_NOTE.md`) and has been explicitly rejected as a required step. The current chain is:

`ADCdb-derisked target (Module A, external; gated by `derisking_tier`/`repurposing_status`) → mCRC evidence per axis and per territory (Modules B–F: prevalence, refractory_or_treated_presence, longitudinal_persistence, clinical_endpoint_context, protein/endpoint, normal-tissue risk, delivery proof, population proof) → KILL / HOLD / SHORTLIST decision for that target × indication → activate supplementary/mechanistic evidence (e.g. DepMap, spatial) only for a named residual uncertainty on an already-shortlisted target`

Malignant-cell state can still appear as one *input* to the prevalence/presence axes (e.g. "is this candidate detected in malignant cells vs adjacent normal") — it is no longer a mandatory discovery stage that has to run before a target exists.

**Two-table evidence model** (revised 2026-08-21, round 3 of the same PR #70 review). `schemas/evidence.tsv` and `schemas/indication_evidence_links.tsv` stay the **source/provenance object** layer — what a dataset's registry metadata plausibly indexes, `SOURCE_INDEXED_NOT_ANALYZED` until reviewed. Both now carry `target_id` (added round 2). The **canonical, target-level interpreted output** of Modules B–F is `schemas/target_evidence.tsv`, which does not just carry `target_id` but also:

- `indication_id`: the specific defined mCRC population/territory this finding applies to. The unit of a target dossier is `target_id x indication_id`, never a bare target — the same target can be `SHORTLIST` in one territory and `HOLD` in another.
- `measurement_layer` and `evidence_directness` (`DIRECT` / `CALIBRATED_PROXY` / `UNCALIBRATED_PROXY` / `UNKNOWN`): RNA, whole-tissue protein, IHC, surfaceome-capture, and a real quantitative surface assay are different measurement layers with different directness, not distinguishable only from claim text.
- `source_evidence_id` (nullable): points back to the raw `evidence.tsv` row when one exists.

The 8 existing `evidence.tsv` objects predate the pivot, are dataset-provenance-level (not target-specific), and keep `target_id = NA`; no `target_evidence.tsv` row exists yet for any real ADCdb target. See `schemas/target_seed.tsv` (Module A's `ADC_TARGET_SEED_UNIVERSE.tsv` input/admission contract) in the repository-root `schemas/` directory.

The initial ontology follows the architecture requirement that a CRC indication is defined by more than a cancer label: disease state, molecular context, treatment line/history and anatomy must remain explicit. That indication-level context is `target_evidence.tsv`'s `indication_id` field, not a separate discovery stage:

`indication_id (defined mCRC population/territory) x target_id x ADC decision axis (prevalence / refractory_or_treated_presence / longitudinal_persistence / clinical_endpoint_context / protein_endpoint / normal_tissue_risk / delivery_proof / population_proof) → measurement_layer + evidence_directness`

Current `indication_evidence_links.tsv` rows are `SOURCE_INDEXED_NOT_ANALYZED`. They indicate that a dataset is a plausible source for an evidence axis based on its registry metadata; they do not establish a biological claim, therapeutic window, target ranking or clinical efficacy.

Files:

- `schemas/clinical_indications.tsv`: seed indication ontology nodes.
- `schemas/evidence.tsv`: source-only evidence objects with claims, provenance, confidence, target_id and explicit review status (provenance layer, not the canonical Module B–F output).
- `schemas/indication_evidence_links.tsv`: source-level links from indication nodes to evidence objects, registry datasets and (now) target_id.
- `schemas/target_seed.tsv`: contract for Module A's external `ADC_TARGET_SEED_UNIVERSE.tsv` output, including the `derisking_tier`/`repurposing_status` admission gate (see `../config/external_sources.yaml`).
- `schemas/target_evidence.tsv`: canonical, target x indication-keyed interpreted-evidence contract for Module B–F output. This is where every real finding goes.

The seed source is the user-provided `Asset-Generation-OS-architecture.md`, especially the CRC clinical-indication ontology and evidence-chain sections. Any future claim must add a reviewed source span, evidence object and human-review status.

Current source-only evidence objects: 8, all pre-pivot and dataset-provenance-level (`target_id = NA`). DepMap 26Q1 is represented only at release level; its CRC subset and dependency results remain unmaterialized, and per `DATA/registry/module_classification.tsv` it is `SUPPLEMENT_FROZEN` (activate only per-target, after shortlist, for a named mechanistic question).
