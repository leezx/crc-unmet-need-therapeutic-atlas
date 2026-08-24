# Module B question — `tgt_erbb2`

Paired with the Module E run for the same target (`../../module_e_normal_tissue_risk/question/tgt_erbb2.md`). Same `indication_id=mcrc_preop_chemotherapy_crlm` territory and dataset pair (`GSE178318`, `GSE225857`) as `tgt_ceacam5`.

> **在 `mcrc_preop_chemotherapy_crlm` 这个 indication 里，ERBB2 是否有足够多能被地址访问的恶性上皮细胞？**

## Status: `GSE178318` has an epithelial-proxy answer — the malignant-cell question itself is still open

Same method as `tgt_ceacam5` (`data_lock/tgt_erbb2.md`, `analysis_contracts/tgt_erbb2.md`): QC-filtered, EPCAM-based epithelial-proxy screen, **not malignancy-confirmed** — no CNV-based confirmation attempt for this target in this pass (per the `tgt_ceacam5` CNV-lite reviewer's own guidance not to repeat that engineering effort per-target; see `reports/PROJECT_STATUS.md`'s Next handoff). `TE010` (3 treated patients, `indication_id=mcrc_preop_chemotherapy_crlm`) and `TE011` (3 treatment-naive patients, `indication_id=mcrc_liver_metastasis`, context evidence) are the real, QC-filtered result. `GSE225857`'s CNSA raw-sequencing route was blocked at the time this question was first posed; it has since produced its own real result via GEO's public route -- see `TE028` (2026-08-24, PR #81).
