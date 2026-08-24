# Module B question — `tgt_f3`

Paired with the Module E run for the same target (`../../module_e_normal_tissue_risk/question/tgt_f3.md`). Same `indication_id=mcrc_preop_chemotherapy_crlm` territory and dataset pair as `tgt_ceacam5`/`tgt_erbb2`.

> **在 `mcrc_preop_chemotherapy_crlm` 这个 indication 里，F3 是否有足够多能被地址访问的恶性上皮细胞？**

## Status: `GSE178318` has an epithelial-proxy answer — the malignant-cell question itself is still open

Same method as `tgt_ceacam5`/`tgt_erbb2` (`data_lock/tgt_f3.md`, `analysis_contracts/tgt_f3.md`): QC-filtered, EPCAM-based epithelial-proxy screen, **not malignancy-confirmed**, no CNV-based confirmation attempt for this target in this pass. `TE015` (3 treated patients) and `TE016` (3 treatment-naive patients, context evidence) are the real, QC-filtered result. `GSE225857` remains genuinely blocked on CNSA access; no row exists for it.
