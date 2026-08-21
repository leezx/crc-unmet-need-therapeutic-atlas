# Modules

This repository is organized around the six evidence modules defined in `../ADC_ATLAS_DATASET_CONTRACT.md`, replacing the old dataset-first / global fetal-state discovery structure (see `../archive/phase2_fetal_state_track_v1/ARCHIVE_NOTE.md`).

| Module | Status | Location |
| --- | --- | --- |
| A — `DERISKED_TARGET_UNIVERSE` | External, reused — not built here | see `../config/external_sources.yaml` (logical `path_env_var` references, not hardcoded paths) |
| B — `MCRC_TARGET_PREVALENCE` | Developed and reviewed in this repo | [`module_b_mcrc_target_prevalence/`](module_b_mcrc_target_prevalence/README.md) |
| C — `REFRACTORY_PERSISTENCE` | Developed and reviewed in this repo | [`module_c_refractory_persistence/`](module_c_refractory_persistence/README.md) |
| D — `PROTEIN_AND_ENDPOINT` | Developed and reviewed in this repo | [`module_d_protein_and_endpoint/`](module_d_protein_and_endpoint/README.md) |
| E — `NORMAL_TISSUE_RISK` | Developed and reviewed in this repo | [`module_e_normal_tissue_risk/`](module_e_normal_tissue_risk/README.md) |
| F — `DELIVERY_AND_CAUSALITY_LITERATURE` | Core support branch, developed in this repo | [`module_f_delivery_and_causality_literature/`](module_f_delivery_and_causality_literature/README.md) |

## Shared conventions

- **Canonical dataset registry stays single-source.** Modules reference dataset IDs already registered in `../DATA/registry/datasets.tsv`; a module folder never forks its own copy of registry metadata. `../DATA/registry/module_classification.tsv` — validated by `../scripts/validate_module_classification.py` against a controlled vocabulary — records each dataset's `module`, `activation_status` (`CORE_ACTIVE`, `CORE_CONTEXT`, `CORE_SUPPORT`, `CONTEXT_ACTIVE`, `SUPPORT`, `REFERENCE_CORE`, `REFERENCE_SUPPORT`, `SUPPLEMENT`, `SUPPLEMENT_FROZEN`), `adc_decision_axis`, `activation_rule`, and `default_execution_order` within its module. `datasets.tsv`'s own `priority` column is legacy Phase 1 download-priority metadata only — not an execution signal.
- **All module output is `target_id`-keyed.** A finding is only real evidence once it is a row in `../schemas/target_evidence.tsv` (or `../schemas/evidence.tsv` / `../schemas/indication_evidence_links.tsv`, which now also carry `target_id`) — not a gene name mentioned in a report's prose. See `../knowledge/README.md`.
- **Per-module working structure** (created as work starts, not pre-populated speculatively):
  - `question/` — the falsifiable question and scope boundary for the module, same spirit as the archived `phase2/01_question/`.
  - `data_lock/` — which processed inputs are locked in for analysis, and why.
  - `analysis_contracts/` — QC rules, marker/protein lists (target-driven, not a hardcoded panel — see the archived Fig1-marker scripts' postmortem in `../archive/phase2_fetal_state_track_v1/ARCHIVE_NOTE.md`), and figure-level contracts before any analysis runs.
  - `results/` — analysis outputs, per dataset, keyed by `target_id`.
- **Source-only discipline is unchanged.** No biological data is committed to this repository regardless of module; see `../CONTRIBUTING.md`.
- **Module F has one registered dataset** (`CSPA_PXD000589`, a delivery/surfaceome-accessibility reference — reclassified here from Module B on 2026-08-21, since it carries no mCRC patient prevalence information) plus sourced literature evidence objects (see `../knowledge/README.md` for the evidence-object schema, which Module F extends rather than replaces).
