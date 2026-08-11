# CRC Unmet-Need Therapeutic Atlas

Registry-first evidence acquisition for therapeutic target discovery in advanced and metastatic colorectal cancer.

This repository intentionally stores **no biological data**. It stores dataset provenance, admission decisions, metadata contracts, download instructions, and update reports. Large files, controlled-access data, and generated analysis objects stay outside Git.

## Scope

- MSS/pMMR refractory metastatic CRC
- RAS-mutant non-G12C metastatic CRC
- post-systemic-therapy CRC
- colorectal liver metastasis, especially treated or matched specimens

Core evidence chain: patient population → malignant cell state → surface target → functional dependency/payload vulnerability → normal-tissue therapeutic window.

## Repository map

| Path | Purpose |
| --- | --- |
| `DATA/registry/` | Canonical dataset registry and source manifests |
| `schemas/` | TSV contracts for datasets, samples, and source files |
| `knowledge/` | Source-only clinical-indication ontology and dataset evidence links |
| `reports/` | Candidate review, scan results, and data-gap reports |
| `config/` | Update and storage-policy configuration |
| `scripts/` | Dependency-free validation and metadata scan scripts |
| `.github/workflows/` | Scheduled scan and PR artifact generation |

## Current phase

Phase 1: dataset discovery and review. Seed resources are candidates to verify; no bulk download is started until `reports/DATASET_REVIEW.md` is approved.

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for the review and update workflow.

Project records:

- [`reports/PROJECT_STATUS.md`](reports/PROJECT_STATUS.md)
- [`reports/PR_HISTORY.md`](reports/PR_HISTORY.md)
- [`reports/CHATGPT_CRC_CLINICAL_INDICATION_MAP_FEEDBACK.md`](reports/CHATGPT_CRC_CLINICAL_INDICATION_MAP_FEEDBACK.md)
- [`reports/P0_SOURCE_VERIFICATION.md`](reports/P0_SOURCE_VERIFICATION.md)
- [`knowledge/README.md`](knowledge/README.md)
GitHub supplementary repositories are indexed with fixed-commit tree metadata only; blob contents are not fetched by the registry workflow.
Configured GitHub tree targets are scanned weekly and retained as metadata-only workflow artifacts; target commits are pinned in [`config/github_tree_targets.tsv`](config/github_tree_targets.tsv).
