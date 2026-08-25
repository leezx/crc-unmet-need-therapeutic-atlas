# Module D data lock — `tgt_nectin4`

Status: **LOCKED — `PXD055821` mass-spec protein abundance + `HPA_CRC_cancer_tissue` IHC. Both whole-tissue, NOT malignant-cell-specific membrane/surface density.**

Same locked files, method, and exclusion rules as `tgt_ceacam5.md` — see that file and `analysis_contracts/pxd055821_protein_abundance.md`/`analysis_contracts/hpa_cancer_ihc.md` for the full method and every caveat. `NECTIN4` is found in `PXD055821`'s gene matrix directly under its current canonical symbol (no alias needed, same as `GSE225857`'s Module B screen — see `modules/module_b_mcrc_target_prevalence/data_lock/tgt_nectin4.md`).

## `NECTIN4` results

`PXD055821`: detected in 13/60 samples (21.7%), the sparsest of the five targets, median=6.913e+04. `HPA_CRC_cancer_tissue`: colorectal cancer, n=10 patients, High=0/Medium=1/Low=7/NotDetected=2 — consistent with (not confirmatory of) `NECTIN4` being a genuinely lower-abundance protein in this evidence set, matching its already-low RNA detection fraction from Module B's screens (`GSE178318`/`GSE225857`). `target_evidence.tsv` rows `TE035` (`PXD055821`) and `TE040` (`HPA_CRC_cancer_tissue`), backed by `EV043`/`EV048`.
