# Archive note — Phase 2 fetal-state / plasticity discovery track (v1)

Archived: 2026-08-21, updated 2026-08-21 after web-ChatGPT review of PR #70 (`REQUEST_CHANGES`, item 4). Nothing here was deleted; this is a straight move from the repository root into this archive folder.

## Why this track is archived, not continued

The original Phase 2 question (`phase2/01_question/one_sentence_question.md`) was:

> 是否存在跨患者可复现的、metastasis-enriched 的 fetal/plasticity-like malignant epithelial 状态，并能推导出一个通过 surface accessibility、normal-tissue window 和 functional support 门禁的候选靶点。

This is a **generic malignant-state discovery** approach: start from an unsupervised cell-state signature (fetal/plasticity-like program), then try to find a druggable target inside it.

The repository's scope was superseded on 2026-08-21 by the **ADC Target Repurposing Atlas** direction recorded in `Asset-Generation-OS-architecture.md` → `CRC-Atlas工业化重构`. That direction inverts the order: start from an already-derisked ADC target universe (Module A, maintained outside this repo), and use this repo only to answer target-specific prevalence/persistence/protein/safety questions (Modules B–F). See `../../ADC_ATLAS_DATASET_CONTRACT.md` and `../../modules/README.md`.

Concretely, the fetal-state NMF/plasticity discovery path is no longer a default analysis path in this repository (it is explicitly named as a track to freeze in the architecture doc: *"放弃原来的 fetal-state 主线"*).

## What is archived here

- `phase2/` — the full Phase 2 tree: one-sentence question, novelty check, figure plan, GSE178318 data lock, cell QC contract, Figure 1 marker set, and result JSON for GSE178318 / CRLM_NMP_ATLAS / GSE224235 / HPA_normal_tissue / HTAN_CRC_progressive_plasticity. Includes locally staged processed inputs under `phase2/03_data/raw/` (gitignored, never committed).
- `reports/GSE178318_STATE_SCORE.md`, `reports/HTAN_CRC_STATE_VALIDATION.md`, `reports/CRLM_NMP_ATLAS_INDEPENDENT_VALIDATION.md`, `reports/GSE224235_VALIDATION_AUDIT.md` — the state-validation reports produced by that track.
- `scripts/score_gse178318_state.py`, `scripts/audit_gse224235_validation.py`, `scripts/validate_crlm_nmp_independent.py`, `scripts/validate_htan_state.py` — the fetal-state scoring script and the validation scripts for datasets now marked `SUPPLEMENT_FROZEN` (GSE224235, CRLM_NMP_ATLAS, HTAN_CRC_progressive_plasticity) in `../../DATA/registry/module_classification.tsv`.
- `scripts/qc_gse178318.py`, `scripts/apply_gse178318_qc.py`, `scripts/audit_hpa_target_window.py` — **corrected 2026-08-21**: these were initially left live in `scripts/` on the claim that their QC logic was "generic, reusable groundwork" for GSE178318/HPA_normal_tissue. Web-ChatGPT review of PR #70 caught that this was wrong: `audit_hpa_target_window.py` hardcodes the old Fig1 marker panel (`TACSTD2, L1CAM, EMP1, SOX2, CHGA, KRT5`) as its `TARGETS` constant, and `qc_gse178318.py` defaults `--marker-set` to the archived `figure1_marker_set_v1.tsv` and writes output back into `phase2/06_results/`. Neither is target-list-driven; both are Fig1-fetal-state tooling, not generic QC. They are archived here with the rest of the track.

**No working QC/audit script exists for GSE178318 or HPA_normal_tissue right now.** When Module B/C (GSE178318) or Module E (HPA_normal_tissue) actually starts a data lock, write a fresh script that takes a target-specific marker/protein list as an explicit input (from the Module A target seed, not a hardcoded constant) — do not resurrect these in place.

## What is not affected

- `DATA/registry/`, `schemas/`, `scripts/`, `knowledge/`, `config/`, and the P0–P8 provenance/closure reports stay in place at the repository root. They are source-only registry infrastructure, not scientific-direction artifacts, and most of the datasets they cover (GSE178318, HPA_normal_tissue, PXD038149, MCRC_liver_metastasis_PDO_2026, …) remain active — now reused under the new Module B–F questions instead of the old Fig1 fetal-state question.
- No dataset row in `DATA/registry/datasets.tsv` was deleted. Datasets that are out of scope for the new Core (e.g. GSE224235, HTAN_CRC_progressive_plasticity, CRLM_NMP_ATLAS, DepMap_26Q1) are marked `SUPPLEMENT_FROZEN` in `DATA/registry/module_classification.tsv`, not removed.

## If this track is ever resumed

Treat it as a `SUPPLEMENT_FROZEN` / target-specific query path (per the architecture doc's "只有当 target X 已经进入 shortlist... 此时再激活" rule), not as a default repository-wide analysis. Re-derive a fresh data lock and analysis contract under the relevant `modules/` folder instead of reactivating this tree in place.
