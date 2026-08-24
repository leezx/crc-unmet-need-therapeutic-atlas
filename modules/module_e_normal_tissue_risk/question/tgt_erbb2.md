# Module E question — `tgt_erbb2`

Second of the four remaining `ADC_TARGET_SEED_UNIVERSE.tsv` targets with documented pan-tumor ADC precedent (`CEACAM5` already run, PR #73-75), run 2026-08-24 applying the same corrected method throughout (paper-aligned HPA "RNA expression (HPA)" product, cell-type-resolved IHC as the primary triage layer, `evidence_directness=UNCALIBRATED_PROXY` for both RNA and IHC).

> **明显不值得继续的正常组织 liability——ERBB2 在 colon/rectum 以外的正常组织里是否有明显的 accessible target-positive 群体？**

Known prior: `ERBB2` (HER2) is a validated ADC target across multiple indications (trastuzumab deruxtecan, trastuzumab emtansine) with well-documented cardiac and pulmonary on-target/off-tumor liabilities in the clinical literature — this run is not discovering that from scratch, it is checking whether this repository's own bulk-RNA + IHC screen surfaces the same signal independently, as a sanity check on the pipeline itself, and whether anything beyond the known cardiac/pulmonary liability shows up.
