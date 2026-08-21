# Modules

This repository is organized around the six evidence modules defined in `../ADC_ATLAS_DATASET_CONTRACT.md`, replacing the old dataset-first / global fetal-state discovery structure (see `../archive/phase2_fetal_state_track_v1/ARCHIVE_NOTE.md`).

| Module | Status | Location |
| --- | --- | --- |
| A — `DERISKED_TARGET_UNIVERSE` | External, reused — not built here | `/Volumes/Stelligen_SSD/Stelligen/DATA/1.Databases/ADCdb/ADCdb_Obsidian` and `.../ADCdb_Claude_redo` |
| B — `MCRC_TARGET_PREVALENCE` | Developed and reviewed in this repo | [`module_b_mcrc_target_prevalence/`](module_b_mcrc_target_prevalence/README.md) |
| C — `REFRACTORY_PERSISTENCE` | Developed and reviewed in this repo | [`module_c_refractory_persistence/`](module_c_refractory_persistence/README.md) |
| D — `PROTEIN_AND_ENDPOINT` | Developed and reviewed in this repo | [`module_d_protein_and_endpoint/`](module_d_protein_and_endpoint/README.md) |
| E — `NORMAL_TISSUE_RISK` | Developed and reviewed in this repo | [`module_e_normal_tissue_risk/`](module_e_normal_tissue_risk/README.md) |
| F — `DELIVERY_AND_CAUSALITY_LITERATURE` | Core support branch, developed in this repo | [`module_f_delivery_and_causality_literature/`](module_f_delivery_and_causality_literature/README.md) |

## Shared conventions

- **Canonical dataset registry stays single-source.** Modules reference dataset IDs already registered in `../DATA/registry/datasets.tsv`; a module folder never forks its own copy of registry metadata. `../DATA/registry/module_classification.tsv` records which module(s) each dataset serves and its activation status (`CORE_ACTIVE`, `CORE_CONTEXT`, `CONTEXT_ACTIVE`, `SUPPLEMENT_FROZEN`).
- **Per-module working structure** (created as work starts, not pre-populated speculatively):
  - `question/` — the falsifiable question and scope boundary for the module, same spirit as the archived `phase2/01_question/`.
  - `data_lock/` — which processed inputs are locked in for analysis, and why.
  - `analysis_contracts/` — QC rules, marker sets, and figure-level contracts before any analysis runs.
  - `results/` — analysis outputs, per dataset.
- **Source-only discipline is unchanged.** No biological data is committed to this repository regardless of module; see `../CONTRIBUTING.md`.
- **Module F is literature/claims-only** — it has no `DATA/registry` biological files at all, only sourced evidence objects (see `../knowledge/README.md` for the existing evidence-object schema, which Module F extends rather than replaces).
