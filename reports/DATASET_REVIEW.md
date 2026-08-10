# Dataset review — Phase 1

Status: **DRAFT / pending source verification**

The registry contains seed candidates from the CRC Unmet-Need Therapeutic Atlas architecture. Before any bulk download, inspect each candidate against the original publication and repository metadata.

## P0 candidates

`GSE178318`, `GSE224235`, `DepMap_26Q1`, `PXD038149`, `MCRC_liver_metastasis_PDO_2026`, `CRC_organoid_CRISPR_dependency`, `HPA_normal_tissue`.

Admission requires high clinical relevance and target-discovery value after verification, plus documented processed data and access terms.

## P1 candidates

`GSE260797`–`GSE260800`, `CRC_Perturb_seq`. Retain only if they add independent malignant-cell-state, spatial, or functional evidence.

## Reference-only candidates

`GSE226997`, `GTEx_normal_tissue`. These comparators cannot substitute for treated metastatic patient evidence or protein-level therapeutic-window evidence.

## Rejected datasets

None recorded yet. Reject generic early-stage, DNA-only, immune-only, or model-only resources that do not close a therapeutic uncertainty.

## Major data gaps

- verified treatment history and matched pre/post specimens
- public advanced/mCRC PDO metadata and drug response
- protein-level surface-target evidence in malignant cells
- normal-tissue cell-type and membrane-localization evidence
- controlled-access availability for clinically annotated cohorts

## Controlled access and storage

No controlled-access accession is admitted until access instructions are documented. Total storage remains `UNKNOWN` until source verification. Processed-first policy applies; raw sequencing is out of scope for Phase 1.

## Stop condition

Do not begin bulk downloading until this review is approved in a PR.
