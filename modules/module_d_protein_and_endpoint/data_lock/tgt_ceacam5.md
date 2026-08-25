# Module D data lock — `tgt_ceacam5`

Status: **LOCKED — `PXD055821` mass-spec protein abundance + `HPA_CRC_cancer_tissue` IHC. Both whole-tissue, NOT malignant-cell-specific membrane/surface density.**

First real Module D run (2026-08-25), per PR #81 round-3 reviewer's explicit recommendation to return to gaps affecting ADC asset selection rather than continuing to invest in `GSE225857`.

## Inputs locked for this run

- **`PXD055821`** — `DATA/registry/PXD055821/file_inventory.tsv` records `220920_PN_CRC_LM_all_63_LM_DIANN.gg_matrix.tsv` (3.48 MB, SHA256-verified) as downloaded 2026-08-25, physically present (gitignored) at `modules/module_d_protein_and_endpoint/data_lock/raw/PXD055821/`. This is one small, already-processed DIA-NN output for a 60-sample sub-cohort of the project's full 152-sample CRLM cohort — the remaining raw `.raw` files and Proteome Discoverer `.pdResult`/`.msf` files are not usable in this environment (no proteomics search-engine software available). Full method and results: `analysis_contracts/pxd055821_protein_abundance.md`.
- **`HPA_CRC_cancer_tissue`** — `DATA/registry/HPA_CRC_cancer_tissue/file_inventory.tsv` records `cancer_data.tsv.zip` (1.72 MB, SHA256-verified) as downloaded 2026-08-25, physically present at `modules/module_d_protein_and_endpoint/data_lock/raw/HPA_CRC_cancer_tissue/`. Distinct dataset from `HPA_normal_tissue` (Module E only). Full method and results: `analysis_contracts/hpa_cancer_ihc.md`.

## `CEACAM5` results

`PXD055821`: detected (nonzero DIA-NN intensity) in 60/60 samples (100%), median=3.715e+07. `HPA_CRC_cancer_tissue`: colorectal cancer, n=10 patients, High=6/Medium=4/Low=0/NotDetected=0 — the only target of the five with any `High` IHC calls in this cohort. Two independent protein-layer measurement types both point toward `CEACAM5` being a real, well-detected tumor-tissue protein in this evidence set. `target_evidence.tsv` rows `TE032` (`PXD055821`) and `TE037` (`HPA_CRC_cancer_tissue`), backed by `EV040`/`EV045`.

## What is explicitly NOT locked / NOT available

- Neither `PXD055821` nor `HPA_CRC_cancer_tissue` is promoted to `APPROVED` in `DATA/registry/datasets.tsv` — both remain `status=CANDIDATE`. Reading an already-downloaded local file for a real analysis is not the same as promoting a candidate.
- `PXD055821`'s 60-sample matrix is not resolved to patient IDs, treatment status, or the project's own 3 proteomic phenotypes (CRLM-SD/CA/OM) — this is an aggregate, across-samples read only.
- `HPA_CRC_cancer_tissue`'s cohort (n=10-12 patients) is a standard, small HPA Pathology Atlas cohort, not linked to this repository's own mCRC treatment-line ontology.

## Exclusion rules

- Whole-tissue mass spectrometry (`PXD055821`) and whole-tumor-section IHC (`HPA_CRC_cancer_tissue`) cannot separate a genuinely accessible, cell-surface-positive malignant-cell population from background/stromal/immune/normal-tissue contribution in a bulk sample — `evidence_directness=UNCALIBRATED_PROXY` for all four rows this run produced (`TE032`, `TE037`, and the equivalent rows for the other four targets).
- Neither source is a calibration step for the other, or for any RNA-based evidence already in this repository (Module B/E) — cross-source agreement or disagreement is recorded as a descriptive observation, not resolved into a single number.
- Per this repository's Module D contract (`modules/module_d_protein_and_endpoint/README.md`): "Whole-tissue MS ≠ malignant-cell-specific membrane density... Module D output is protein-level support, never a Module B surface-density upgrade."
