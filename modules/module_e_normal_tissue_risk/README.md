# Module E — NORMAL_TISSUE_RISK

## Goal

Not a safety score. Find:

> **明显不值得继续的正常组织 liability。**

The question is not "is average normal-tissue RNA a few-fold lower than tumor?" It is: does liver, small intestine, lung, kidney, heart, bone marrow, etc. contain an accessible target-positive cell population?

## Inputs

- `HPA_normal_tissue` (HPA v25.1) — 45 normal tissues IHC + tissue RNA/MS + ~76 annotated cell types. Registry `status` is `CANDIDATE`, same as every other dataset in this registry; it has a file inventory further along than most, but that is not an `APPROVED` designation — do not describe it as one.
- GTEx / normal scRNA as bulk-RNA support only.

## Per-target output

Per key compartment (colon, small intestine, liver, lung, kidney, heart, skin, bone marrow, …): protein/IHC-first triage of accessible target-positive cell populations, not just RNA. All rows `target_id`-keyed per `../../schemas/target_evidence.tsv`.

## Cannot prove

HPA-negative ≠ safe. IHC intensity ≠ accessible antigen density. This module alone cannot assert a therapeutic window.

## Status

First real target run done (2026-08-23): `tgt_ceacam5` (`CEACAM5`), against the bulk-RNA components of `HPA_normal_tissue`/`GTEx_normal_tissue` via the new `../../scripts/extract_normal_tissue_rna.py` (fail-closed `path_env_var` read, no new download — see `../../config/external_sources.yaml`'s `module_e_normal_tissue_bulk_rna_reference` block). Two `target_evidence.tsv` rows produced (`TE001`/`TE002`), `evidence_directness=UNCALIBRATED_PROXY` (bulk RNA, not protein/IHC/cell-type-resolved — the ideal "protein/IHC-first triage" this README calls for is still not met). See `question/tgt_ceacam5.md`, `data_lock/tgt_ceacam5.md`, `analysis_contracts/tgt_ceacam5.md` (`results/tgt_ceacam5_normal_tissue_rna.tsv` itself is gitignored, not committed — regenerate it from the two source files via the script above). **No live QC/audit script exists for the IHC/cell-type-resolved side of `HPA_normal_tissue` yet** — the previous `audit_hpa_target_window.py` hardcoded the old Fig1 marker panel and has been archived; see `../../archive/phase2_fetal_state_track_v1/ARCHIVE_NOTE.md`. A fresh script must take a target-specific protein list as an explicit input.
