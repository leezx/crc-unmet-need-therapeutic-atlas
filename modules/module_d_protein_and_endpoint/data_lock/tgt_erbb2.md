# Module D data lock — `tgt_erbb2`

Status: **LOCKED — `PXD055821` mass-spec protein abundance (whole-tissue) + `HPA_CRC_cancer_tissue` IHC (cancer-cell-focused staining category). Neither establishes malignant-cell-specific membrane/surface density.**

Same locked files, method, and exclusion rules as `tgt_ceacam5.md` — see that file and `analysis_contracts/pxd055821_protein_abundance.md`/`analysis_contracts/hpa_cancer_ihc.md` for the full method and every caveat.

## `ERBB2` results

`PXD055821`: detected in 56/60 specimens (93.3%), median=2.191e+05. `HPA_CRC_cancer_tissue`: colorectal cancer, n=11 patients, High=0/Medium=3/Low=2/NotDetected=6 — the majority of patients score `Not detected` by IHC despite high MS detection frequency, a real cross-source difference not reconciled here (different cohorts, different assay sensitivity). `target_evidence.tsv` rows `TE033` (`PXD055821`) and `TE038` (`HPA_CRC_cancer_tissue`), backed by `EV041`/`EV046`.
