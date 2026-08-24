# Module E question — `tgt_erbb2`

Second of the four remaining `ADC_TARGET_SEED_UNIVERSE.tsv` targets with documented pan-tumor ADC precedent (`CEACAM5` already run, PR #73-75), run 2026-08-24 applying the same corrected method throughout (paper-aligned HPA "RNA expression (HPA)" product, cell-type-resolved IHC as the primary triage layer, `evidence_directness=UNCALIBRATED_PROXY` for both RNA and IHC).

> **明显不值得继续的正常组织 liability——ERBB2 在 colon/rectum 以外的正常组织里是否有明显的 accessible target-positive 群体？**

`ERBB2` (HER2) is a validated ADC target across multiple indications (trastuzumab deruxtecan, trastuzumab emtansine) — no clinical-literature toxicity claim is asserted or checked against here (this pass does not query external clinical literature; corrected 2026-08-24, PR #76 round 1 review — an earlier version of this file asserted "well-documented cardiac and pulmonary...liabilities" as prior fact and framed this run as corroborating it, which this repository's own provenance discipline does not permit without a cited source). This run reports only what this repository's own bulk-RNA + IHC screen shows.
