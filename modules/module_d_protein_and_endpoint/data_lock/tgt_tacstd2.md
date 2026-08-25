# Module D data lock — `tgt_tacstd2`

Status: **LOCKED — `PXD055821` mass-spec protein abundance + `HPA_CRC_cancer_tissue` IHC. Both whole-tissue, NOT malignant-cell-specific membrane/surface density.**

Same locked files, method, and exclusion rules as `tgt_ceacam5.md` — see that file and `analysis_contracts/pxd055821_protein_abundance.md`/`analysis_contracts/hpa_cancer_ihc.md` for the full method and every caveat.

## `TACSTD2` results

`PXD055821`: detected in 43/60 samples (71.7%), median=3.025e+05, the second-highest detection fraction of the five targets. `HPA_CRC_cancer_tissue`: colorectal cancer, n=12 patients, High=0/Medium=0/Low=3/NotDetected=9 — 9 of 12 patients score `Not detected` by IHC despite reasonably frequent MS detection, a real cross-source difference not reconciled here (different cohorts, different assay sensitivity). `target_evidence.tsv` rows `TE036` (`PXD055821`) and `TE041` (`HPA_CRC_cancer_tissue`), backed by `EV044`/`EV049`.
