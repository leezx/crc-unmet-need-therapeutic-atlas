# Module D data lock — `tgt_erbb2`

Status: **LOCKED — `PXD055821` mass-spec protein abundance (whole-tissue) + `HPA_CRC_cancer_tissue` IHC (cancer-cell-focused staining category) + `MCRC_liver_metastasis_PDO_2026` PDO mIHC (source-authors'-own reliability caveat — see below). None establishes malignant-cell-specific membrane/surface density.**

`PXD055821`/`HPA_CRC_cancer_tissue` locked files, method, and exclusion rules same as `tgt_ceacam5.md` — see that file and `analysis_contracts/pxd055821_protein_abundance.md`/`analysis_contracts/hpa_cancer_ihc.md`. `MCRC_liver_metastasis_PDO_2026`'s method and its critical caveat are in `analysis_contracts/pdo_erbb2_mihc.md`.

## `ERBB2` results

`PXD055821`: detected in 56/60 specimens (93.3%), median=2.191e+05. `HPA_CRC_cancer_tissue`: colorectal cancer, n=11 patients, High=0/Medium=3/Low=2/NotDetected=6 — the majority of patients score `Not detected` by IHC despite high MS detection frequency, a real cross-source difference not reconciled here (different cohorts, different assay sensitivity). `target_evidence.tsv` rows `TE033` (`PXD055821`) and `TE038` (`HPA_CRC_cancer_tissue`), backed by `EV041`/`EV046`.

`MCRC_liver_metastasis_PDO_2026`: `ERBB2` mIHC detected (nonzero `mean_express_PDO`) in 136/136 PDOs (100.0%), median=0.0910. *** **Not clean corroboration**: the source publication's own methods text states, verbatim, that `ERBB2` "was excluded from analysis due to ... no or very low expression levels" in this 14-marker multiplex panel — the source authors' own QC judged this specific reagent unreliable and excluded it from every downstream analysis in their own paper. A different `ERBB2` antibody clone was used successfully elsewhere in the same publication for a single-patient case-report figure, consistent with this multiplex reagent specifically being the problem, not `ERBB2` IHC in general. `target_evidence.tsv` row `TE042` (`evidence_level=EXPLORATORY_UNDERPOWERED`, `confidence=LOW` — reflecting the caveat, not small-n underpowering), backed by `EV050`. See `analysis_contracts/pdo_erbb2_mihc.md` for the full caveat and why it must always accompany this row.
