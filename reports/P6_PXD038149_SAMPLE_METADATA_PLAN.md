# P6 — PXD038149 sample-metadata gate

## Objective

Define the provenance contract for the next review of `SamplesDescription.xlsx` without downloading or committing the workbook.

## Authoritative source

- Dataset: `PXD038149`
- File: `SamplesDescription.xlsx`
- PRIDE API file category: `OTHER`
- Recorded size: `8,577` bytes
- Recorded endpoint: `ftp://ftp.pride.ebi.ac.uk/pride/data/archive/2025/02/PXD038149/SamplesDescription.xlsx`
- Registry entry: `DATA/registry/PXD038149/file_inventory.tsv`

## Parsing contract after explicit staging

1. Accept a user- or workflow-staged local copy only; do not add a downloader to the registry repository.
2. Capture MD5/SHA-256 locally with `scripts/capture_checksums.py` before reading content into an analysis workspace.
3. Record workbook sheet names, column headers, row count, and a stable source-to-row identifier map.
4. Preserve raw source labels verbatim; normalize only into documented fields such as sample identifier, model/organoid identifier, disease context, treatment exposure, treatment timing, and assay role.
5. Use `UNKNOWN` when the workbook does not support a field. Do not infer systemic treatment exposure from PDO/drug-response labels alone.
6. Keep the dataset `CANDIDATE` until sample-level provenance and license/access checks pass review.

## Stop conditions

- No staged file: metadata parsing and checksum capture stop; the registry remains source-only.
- Workbook schema changes or ambiguous sample identifiers: open a review issue/PR instead of guessing.
- Raw `.wiff`/`.wiff.scan` files remain out of scope unless a separate explicit reprocessing decision is approved.
