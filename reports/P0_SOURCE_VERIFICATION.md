# P0 source verification — first pass

Date: 2026-08-10

This is a metadata-only verification pass. No biological data were downloaded.

## Verified as actionable source entries

- **GSE178318** — official GEO record is public, with 15 samples from six labelled patients, matched primary CRC/liver metastasis/PBMC material, preoperative chemotherapy context, processed matrix files, and SRA raw-data availability. The record states that usage terms require contacting the PI.
- **GSE224235** — official GEO record is public and contains matched primary/metastatic lesion material. It is a context comparator, not a genome-wide surface-target discovery dataset: the GEO record verifies NanoString nCounter PanCancer IO 360 (900 genes), while GeoMx availability remains unconfirmed. Processed values are included in the sample table and a 170 KB raw archive is listed.
- **PXD038149** — ProteomeXchange/PRIDE record confirms advanced CRC PDOs, heavily pre-treated models, pre/post-chemotherapy liver disease PDOs, SWATH-MS, bulk RNA-seq and functional drug assays. The repository FTP archive is available; seven non-raw files are indexed, while workbook staging, parsing and checksums remain blocked.
- **HPA** — official Human Protein Atlas portal is live and exposes tissue, single-cell, subcellular, blood, cancer and downloadable-data resources. It remains a required safety reference, not a patient discovery cohort.

## Verified reference or conditional entries

- **GSE226997** — official GEO record confirms four primary CRC Visium samples and processed supplementary files. It remains `REFERENCE_ONLY`; the listed 41.2 GB raw archive is out of scope by default.
- **DepMap 26Q1** — official release entry and 26Q1 release announcement confirm CRISPR, mutation/CNV and expression data. The portal currently applies interactive bot verification; exact CRC subset files and release terms still require recording.
- **MCRC liver-metastasis PDO 2026** — the publication and 213-organoid/102-patient scale are confirmed, but no raw/processed repository accession has been recorded yet. It remains `CANDIDATE` and is not approved for download.
- **CRLM-NMP-ATLAS** — canonical Zenodo/CELLxGENE processed scRNA and spatial data from six CRLM patients with baseline and post-normothermic-perfusion windows; 75,104 cells are listed by CELLxGENE. Sample count remains UNKNOWN. Proposed P0 because it adds an ex vivo therapeutic-window context.
- **HTAN progressive plasticity** — CELLxGENE collection from 31 MSS patients and 83 tumor/normal samples across primary and metastatic sites. Proposed P0 because it directly supports malignant-cell-state and plasticity analysis.
- **GSE159216** — CRLM bulk transcriptomic subtype comparator; proposed P1.
- **Zenodo 10.5281/zenodo.10073712** — retained as an alias/source-mirror candidate for CRLM-NMP-ATLAS because the current manifests show the same 8.2 GB `data share.zip` and checksum. It is not counted as independent evidence pending underlying-package resolution.

## Admission decisions

No candidate is moved to `APPROVED` in this pass. `APPROVED` requires a dataset directory, a source manifest, an exact processed-file inventory, and enough access/license information to make the download reproducible.

## Next actions

1. Inventory processed files and checksums for GSE178318, PXD038149 and HPA.
2. Confirm whether the GSE224235 GeoMx component has a distinct accession or supplementary file set.
3. Record DepMap 26Q1 exact download file names and CRC model filtering rules.
4. Locate the 2026 PDO biobank repository accession.
5. Only then create a reviewed PR that changes candidate status to `APPROVED`.

## Relationship control

Potential duplicate/source relationships are recorded in `DATA/registry/relationships.tsv`. Evidence aggregation must count the canonical dataset only until the relationship is resolved.

## 2026-08-21 pass — ADC Atlas pivot candidates (13 datasets)

