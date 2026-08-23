# Module B question — `tgt_ceacam5`

Paired with the Module E run for the same target (see `../../module_e_normal_tissue_risk/question/tgt_ceacam5.md` for why `CEACAM5` was picked).

> **在 `mcrc_preop_chemotherapy_crlm` 这个 indication（preoperative chemo/RT 后的 matched primary/CRLM 标本）里，CEACAM5 是否有足够多能被地址访问的恶性上皮细胞？**

`indication_id = mcrc_preop_chemotherapy_crlm` — chosen because it is exactly the territory `GSE225857` and `GSE178318` (this module's two `CORE_ACTIVE`/`every_target` datasets per `DATA/registry/module_classification.tsv`) actually sample, not a broader indication their data can't speak to.

## Status: BLOCKED, not answered

See `data_lock/tgt_ceacam5.md`. No `target_evidence.tsv` row is written for Module B in this pass -- an absent row here means no claim was made, not that the answer is negative or unknown-and-guessed. This mirrors the discipline this repository has used for every genuine gap since the Phase 1 verification pass (PR #71): preserve the gap, don't force a closure.
