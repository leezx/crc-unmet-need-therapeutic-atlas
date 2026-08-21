# Knowledge/review layer — source-only skeleton

This directory links clinical-indication ontology nodes to registry datasets without storing biological measurements or target conclusions.

**Target-first, as of 2026-08-21** (revised after web-ChatGPT review of PR #70, `REQUEST_CHANGES` items 1 and 3). The evidence chain here previously read `patient population → malignant cell state → surface target → functional dependency/payload vulnerability → normal-tissue therapeutic window`, which treats an unsupervised malignant-cell-state discovery step as a required intermediary between patient population and target. That framing is the old, now-archived Phase 2 fetal-state/plasticity direction (see `../archive/phase2_fetal_state_track_v1/ARCHIVE_NOTE.md`) and has been explicitly rejected as a required step. The current chain is:

`ADCdb-derisked target (Module A, external) → mCRC evidence per axis (Modules B–F: prevalence, persistence, protein/endpoint, normal-tissue risk, delivery proof, population proof) → KILL / HOLD / SHORTLIST decision → activate supplementary/mechanistic evidence (e.g. DepMap, spatial) only for a named residual uncertainty on an already-shortlisted target`

Malignant-cell state can still appear as one *input* to the prevalence/persistence axes (e.g. "is this candidate detected in malignant cells vs adjacent normal") — it is no longer a mandatory discovery stage that has to run before a target exists.

Every evidence object and link now carries a `target_id` (added 2026-08-21, see `schemas/evidence.tsv` and `schemas/indication_evidence_links.tsv`) so results can be retrieved and aggregated by target, not only by indication or by gene names appearing in claim text. The 8 existing evidence objects predate the pivot and are dataset-provenance-level, not target-specific, so they keep `target_id = NA`; any new evidence object tied to a specific ADCdb target must set it. See `schemas/target_seed.tsv` (Module A's `ADC_TARGET_SEED_UNIVERSE.tsv` input contract) and `schemas/target_evidence.tsv` (the canonical target-level evidence contract Modules B–F should populate going forward) in the repository-root `schemas/` directory.

The initial ontology follows the architecture requirement that a CRC indication is defined by more than a cancer label: disease state, molecular context, treatment line/history and anatomy must remain explicit. That indication-level context is still tracked, now alongside (not instead of) the target axis:

`patient population/indication context ↔ target_id ↔ ADC decision axis (prevalence / persistence / protein_endpoint / normal_tissue_risk / delivery_proof / population_proof)`

Current links are `SOURCE_INDEXED_NOT_ANALYZED`. They indicate that a dataset is a plausible source for an evidence axis based on its registry metadata; they do not establish a biological claim, therapeutic window, target ranking or clinical efficacy.

Files:

- `schemas/clinical_indications.tsv`: seed indication ontology nodes.
- `schemas/evidence.tsv`: source-only evidence objects with claims, provenance, confidence, target_id and explicit review status.
- `schemas/indication_evidence_links.tsv`: source-level links from indication nodes to evidence objects, registry datasets and (now) target_id.
- `schemas/target_seed.tsv`: contract for Module A's external `ADC_TARGET_SEED_UNIVERSE.tsv` output (see `../config/external_sources.yaml`).
- `schemas/target_evidence.tsv`: canonical target-level evidence contract for Module B–F output.

The seed source is the user-provided `Asset-Generation-OS-architecture.md`, especially the CRC clinical-indication ontology and evidence-chain sections. Any future claim must add a reviewed source span, evidence object and human-review status.

Current source-only evidence objects: 8, all pre-pivot and dataset-provenance-level (`target_id = NA`). DepMap 26Q1 is represented only at release level; its CRC subset and dependency results remain unmaterialized, and per `DATA/registry/module_classification.tsv` it is `SUPPLEMENT_FROZEN` (activate only per-target, after shortlist, for a named mechanistic question).