This is the Phase 1 verification pass for the 13 datasets added by the ADC Target Repurposing Atlas pivot (`Asset-Generation-OS-architecture.md` → `CRC-Atlas工业化重构`, PR #70). Metadata-only; no biological data downloaded. Full per-candidate detail is in `P0_SOURCE_VERIFICATION.tsv`; `datasets.tsv` and each candidate's `source_manifest.tsv` carry the verified fields.

**Verified via official landing page (GEO/ProteomeXchange/HPA) and publication:**

- **GSE274551** — CB-839+panitumumab(+irinotecan) phase I/II trial (Ciombor et al., Clin Cancer Res 2025, PMID 39927885); 35 tumor-core biopsies, RAS-WT mCRC progressed on prior anti-EGFR. Single processed count matrix confirmed (1.1 MB); file inventory recorded.
- **GSE225857** — Science Advances 2023 (PMID 37327339) confirms the true study scope is 27 samples / 6 patients, not the 8 GSM records formally on GEO; most raw scRNA data lives at CNSA (CNP0002540, CNP0003321) for patient-privacy reasons, a discrepancy worth flagging for anyone reading the GEO page alone.
- **GSE84267** — genuine paired pre-cetuximab(+FOLFOX)/acquired-resistance liver biopsies, 2 patients, 4 samples, PMID 31018951. The only true longitudinal design among the new Module C candidates.
- **GSE196576** — CALGB/SWOG 80405 trial, 579 total / 469 primary tumors analyzed, matches the architecture doc exactly; downstream immune-signature publication PMID 39779996.
- **GSE294385** — 11 patients / 37 samples / 341,328 spatial spots, matches the architecture doc exactly; no associated publication linked on GEO yet, so none is recorded.
- **GSE235919 / GSE235917** — MEDITREME trial RNA-seq and scRNA-seq arms respectively (RAS-mutant MSS mCRC, durvalumab+tremelimumab+chemo), shared PMID 37563240. GSE235919's processed TPM matrix is a single named file; file inventory recorded.
- **GSE5851** — 80 samples confirmed (was `UNKNOWN` sample count before this pass); pretreatment cetuximab-monotherapy pharmacogenomics, PMID 17664471.
- **PXD055821 / PXD022613** — proteomics cohorts confirmed (152 CRLM / 58 CRLM respectively) with real DOIs/PMIDs; file-level PRIDE API listing not yet queried.
- **CSPA_PXD000589** — Bausch-Fluck et al., PLoS One 2015 (PMID 25894527) confirmed; the practically useful access point is the interactive database at `wlab.ethz.ch/cspa`, recorded as a second source alongside the PXD000589 deposit.
- **CPTAC_COAD** — landmark publication confirmed (Vasaikar et al., Cell 2019, PMID 31031003); the PDC portal itself is a JavaScript SPA that could not be fetched for exact study ID or file inventory in this pass.
- **HPA_CRC_cancer_tissue** — HPA v25.1 cancer-proteome page confirmed (20 tumor types incl. colorectal, plus prognostic/RNA/CPTAC-MS layers), distinct from `HPA_normal_tissue`.

## Admission decisions (this pass)

No candidate moves to `APPROVED`. All 13 remain `CANDIDATE`; two (`GSE274551`, `GSE235919`) now have a real single-file `file_inventory.tsv`, the other 11 have an updated, dataset-specific `no_file_inventory_disposition.tsv` explaining exactly what's still deferred (usually: a bundled `RAW.tar`/API listing not yet opened/queried) rather than a generic placeholder.

## Next actions (this pass)

1. Query the PRIDE API file listing for `PXD055821`, `PXD022613`, and `CSPA_PXD000589` (same method already used for `PXD038149`).
2. Fetch the exact GEO suppl `filelist.txt` for `GSE196576` and `GSE235917` to name their processed files precisely.
3. Review CNSA (CNP0002540, CNP0003321) access terms for `GSE225857`'s raw single-cell data.
4. Use the PDC GraphQL/REST API (not the SPA UI) to resolve `CPTAC_COAD`'s exact study ID and case count.
5. Only then consider any candidate for `APPROVED`.
