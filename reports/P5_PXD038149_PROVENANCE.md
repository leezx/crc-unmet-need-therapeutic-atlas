# P5 PXD038149 provenance inventory

Date: 2026-08-11

The official PRIDE/ProteomeXchange API confirms PXD038149 as a human advanced-CRC PDO proteotranscriptomic dataset with CC0 license metadata, TripleTOF 6600 SWATH-MS, bulk RNA-seq context and functional drug-response aims. The associated publication describes 29 PDO lines from 22 advanced CRC patients, including heavily pre-treated models and a paired pre/post-chemotherapy liver-metastasis model.

The PRIDE API reports 51 files: 44 raw files and 7 non-raw files. This repository inventories the seven non-raw files only: sample descriptions, two quantitative proteomics spreadsheets, search/identification output, a spectral-library peak file, and preprocessing output. Their exact FTP paths and byte sizes are in `DATA/registry/PXD038149/file_inventory.tsv`.

No PRIDE files were downloaded. Raw `.wiff` and `.wiff.scan` files remain priority 3/out of default scope. Checksum capture is deferred until an explicitly approved external staging step.

## Admission state

PXD038149 remains `CANDIDATE`, not `APPROVED`. The next gate is to inspect the sample-description workbook and reconcile PDO names, primary/metastatic origin, treatment exposure and drug-response fields after an explicit processed-file staging decision.
