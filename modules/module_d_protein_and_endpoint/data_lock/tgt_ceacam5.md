# Module D data lock — `tgt_ceacam5`

Status: **LOCKED — `PXD055821` mass-spec protein abundance (whole-tissue) + `HPA_CRC_cancer_tissue` IHC (cancer-cell-focused staining category). Neither establishes malignant-cell-specific membrane/surface density.**

First real Module D run (2026-08-25), per PR #81 round-3 reviewer's explicit recommendation to return to gaps affecting ADC asset selection rather than continuing to invest in `GSE225857`.

Revised 2026-08-25 (PR #82 round 1 review): the original version of this file (a) called `PXD055821`'s 60 columns "samples" when the publication's own text confirms they are 60 specimens from 51 patients (the Sydney cohort) — a specimen-level, not patient-level, read; (b) mischaracterized `HPA_CRC_cancer_tissue` as "whole-tumor-section IHC," when HPA's own methodology scores staining intensity and fraction of *positive cancer cells* specifically. Both fixed below; `evidence_directness` stays `UNCALIBRATED_PROXY` for both sources regardless.

## Inputs locked for this run

- **`PXD055821`** — `DATA/registry/PXD055821/file_inventory.tsv` records `220920_PN_CRC_LM_all_63_LM_DIANN.gg_matrix.tsv` (3.48 MB, SHA256-verified) as downloaded 2026-08-25, physically present (gitignored) at `modules/module_d_protein_and_endpoint/data_lock/raw/PXD055821/`. This is one small, already-processed DIA-NN output for the project's 60-specimen "Sydney cohort" sub-cohort (60 specimens from 51 patients; full project is 152 specimens from 111 patients across 3 centers) — the remaining raw `.raw` files and Proteome Discoverer `.pdResult`/`.msf` files are not usable in this environment (no proteomics search-engine software available). Full method and results: `analysis_contracts/pxd055821_protein_abundance.md`.
- **`HPA_CRC_cancer_tissue`** — `DATA/registry/HPA_CRC_cancer_tissue/file_inventory.tsv` records `cancer_data.tsv.zip` (1.72 MB, SHA256-verified) as downloaded 2026-08-25, physically present at `modules/module_d_protein_and_endpoint/data_lock/raw/HPA_CRC_cancer_tissue/`. Distinct dataset from `HPA_normal_tissue` (Module E only). Full method and results: `analysis_contracts/hpa_cancer_ihc.md`.

## `CEACAM5` results

`PXD055821`: detected (nonzero DIA-NN intensity) in 60/60 specimens (100%), median=3.715e+07. `HPA_CRC_cancer_tissue`: colorectal cancer, n=10 patients, High=6/Medium=4/Low=0/NotDetected=0 — the only target of the five with any `High` IHC calls in this cohort. Two independent protein-layer sources both show real signal for `CEACAM5`, reported as a descriptive observation, not a joint or calibrated score. `target_evidence.tsv` rows `TE032` (`PXD055821`) and `TE037` (`HPA_CRC_cancer_tissue`), backed by `EV040`/`EV045`.

## What is explicitly NOT locked / NOT available

- Neither `PXD055821` nor `HPA_CRC_cancer_tissue` is promoted to `APPROVED` in `DATA/registry/datasets.tsv` — both remain `status=CANDIDATE`. Reading an already-downloaded local file for a real analysis is not the same as promoting a candidate.
- `PXD055821`'s 60-specimen matrix is not resolved to patient IDs (some of the 51 patients contributed more than one specimen), treatment status, or the project's own 3 proteomic phenotypes (CRLM-SD/CA/OM) — this is an aggregate, across-specimens read only.
- `HPA_CRC_cancer_tissue`'s cohort (n=10-12 patients) is a standard, small HPA Pathology Atlas cohort, not linked to this repository's own mCRC treatment-line ontology.

## Exclusion rules

- Whole-tissue mass spectrometry (`PXD055821`) cannot separate a genuinely accessible, cell-surface-positive malignant-cell population from background/stromal/immune/normal-tissue contribution in a bulk specimen. `HPA_CRC_cancer_tissue`'s cancer-cell-focused IHC annotation is a step closer (it does score cancer cells specifically, not a bulk mix), but is still a categorical intensity/fraction-positive call, not membrane-specific or quantitative antigen density. `evidence_directness=UNCALIBRATED_PROXY` for all rows this run produced (`TE032`-`TE041`), for both sources, regardless of this distinction.
- Neither source is a calibration step for the other, or for any RNA-based evidence already in this repository (Module B/E) — cross-source agreement or disagreement is recorded as a descriptive observation, not resolved into a single number, and not used to rank the five targets against each other (per-protein MS response and per-antibody IHC scale both differ across targets — see `analysis_contracts/pxd055821_protein_abundance.md`'s and `analysis_contracts/hpa_cancer_ihc.md`'s own comparability caveats).
- Per this repository's Module D contract (`modules/module_d_protein_and_endpoint/README.md`): "Whole-tissue MS ≠ malignant-cell-specific membrane density... Module D output is protein-level support, never a Module B surface-density upgrade."
