# DepMap Public 26Q1

Official release entry: https://depmap.org/portal/data_page/?tab=allData

Release notes: https://depmap.org/portal/resources?subcategory=release-notes&topic=depmap-quarterly-release-notes

The official 26Q1 release page describes primary and supplemental files covering model/condition/mapping metadata, genome-wide CRISPR screens, copy number, mutations, expression, fusions, global genomic features, and a release README. The 26Q1 release notes report 25 new genome-wide CRISPR/omics models, updated CRISPR library correction and mutation filtering pipelines, and updated model annotations. These are release-level claims only; no CRC subset has been extracted here.

`model_filter_contract.tsv` defines the source-only CRC model selection contract. It names candidate metadata field roles and hold/exclude rules without asserting that the fields or any CRC subset have been materialized. The contract must be checked against the exact pinned release headers before use.

Use the official bulk download section, not portal scraping. The 26Q1 release includes genome-wide CRISPR, expression, mutation and copy-number data. Before approval, record exact file names, release terms, CRC model filtering rules, and checksums.

Current gate: the portal requires interactive human verification and the exact file-level download URLs were not materialized in this repository. Do not infer stable URLs from page text, download bulk files, or claim CRC-specific availability until an authorized interactive portal session or official release catalog provides the exact file names, sizes, URLs, and terms.
