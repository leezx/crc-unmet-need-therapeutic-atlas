# Module B question — `tgt_ceacam5`

Paired with the Module E run for the same target (see `../../module_e_normal_tissue_risk/question/tgt_ceacam5.md` for why `CEACAM5` was picked).

> **在 `mcrc_preop_chemotherapy_crlm` 这个 indication（preoperative chemo/RT 后的 matched primary/CRLM 标本）里，CEACAM5 是否有足够多能被地址访问的恶性上皮细胞？**

`indication_id = mcrc_preop_chemotherapy_crlm` — chosen because it is the territory `GSE225857` and `GSE178318` (this module's two `CORE_ACTIVE`/`every_target` datasets per `DATA/registry/module_classification.tsv`) sample, not a broader indication their data can't speak to. Its `prior_therapy` field was loosened 2026-08-23 (PR #73 round 1 review) from a specific regimen (`CAPEOX_OR_FOLFOX_BEV`) to `PREOPERATIVE_CHEMOTHERAPY_AND_OR_RT`, matching what `GSE225857`'s own metadata actually supports — `GSE178318` is itself a mixed cohort where only 3 of 6 patients received a matching regimen (per `DATA/registry/GSE178318/sample_map.tsv`) and the other 3 are treatment-naive, so neither dataset is uniformly "this indication."

## Status: `GSE178318` answered (2026-08-23); `GSE225857` still blocked

See `data_lock/tgt_ceacam5.md` and `analysis_contracts/tgt_ceacam5.md` for the real result: yes, every one of `GSE178318`'s 6 patients has a detectable CEACAM5-positive epithelial subpopulation in both primary and liver-metastasis tissue (`TE004`), with the caveats stated there (marker-score typing, not malignancy calling; n=6 descriptive, not population prevalence; cohort composition is mixed treatment status). `GSE225857` -- this module's other `CORE_ACTIVE` dataset for this indication -- remains genuinely blocked on CNSA access; no `target_evidence.tsv` row exists for it. This mirrors the discipline this repository has used for every genuine gap since the Phase 1 verification pass (PR #71): preserve the gap, don't force a closure, and don't let one dataset's real result stand in for a dataset that's still blocked.
