# P1 provenance inventory — first processed-file pass

Date: 2026-08-11

This pass records exact repository-listed files, sizes, URLs and download priority. No biological files were downloaded and no candidate was moved to `APPROVED`.

## GSE178318

The official GEO record lists three processed files: `GSE178318_barcodes.tsv.gz` (578.6 KB), `GSE178318_genes.tsv.gz` (258.3 KB), and `GSE178318_matrix.mtx.gz` (520.7 MB). The record also exposes SRA raw data, but raw sequencing remains out of scope. The exact URLs and current checksum state are recorded in `DATA/registry/GSE178318/file_inventory.tsv`.

The series page lists 15 samples from six labelled patients, including matched primary CRC, liver metastasis and PBMC material, and states that data-usage terms require contacting the principal investigator. This remains a strong processed-first candidate, but sample-level treatment and pairing metadata must be reviewed before `APPROVED`.

## GSE224235

The official GEO record states that processed values are included in the sample table and lists `GSE224235_RAW.tar` at 170.0 KB. The accession-level platform is NanoString nCounter PanCancer IO 360 (900 genes); the page describes GeoMx as part of the wider project but does not establish a downloadable GeoMx ROI matrix for this accession. The raw archive is therefore not a default download target.

## Admission decision

Both inventories are `VERIFIED` source records, not `APPROVED` datasets. Approval still requires checksum capture, exact sample-level metadata review, license/access confirmation, and a reproducible download test for the processed files.
