# P0 source verification — first pass

Date: 2026-08-10

This is a metadata-only verification pass. No biological data were downloaded.

## Verified as actionable source entries

- **GSE178318** — official GEO record is public, with 15 samples from six labelled patients, matched primary CRC/liver metastasis/PBMC material, preoperative chemotherapy context, processed matrix files, and SRA raw-data availability. The record states that usage terms require contacting the PI.
- **GSE224235** — official GEO record is public and contains matched primary/metastatic lesion material. It is not a generic scRNA/spatial matrix: the GEO record describes NanoString nCounter PanCancer IO 360 (900 genes), while the wider study includes GeoMx spatial data. Processed values are included in the sample table and a 170 KB raw archive is listed.
- **PXD038149** — ProteomeXchange/PRIDE record confirms advanced CRC PDOs, heavily pre-treated models, pre/post-chemotherapy liver disease PDOs, SWATH-MS, bulk RNA-seq and functional drug assays. The repository FTP archive is available; exact file inventory remains to be recorded.
- **HPA** — official Human Protein Atlas portal is live and exposes tissue, single-cell, subcellular, blood, cancer and downloadable-data resources. It remains a required safety reference, not a patient discovery cohort.

## Verified reference or conditional entries

- **GSE226997** — official GEO record confirms four primary CRC Visium samples and processed supplementary files. It remains `REFERENCE_ONLY`; the listed 41.2 GB raw archive is out of scope by default.
- **DepMap 26Q1** — official release entry and 26Q1 release announcement confirm CRISPR, mutation/CNV and expression data. The portal currently applies interactive bot verification; exact CRC subset files and release terms still require recording.
- **MCRC liver-metastasis PDO 2026** — the publication and 213-organoid/102-patient scale are confirmed, but no raw/processed repository accession has been recorded yet. It remains `CANDIDATE` and is not approved for download.

## Admission decisions

No candidate is moved to `APPROVED` in this pass. `APPROVED` requires a dataset directory, a source manifest, an exact processed-file inventory, and enough access/license information to make the download reproducible.

## Next actions

1. Inventory processed files and checksums for GSE178318, PXD038149 and HPA.
2. Confirm whether the GSE224235 GeoMx component has a distinct accession or supplementary file set.
3. Record DepMap 26Q1 exact download file names and CRC model filtering rules.
4. Locate the 2026 PDO biobank repository accession.
5. Only then create a reviewed PR that changes candidate status to `APPROVED`.
