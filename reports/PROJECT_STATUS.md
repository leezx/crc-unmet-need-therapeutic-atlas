# CRC Unmet-Need Therapeutic Atlas — project status

更新时间：2026-08-21

This file describes current state only. The pre-pivot status (Phase 1 source-only + Phase 2 global fetal-state discovery, through PR #66) is preserved as a historical record at [`../archive/phase2_fetal_state_track_v1/PROJECT_STATUS_LEGACY_2026-08-11.md`](../archive/phase2_fetal_state_track_v1/PROJECT_STATUS_LEGACY_2026-08-11.md) — do not read it as current.

## Current stage: ADC Target Repurposing Atlas pivot (target-first)

Source: `Asset-Generation-OS-architecture.md` → `CRC-Atlas工业化重构`（用户手工备注）, 2026-08-21. This is a **scope pivot**, not a data loss: the repository's single task is now

`ADCdb-derisked target (Module A, external) → mCRC evidence per axis (Modules B–F) → KILL / HOLD / SHORTLIST → supplementary/mechanistic evidence only for a named residual uncertainty on an already-shortlisted target`

— not the old `patient population → malignant cell state → surface target → functional dependency → normal-tissue window` chain, which required an unsupervised cell-state discovery step before a target could even exist. See [`../ADC_ATLAS_DATASET_CONTRACT.md`](../ADC_ATLAS_DATASET_CONTRACT.md), [`../modules/README.md`](../modules/README.md), and [`../knowledge/README.md`](../knowledge/README.md).

This is PR #70 (`pivot/adc-target-repurposing-atlas`), currently in its **second commit round** after web-ChatGPT review (`CRC临床适应症地图` conversation, `Biotech ideas` project) returned `REQUEST_CHANGES` on the first round. See "Review history" below.

## Current scale

- 32 registry candidates (20 pre-pivot + 12 added this pivot: `GSE274551`, `GSE225857`, `GSE84267`, `PXD055821`, `PXD022613`, `GSE196576`, `GSE294385`, `GSE235919`, `GSE235917`, `GSE5851`, `CSPA_PXD000589`, `CPTAC_COAD`, `HPA_CRC_cancer_tissue`). All still `status=CANDIDATE`; none of the 13 pivot-added candidates have completed Phase 1 source verification yet — their `source_manifest.tsv` records only the accession URL already cited in the architecture doc, nothing more.
- `DATA/registry/module_classification.tsv`: 34 rows (some datasets serve two modules, e.g. `GSE178318`/`GSE225857` serve both B and C) covering all 32 datasets, each with `module`, `activation_status`, `adc_decision_axis`, `activation_rule`, `default_execution_order` — validated by `scripts/validate_module_classification.py` against a controlled vocabulary, not just free-text `reason`.
- `datasets.tsv`'s own `priority` column (`P0_DOWNLOAD` / `P1_DOWNLOAD` / `REFERENCE_ONLY`) is retained as **legacy Phase 1 download-priority metadata only**; it is not re-derived from the pivot and must not be read as an execution-priority signal — `module_classification.tsv` is canonical for that (see `CONTRIBUTING.md`).
- `schemas/target_seed.tsv` and `schemas/target_evidence.tsv` are new, empty (header-only) contracts. `schemas/evidence.tsv` and `schemas/indication_evidence_links.tsv` gained a `target_id` column; all 8 existing rows are pre-pivot dataset-provenance evidence and keep `target_id = NA`.
- `config/external_sources.yaml` is new: Module A's two source locations and output contract are declared there via `path_env_var`, not hardcoded into prose docs.
- `archive/phase2_fetal_state_track_v1/` now holds the full old `phase2/` tree, 4 state-validation reports, 7 scripts (all of them — `qc_gse178318.py`, `apply_gse178318_qc.py`, and `audit_hpa_target_window.py` were moved here in round 2 after review caught that they still defaulted to the old Fig1 marker panel), and the pre-pivot `PROJECT_STATUS.md` body.

## Completed this pivot (round 1 + round 2 fixes)

1. `ADC_ATLAS_DATASET_CONTRACT.md` — per-module allowed questions / forbidden claims / activation rules.
2. `modules/` — one working folder per Module B–F, admission language corrected to match canonical registry `status` (round 2).
3. `DATA/registry/module_classification.tsv` + `schemas/module_classification.tsv` + `scripts/validate_module_classification.py` — single canonical execution-priority contract, machine-checkable (round 2; round 1 shipped the file without a schema/validator/controlled vocabulary).
4. `schemas/target_seed.tsv`, `schemas/target_evidence.tsv`, `target_id` added to `schemas/evidence.tsv` / `schemas/indication_evidence_links.tsv`, `config/external_sources.yaml` — target-first is now a data model, not just prose (round 2).
5. Old fetal-state track fully archived: `phase2/`, its 4 reports, and now all 7 of its scripts (round 2 correction — 3 were incorrectly left live in round 1).
6. `.gitignore` restores the original `phase2/03_data/raw|processed|06_results` patterns in addition to the new archive paths, so any other existing checkout with local biological files at the old path stays protected (round 2).
7. `knowledge/README.md` rewritten target-first; the old mandatory malignant-cell-state evidence chain is retracted (round 2).

## Current gates and limits

- None of the 13 pivot-added registry candidates have completed Phase 1 source verification (original publication, repository metadata, license, processed availability). Registry admission (a `source_manifest.tsv` existing) is not the same as verification.
- No Module (B–F) has a data lock or analysis contract yet — `modules/*/README.md` define scope only.
- `MCRC_liver_metastasis_PDO_2026`'s mIHC panel covers only 14 markers; Module D must do a `target_observable` coverage check per target before assuming RNA→protein calibration is available.
- `knowledge/` still has only the 8 pre-pivot, non-target-specific evidence objects; no `target_evidence.tsv` row exists yet for any real ADCdb target.
- Module A (`ADC_TARGET_SEED_UNIVERSE.tsv`) has not actually been produced against `schemas/target_seed.tsv` — the contract exists, the seed universe file does not.

## Next handoff

Per the reviewing conversation's own framing: **12 new candidate source verification → Module A target input contract → target-first B–F execution.** Concretely:

1. Complete Phase 1 source verification for the 13 pivot-added candidates.
2. Produce a first `ADC_TARGET_SEED_UNIVERSE.tsv` (even a small one) conforming to `schemas/target_seed.tsv`, sourced via `config/external_sources.yaml`.
3. Take the first `target_id` through Modules B and E (the two `CORE_ACTIVE`/`every_target` modules) end to end, producing real `target_evidence.tsv` rows, before building out C/D/F tooling.
4. Not next: reactivating any `SUPPLEMENT_FROZEN` dataset (DepMap, HTAN, CRLM-NMP, Perturb-seq, …) without a named target-specific uncertainty.

## Review history

- **PR #70, round 1** — Initial pivot commit. Web-ChatGPT review (`CRC临床适应症地图`, `Biotech ideas` project): `REQUEST_CHANGES`. Five blockers: (1) target-first existed only in prose, no `target_id` data model; (2) two conflicting dataset-priority sources (`module_classification.tsv` vs `datasets.tsv.priority`) with no schema/vocabulary on the new one; (3) this status file and `knowledge/README.md` still presented the old Phase 2 state as current; (4) `qc_gse178318.py` / `apply_gse178318_qc.py` / `audit_hpa_target_window.py` still carried the old Fig1 marker panel by default, and several module READMEs contradicted canonical registry status; (5) `.gitignore` dropped the legacy `phase2/03_data/raw` etc. patterns, an unnecessary data-leak risk for other checkouts. Three non-blocking suggestions: reclassify `CSPA_PXD000589` out of Module B, register a separate HPA cancer/CRC layer for Module D, flag the PDO's 14-marker mIHC coverage limit.
- **PR #70, round 2** — this round. All five blockers and all three suggestions addressed (see "Completed this pivot" above). Not yet re-submitted for review.

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
