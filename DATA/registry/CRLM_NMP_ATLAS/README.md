# CRLM-NMP-ATLAS

The latest published Zenodo version is record `16939324` (`10.5281/zenodo.16939324`), linked to concept DOI `10.5281/zenodo.15234826`. Its source API exposes three downloadable archives: `data.zip`, `Analysis.zip`, and `environments.zip`. This repository records their names, sizes, source-record MD5 values, license and download paths only.

The inner h5ad file names, sample rows and baseline/post-perfusion window fields are not asserted because the archives have not been downloaded or staged. The CELLxGENE collection remains a second source-level access path.

`sample_map_contract.tsv` defines the source-to-row metadata contract for patient, specimen, anatomic context, perfusion window, assay modality and exposure context. It intentionally contains no sample rows; absent fields remain UNKNOWN until a source-level metadata export or explicitly staged archive listing is reviewed.

Primary data record: https://zenodo.org/records/15234826

CELLxGENE collection: https://cellxgene.cziscience.com/collections/be679cb1-35f0-46c9-9a2d-30691862a54a

Canonical processed resource: six colorectal-liver-metastasis patients and 75,104 cells listed by the CELLxGENE collection, including baseline and post-normothermic-perfusion windows. The Zenodo package currently reports an 8.2 GB `data share.zip`; sample count is not inferred from the cell count. Prefer the processed h5ad package and metadata; do not download raw sequencing by default.

The Zenodo record `10.5281/zenodo.10073712` is tracked separately as a provenance alias/source-mirror candidate because it exposes the same `data share.zip` size and checksum observed in the current manifests. It must not be counted as an independent cohort until resolved.
