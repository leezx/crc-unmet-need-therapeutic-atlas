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

First real target run done (2026-08-23, corrected round 1 of PR #73's review): `tgt_ceacam5` (`CEACAM5`), against both the RNA and — after round 1 caught that the first pass wrongly said IHC was unavailable — the cell-type-resolved IHC components of `HPA_normal_tissue`, plus `GTEx_normal_tissue`'s RNA, via `../../scripts/extract_normal_tissue_rna.py`. HPA's two files are read from this repository's own canonical, checksum-verified local cache (`DATA/registry/HPA_normal_tissue/source_manifest.tsv`), not an external `path_env_var` resource; only GTEx is external, resolved via `../../config/external_sources.yaml`'s `module_e_gtex_bulk_rna_reference` block. Three `target_evidence.tsv` rows produced: `TE001`/`TE002` (RNA) and `TE003` (HPA IHC) — all three `evidence_directness=UNCALIBRATED_PROXY` (IHC is closer to real biology than bulk RNA, distinguished by `measurement_layer=IHC`, but is not itself a calibration step — no target-specific quantitative surface assay or IHC-to-surface-density mapping exists here, so it does not earn `CALIBRATED_PROXY`; corrected 2026-08-23, PR #73 round 2 review). The ideal "protein/IHC-first triage" this README calls for is now actually met for this target. See `question/tgt_ceacam5.md`, `data_lock/tgt_ceacam5.md`, `analysis_contracts/tgt_ceacam5.md` (the full per-tissue results TSVs are gitignored, not committed — regenerate via the script above). **No live QC/audit script exists for running this systematically across other targets yet** — the previous `audit_hpa_target_window.py` hardcoded the old Fig1 marker panel and has been archived; see `../../archive/phase2_fetal_state_track_v1/ARCHIVE_NOTE.md`. `scripts/extract_normal_tissue_rna.py` takes `--gene` as an explicit input and is the fresh replacement for the RNA+IHC extraction step, but is not yet wired into a batch runner.

**Remaining four targets run 2026-08-24**: `tgt_erbb2` (`ERBB2`), `tgt_f3` (`F3`), `tgt_nectin4` (`NECTIN4`), `tgt_tacstd2` (`TACSTD2`) — the four other `ADC_TARGET_SEED_UNIVERSE.tsv` targets with documented ADC precedent, same corrected method as `CEACAM5` throughout. 15 new `target_evidence.tsv` rows (`TE007`-`TE009` `ERBB2`, `TE012`-`TE014` `F3`, `TE017`-`TE019` `NECTIN4`, `TE022`-`TE024` `TACSTD2`; RNA HPA + RNA GTEx + IHC per target) — 14 `evidence_directness=UNCALIBRATED_PROXY`, one `UNKNOWN` (`TE014`, `F3`'s IHC row: no usable IHC data exists, which is coded `UNKNOWN`, not a weak proxy — fixed 2026-08-24, PR #76 round 1 review, since "no evidence" must not be coded as "weak evidence"). Real, notable protein-level findings: `ERBB2`'s IHC layer scores cardiomyocytes and lung alveolar cells Medium; `NECTIN4` shows a Medium skin IHC signal on top of its high skin RNA; `TACSTD2` reaches IHC-High in skin (one of two targets in this repository with any IHC-High row — `CEACAM5` has 12 of its own from PR #73). These rows report only the HPA/GTEx expression finding itself — no causal on-target/off-tumor clinical-toxicity claim is made anywhere in this repository's canonical evidence for any of the four (corrected 2026-08-24, PR #76 round 1 review: an earlier version of this PR asserted several such claims — e.g. "matches known anti-HER2 cardiac/pulmonary toxicity" — without a cited clinical source, and one of them, about `TACSTD2`/sacituzumab govitecan's toxicity profile, was itself factually wrong; see `question/tgt_tacstd2.md`). One real, notable gap: **`F3` has no usable HPA IHC data** — exactly one row, `Tissue=N/A`/`Level=N/A`/`Reliability=Uncertain` (confirmed by direct inspection, not a script bug) — its normal-tissue assessment rests on bulk RNA alone, this module's "protein/IHC-first triage" principle genuinely not available for this one target. `NECTIN4`'s and `TACSTD2`'s low-signal compartments are colon/rectum/small-intestine specifically, not "GI" broadly — both still show real Medium IHC signal in esophagus (upper GI). See each target's `question/`, `data_lock/`, `analysis_contracts/tgt_<x>.md`.
