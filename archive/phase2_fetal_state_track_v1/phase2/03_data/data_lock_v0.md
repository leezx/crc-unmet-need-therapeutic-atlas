# Phase 2 data-lock v0

状态：**PLANNED — not yet locked**

## Primary cohort candidates

| Dataset | Role | Required lock before analysis |
|---|---|---|
| GSE178318 | matched primary/CRLM scRNA discovery | sample-level treatment/pairing and processed-file integrity |
| HTAN_CRC_progressive_plasticity | independent malignant-state replication | exact export metadata, patient/sample mapping and cell-type scope |
| CRLM_NMP_ATLAS | independent ex vivo CRLM state/window context | row-level sample map and perfusion-window metadata |

## Target/safety candidates

| Dataset | Role | Required lock before analysis |
|---|---|---|
| HPA_normal_tissue | normal-tissue exclusion | versioned file metadata, organ scope and terms |
| GTEx_normal_tissue | bulk normal-tissue comparator | release/access terms and comparator limitations |

## Functional candidates

| Dataset | Role | Required lock before analysis |
|---|---|---|
| DepMap_26Q1 | dependency context | exact CRC model subset, file headers and release pin |
| MCRC_liver_metastasis_PDO_2026 | PDO multi-omic/drug-response context | sample-level clinical/treatment reconciliation and terms |
| PXD038149 | proteotranscriptomic/PDO response context | workbook staging, sample metadata and processed-file selection |

## Inclusion/exclusion rules

- Primary analysis requires malignant epithelial annotation or a reproducible malignant-cell-state proxy.
- Individual cells are not independent biological replicates; patient/sample is the inferential unit.
- Mouse engineered-organoid series GSE263580–GSE263582 remain reference-only and cannot be used as human cohort evidence.
- Controlled-access EGA Perturb-seq remains a source-only functional reference until access is separately authorized.
- No target is promoted to `APPROVED` from expression alone.
