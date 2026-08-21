# CRC Unmet-Need Therapeutic Atlas — project status

更新时间：2026-08-21

This file describes current state only. The pre-pivot status (Phase 1 source-only + Phase 2 global fetal-state discovery, through PR #66) is preserved as a historical record at [`../archive/phase2_fetal_state_track_v1/PROJECT_STATUS_LEGACY_2026-08-11.md`](../archive/phase2_fetal_state_track_v1/PROJECT_STATUS_LEGACY_2026-08-11.md) — do not read it as current.

## Current stage: ADC Target Repurposing Atlas pivot (target-first)

Source: `Asset-Generation-OS-architecture.md` → `CRC-Atlas工业化重构`（用户手工备注）, 2026-08-21. This is a **scope pivot**, not a data loss: the repository's single task is now

`ADCdb-derisked target (Module A, gated by `derisking_tier`/`repurposing_status`, external) → mCRC evidence per axis and territory (Modules B–F, `target_id x indication_id`-keyed) → KILL / HOLD / SHORTLIST for that target × territory → supplementary/mechanistic evidence only for a named residual uncertainty on an already-shortlisted target`

— not the old `patient population → malignant cell state → surface target → functional dependency → normal-tissue window` chain, which required an unsupervised cell-state discovery step before a target could even exist. See [`../ADC_ATLAS_DATASET_CONTRACT.md`](../ADC_ATLAS_DATASET_CONTRACT.md), [`../modules/README.md`](../modules/README.md), and [`../knowledge/README.md`](../knowledge/README.md).

This is PR #70 (`pivot/adc-target-repurposing-atlas`), **merged into `main`** after four review rounds with web-ChatGPT (`CRC临床适应症地图` conversation, `Biotech ideas` project): `REQUEST_CHANGES` on rounds 1–3, `APPROVE` on round 4 (head `b00d7ec`). See "Review history" below.

## Current scale

- 32 registry candidates (19 pre-pivot + 13 added this pivot: `GSE274551`, `GSE225857`, `GSE84267`, `PXD055821`, `PXD022613`, `GSE196576`, `GSE294385`, `GSE235919`, `GSE235917`, `GSE5851`, `CSPA_PXD000589`, `CPTAC_COAD`, `HPA_CRC_cancer_tissue`). All still `status=CANDIDATE`; none of the 13 pivot-added candidates have completed Phase 1 source verification yet — their `source_manifest.tsv` records only the accession URL already cited in the architecture doc, nothing more.
- `DATA/registry/module_classification.tsv`: 34 rows (some datasets serve two modules, e.g. `GSE178318`/`GSE225857` serve both B and C) covering all 32 datasets, each with `module`, `activation_status`, `adc_decision_axis`, `activation_rule`, `activation_context` (added round 3), `default_execution_order` — validated by `scripts/validate_module_classification.py` against a controlled vocabulary, not just free-text `reason`. Module C's axis was `persistence` (round 1) → split into `persistence`/`clinical_endpoint_context` (round 3) → `persistence` retired entirely and split further into `longitudinal_persistence` (a real paired pre/post-treatment design — only `GSE84267` qualifies) and `refractory_or_treated_presence` (single-timepoint presence in treated/refractory tissue — `GSE274551`, `GSE178318`, `GSE225857`, `GSE294385`) (round 4), because a bare `persistence` label was itself a proxy-upgrade risk.
- `datasets.tsv`'s own `priority` column (`P0_DOWNLOAD` / `P1_DOWNLOAD` / `REFERENCE_ONLY`) is retained as **legacy Phase 1 download-priority metadata only**; it is not re-derived from the pivot and must not be read as an execution-priority signal — `module_classification.tsv` is canonical for that (see `CONTRIBUTING.md`).
- `schemas/target_seed.tsv` (round 3: gained `derisking_tier`/`repurposing_status` admission fields) and `schemas/target_evidence.tsv` (round 3: gained `indication_id`, `measurement_layer`, `evidence_directness`, `source_evidence_id`) are new, empty (header-only) contracts. `schemas/evidence.tsv` and `schemas/indication_evidence_links.tsv` gained a `target_id` column (round 2); all 8 existing rows are pre-pivot dataset-provenance evidence and keep `target_id = NA`.
- `config/external_sources.yaml` is new: Module A's two source locations and output contract are declared there via `path_env_var`, not hardcoded into prose docs.
- `archive/phase2_fetal_state_track_v1/` now holds the full old `phase2/` tree, 4 state-validation reports, 7 scripts (all of them — `qc_gse178318.py`, `apply_gse178318_qc.py`, and `audit_hpa_target_window.py` were moved here in round 2 after review caught that they still defaulted to the old Fig1 marker panel), and the pre-pivot `PROJECT_STATUS.md` body.

## Completed this pivot (rounds 1–4)

1. `ADC_ATLAS_DATASET_CONTRACT.md` — per-module allowed questions / forbidden claims / activation rules; round 3 added the Module A admission gate and the two-table evidence model description.
2. `modules/` — one working folder per Module B–F; admission language corrected to match canonical registry `status` (round 2); Module C's `persistence` vs `clinical_endpoint_context` split and Module B's surface-density boundary hardened (round 3).
3. `DATA/registry/module_classification.tsv` + `schemas/module_classification.tsv` + `scripts/validate_module_classification.py` — canonical execution-priority contract (round 2), extended round 3 with `activation_context` (names the actual RAS-mutant/RAS-WT/anti-EGFR/MRD/first-line territory instead of leaving it in free-text `reason`) and the `clinical_endpoint_context` axis.
4. `schemas/target_seed.tsv`, `schemas/target_evidence.tsv`, `target_id` on `schemas/evidence.tsv` / `schemas/indication_evidence_links.tsv`, `config/external_sources.yaml` (round 2) — round 3 makes the two-table model explicit (`evidence.tsv` = provenance object, `target_evidence.tsv` = canonical `target_id x indication_id`-keyed interpreted output, linked via `source_evidence_id`) and adds the Module A `derisking_tier`/`repurposing_status` admission gate.
5. Old fetal-state track fully archived: `phase2/`, its 4 reports, and all 7 of its scripts (round 2).
6. `.gitignore` restores the original `phase2/03_data/raw|processed|06_results` patterns in addition to the new archive paths (round 2).
7. `knowledge/README.md` rewritten target-first; the old mandatory malignant-cell-state evidence chain is retracted (round 2), then updated for the two-table model and `indication_id`-keyed dossiers (round 3).
8. Consistency fixes (round 3): `CSPA_PXD000589`'s `datasets.tsv` reason text now says Module F, not Module A/B; this file's candidate-count arithmetic corrected to 19+13; `config/project_completion.yaml`'s remaining-component name corrected to thirteen; Module D README's HPA_CRC_cancer_tissue file-inventory claim removed (it has none yet — only `MCRC_liver_metastasis_PDO_2026` does).
9. Module C's `persistence` axis retired and split into `longitudinal_persistence` (only `GSE84267` — the one genuine paired pre/post-treatment design) and `refractory_or_treated_presence` (`GSE274551`, `GSE178318`, `GSE225857`, `GSE294385` — single-timepoint presence in treated/refractory/metastatic tissue, which proves presence, not treatment-induced retention) (round 4). Module A's `B_PRECLINICAL_ADC` tier tightened to require a real preclinical ADC construct (in-vitro killing / in-vivo efficacy), not just antibody-internalization evidence — that alone now falls to `C_ANTIBODY_OR_BIOLOGY_ONLY` → `FUTURE` by default (round 4). "Next handoff" wording corrected: Modules B+E are the intentionally selected minimum first-pass slice, not "the two `CORE_ACTIVE`/`every_target` modules" — C and D also have `CORE_ACTIVE`/`every_target` rows (round 4).

## Current gates and limits

- None of the 13 pivot-added registry candidates have completed Phase 1 source verification (original publication, repository metadata, license, processed availability). Registry admission (a `source_manifest.tsv` existing) is not the same as verification.
- No Module (B–F) has a data lock or analysis contract yet — `modules/*/README.md` define scope only.
- `MCRC_liver_metastasis_PDO_2026`'s mIHC panel covers only 14 markers; Module D must do a `target_observable` coverage check per target before assuming RNA→protein calibration is available.
- `knowledge/` still has only the 8 pre-pivot, non-target-specific evidence objects; no `target_evidence.tsv` row exists yet for any real ADCdb target.
- Module A (`ADC_TARGET_SEED_UNIVERSE.tsv`) has not actually been produced against `schemas/target_seed.tsv` — the contract (including the `derisking_tier`/`repurposing_status` admission gate) exists, the seed universe file does not.

## Next handoff

Per the reviewing conversation's own framing: **13 new candidate source verification → Module A target input contract → target-first B–F execution, one target x indication at a time.** Concretely:

1. Complete Phase 1 source verification for the 13 pivot-added candidates.
2. Produce a first `ADC_TARGET_SEED_UNIVERSE.tsv` (even a small one) conforming to `schemas/target_seed.tsv`, sourced via `config/external_sources.yaml`, with `derisking_tier`/`repurposing_status` actually set (not left blank).
3. Take the first `target_id x indication_id` through Modules B and E first — the intentionally selected minimum first-pass vertical slice (**not** the only `CORE_ACTIVE`/`every_target` modules; C and D also have `CORE_ACTIVE`/`every_target` rows) — end to end, producing real `target_evidence.tsv` rows with `measurement_layer` and `evidence_directness` set, before building out C/D/F tooling.
4. Not next: reactivating any `SUPPLEMENT_FROZEN` dataset (DepMap, HTAN, CRLM-NMP, Perturb-seq, …) without a named target-specific uncertainty.

## Review history

- **PR #70, round 1** — Initial pivot commit. Web-ChatGPT review (`CRC临床适应症地图`, `Biotech ideas` project): `REQUEST_CHANGES`. Five blockers: (1) target-first existed only in prose, no `target_id` data model; (2) two conflicting dataset-priority sources (`module_classification.tsv` vs `datasets.tsv.priority`) with no schema/vocabulary on the new one; (3) this status file and `knowledge/README.md` still presented the old Phase 2 state as current; (4) `qc_gse178318.py` / `apply_gse178318_qc.py` / `audit_hpa_target_window.py` still carried the old Fig1 marker panel by default, and several module READMEs contradicted canonical registry status; (5) `.gitignore` dropped the legacy `phase2/03_data/raw` etc. patterns, an unnecessary data-leak risk for other checkouts. Three non-blocking suggestions: reclassify `CSPA_PXD000589` out of Module B, register a separate HPA cancer/CRC layer for Module D, flag the PDO's 14-marker mIHC coverage limit.
- **PR #70, round 2** — All five round-1 blockers and all three suggestions addressed. Web-ChatGPT review: `REQUEST_CHANGES` again, but explicitly confirmed the core pivot direction (target-first, old-track archival, canonical execution priority, external Module A reference, script cleanup) is now real, not surface patching. Five new items, all narrower/contract-level rather than architectural: (1) `target_evidence.tsv` didn't express target × patient-territory × evidence-directness — same target's evidence across different mCRC populations could get merged into one dossier, and RNA/protein/surface evidence could only be told apart by claim text; (2) Module C conflated `persistence` with plain `clinical_endpoint_context` (first-line/pretreatment response-association cohorts read as if they proved post-treatment persistence), and `activation_context=context_specific` had no machine-readable territory; (3) Module B's README implied Module D calibration alone could upgrade `RNA_high` to a surface-density claim, which Module D's own caveats already reject; (4) Module A's `target_seed.tsv` had no machine-readable admission rule for whether a target is even in active repurposing search; (5) a batch of consistency issues (candidate-count arithmetic, a stale `twelve_pivot_candidates` config key, an overclaimed file-inventory sentence, a stale Module A/B reason string, and a stale PR description).
- **PR #70, round 3** — All five round-2 items and all consistency issues addressed. Web-ChatGPT independently spot-checked GSE274551/GSE225857/GSE84267/PXD055821/PXD022613 against their official source records and found no problem with the candidate set itself; still `REQUEST_CHANGES`, but on two narrow scientific-semantics blockers plus one wording fix: (1) `GSE274551` (and, on inspection, `GSE178318`/`GSE225857`/`GSE294385`) was labeled `persistence`, but per official GEO design it/they are single-timepoint biopsies in refractory/treated tissue, not a paired pre/post-treatment measurement — only `GSE84267` actually is one; (2) `derisking_tier=B_PRECLINICAL_ADC`'s definition included "antibody-internalization evidence exists" on its own, which under-derisks a target relative to this Atlas's repurposing-first premise; (3) "Modules B and E (the two `CORE_ACTIVE`/`every_target` modules)" is factually wrong (C and D also have such rows) — should read as an intentional first-pass slice, not an exhaustive list. Reviewer's own stated bar: fixing these three closes the review with `APPROVE`, no further scope expansion.
- **PR #70, round 4** — All three round-3 items addressed: Module C's `persistence` axis retired and split into `longitudinal_persistence` / `refractory_or_treated_presence`; `B_PRECLINICAL_ADC` now requires a real preclinical ADC construct, not antibody-internalization alone; the Next-handoff wording corrected (see "Completed this pivot" item 9 above). Web-ChatGPT final review, head `b00d7ec`: **`APPROVE`**. No new blockers found; explicit note that this PR's job is the strategic pivot and execution contract, not starting real data analysis, and that job is now met. Merged.

## 权威项目记录

- [README.md](../README.md)：仓库目标、范围和 repository map
- [ADC_ATLAS_DATASET_CONTRACT.md](../ADC_ATLAS_DATASET_CONTRACT.md)：Module A-F 数据契约
- [modules/README.md](../modules/README.md)：模块工作目录索引
- [knowledge/README.md](../knowledge/README.md)：target-first evidence chain 和 schema
- [DATASET_REVIEW.md](DATASET_REVIEW.md)：Phase 1 候选、数据缺口和 stop condition
- [PHASE1_REVIEW_CHECKLIST.md](PHASE1_REVIEW_CHECKLIST.md)：逐候选 admission gate
- [PR_HISTORY.md](PR_HISTORY.md)：PR、网页版 ChatGPT 审核和合并记录
- [CHATGPT_CRC_CLINICAL_INDICATION_MAP_FEEDBACK.md](CHATGPT_CRC_CLINICAL_INDICATION_MAP_FEEDBACK.md)：外部审核反馈归档
- [updates/REVIEW_CHECKLIST.md](updates/REVIEW_CHECKLIST.md)：上游 pinned-target 漂移后的人工复核流程
- [P2_SAMPLE_METADATA.md](P2_SAMPLE_METADATA.md)：GSE178318 sample-level treatment/pairing reconciliation
- [PXD038149_SAMPLE_METADATA_GATE.tsv](PXD038149_SAMPLE_METADATA_GATE.tsv)：PXD038149 workbook staging and sample-metadata gate
- [SOURCE_ONLY_FINAL_AUDIT.tsv](SOURCE_ONLY_FINAL_AUDIT.tsv)：无生物数据边界审计结果
- `DATA/registry/*/no_file_inventory_disposition.tsv`：显式不主张 file-level inventory 的 source-only 处置
- [../archive/phase2_fetal_state_track_v1/PROJECT_STATUS_LEGACY_2026-08-11.md](../archive/phase2_fetal_state_track_v1/PROJECT_STATUS_LEGACY_2026-08-11.md)：pre-pivot status, historical only
