# P7 — GSE226997 source review

## Source evidence

- Official GEO record: <https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE226997>
- Title: *Visium Spatial transcriptomics analysis of human primary colorectal cancer*.
- Organism and design: Homo sapiens; four primary CRC patients; Visium spatial transcriptomics.
- Samples: `GSM7089855`–`GSM7089858`, one series sample per patient.
- Processed availability: the official supplementary `filelist.txt` lists four sample-level archives: `GSM7089855_Ajou_Visium_P1.tar.gz` (12,863,232,737 bytes), `GSM7089856_Ajou_Visium_P2.tar.gz` (9,722,628,803 bytes), `GSM7089857_Ajou_Visium_P3.tar.gz` (9,824,252,182 bytes), and `GSM7089858_Ajou_Visium_P4.tar.gz` (11,783,555,645 bytes). Their sample-level URLs returned HTTP 200 on metadata-only HEAD checks; these are indexed only and were not downloaded.
- Raw availability: `GSE226997_RAW.tar`, listed as 44,193,679,360 bytes; not downloaded and not required for this processed-first registry gate.
- Publication: PMID 38446659; DOI `10.1038/s41598-024-52868-0`.

## Registry decision

The dataset remains `CANDIDATE` and `REFERENCE_ONLY`. This pass records exact public file metadata and download URLs only. Checksums remain `NOT_RECORDED` because no biological file content was downloaded or read.
