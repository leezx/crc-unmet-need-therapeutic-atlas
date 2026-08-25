# Module D data lock — `tgt_f3`

Status: **LOCKED — `PXD055821` mass-spec protein abundance (whole-tissue) + `HPA_CRC_cancer_tissue` IHC (cancer-cell-focused staining category). Neither establishes malignant-cell-specific membrane/surface density.**

Same locked files, method, and exclusion rules as `tgt_ceacam5.md` — see that file and `analysis_contracts/pxd055821_protein_abundance.md`/`analysis_contracts/hpa_cancer_ihc.md` for the full method and every caveat.

## `F3` results

`PXD055821`: detected in 16/60 specimens (26.7%), median=1.384e+05. `HPA_CRC_cancer_tissue`: colorectal cancer, n=12 patients, High=0/Medium=0/Low=12/NotDetected=0 — every scored patient is `Low`, never `Not detected`, a distinct pattern from its comparatively sparse MS detection, not reconciled here (different cohorts, different assay sensitivity, not a cross-target ranking). `target_evidence.tsv` rows `TE034` (`PXD055821`) and `TE039` (`HPA_CRC_cancer_tissue`), backed by `EV042`/`EV047`.
