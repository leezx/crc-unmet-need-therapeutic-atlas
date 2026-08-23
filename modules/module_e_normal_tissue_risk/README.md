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

First real target run done (2026-08-23, corrected round 1 of PR #73's review): `tgt_ceacam5` (`CEACAM5`), against both the RNA and — after round 1 caught that the first pass wrongly said IHC was unavailable — the cell-type-resolved IHC components of `HPA_normal_tissue`, plus `GTEx_normal_tissue`'s RNA, via `../../scripts/extract_normal_tissue_rna.py`. HPA's two files are read from this repository's own canonical, checksum-verified local cache (`DATA/registry/HPA_normal_tissue/source_manifest.tsv`), not an external `path_env_var` resource; only GTEx is external, resolved via `../../config/external_sources.yaml`'s `module_e_gtex_bulk_rna_reference` block. Three `target_evidence.tsv` rows produced: `TE001`/`TE002` (RNA, `evidence_directness=UNCALIBRATED_PROXY`) and `TE003` (HPA IHC, `evidence_directness=CALIBRATED_PROXY`) — the ideal "protein/IHC-first triage" this README calls for is now actually met for this target. See `question/tgt_ceacam5.md`, `data_lock/tgt_ceacam5.md`, `analysis_contracts/tgt_ceacam5.md` (the full per-tissue results TSVs are gitignored, not committed — regenerate via the script above). **No live QC/audit script exists for running this systematically across other targets yet** — the previous `audit_hpa_target_window.py` hardcoded the old Fig1 marker panel and has been archived; see `../../archive/phase2_fetal_state_track_v1/ARCHIVE_NOTE.md`. `scripts/extract_normal_tissue_rna.py` takes `--gene` as an explicit input and is the fresh replacement for the RNA+IHC extraction step, but is not yet wired into a batch runner.
