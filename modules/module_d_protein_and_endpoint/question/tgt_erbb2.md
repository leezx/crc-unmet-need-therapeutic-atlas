# Module D question — `tgt_erbb2`

Same method and data sources as `tgt_ceacam5.md`.

> **`ERBB2`'s RNA signal (Module B: `RNA_low` in every patient x site stratum in both CRLM cohorts, never `RNA_high` or `RNA_no`) — does protein-level evidence corroborate it?**

See `data_lock/tgt_erbb2.md`: a real, notable split — `PXD055821` MS detects `ERBB2` in 93.3% of specimens (high detection frequency), but `HPA_CRC_cancer_tissue` IHC scores the majority of patients (6/11) `Not detected`. Recorded as a genuine cross-source disagreement, not resolved or explained away here — could reflect real biological heterogeneity, different cohort composition, or different assay sensitivity between mass spec and IHC. A third source, `MCRC_liver_metastasis_PDO_2026`'s PDO mIHC, detects `ERBB2` (nonzero) in 136/136 PDOs — but this source cannot be read as tipping the balance toward "detected": the source publication's own methods text states `ERBB2` was excluded from its own analysis due to unreliable signal in this specific multiplex panel, so a nonzero value here is at least as consistent with assay noise as with true expression (see `analysis_contracts/pdo_erbb2_mihc.md`). ADC precedent for `ERBB2` is recorded in Module A and not restated here.
