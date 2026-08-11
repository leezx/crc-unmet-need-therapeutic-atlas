# P6 — PXD038149 sample-metadata gate

## Objective

Define the provenance contract for the next review of the two PRIDE sample-description workbook candidates without downloading or committing either workbook.

## Authoritative source

- Dataset: `PXD038149`
- Preferred file: `SamplesDescriptionFINAL.xlsx`
- Alternate file: `SamplesDescription.xlsx`
- PRIDE API file category: `OTHER`
- Recorded sizes: `9,686` bytes (`SamplesDescriptionFINAL.xlsx`) and `8,577` bytes (`SamplesDescription.xlsx`)
- Recorded endpoints: both exact FTP paths are in `DATA/registry/PXD038149/file_inventory.tsv`
- Registry entry: `DATA/registry/PXD038149/file_inventory.tsv`

The preferred workbook is `SamplesDescriptionFINAL.xlsx` because it is the explicitly final-named sample-description artifact in the PRIDE file inventory. The alternate workbook must not be silently merged with it; if both are staged, compare their schemas and identifiers before selecting one.

## Parsing contract after explicit staging

1. Accept a user- or workflow-staged local copy only; do not add a downloader to the registry repository.
2. Capture MD5/SHA-256 locally with `scripts/capture_checksums.py` before reading content into an analysis workspace.
3. Record workbook sheet names, column headers, row count, and a stable source-to-row identifier map.
4. Preserve raw source labels verbatim; normalize only into documented fields such as sample identifier, model/organoid identifier, disease context, treatment exposure, treatment timing, and assay role.
5. Use `UNKNOWN` when the workbook does not support a field. Do not infer systemic treatment exposure from PDO/drug-response labels alone.
6. Keep the dataset `CANDIDATE` until sample-level provenance and license/access checks pass review.

## Stop conditions

- No staged file: metadata parsing and checksum capture stop; the registry remains source-only.
- Both workbook candidates staged with conflicting schemas or identifiers: stop and open a review issue/PR; do not choose by filename alone.
- Workbook schema changes or ambiguous sample identifiers: open a review issue/PR instead of guessing.
- Raw `.wiff`/`.wiff.scan` files remain out of scope unless a separate explicit reprocessing decision is approved.
