# Contributing and review workflow

1. Add or edit one row in `DATA/registry/datasets.tsv`.
2. Add the corresponding dataset `README.md` and `source_manifest.tsv`.
3. Keep `status` as `CANDIDATE` until the original publication and repository metadata are inspected.
4. Preserve unknowns as `NA` or `UNKNOWN`; never infer treatment or biomarker status.
5. Run `python3 scripts/validate_registry.py` and `python3 scripts/scan_sources.py --offline`.
6. Open a draft PR. A human reviewer approves priority and any change to download scope.

The registry is not a downloader. Prefer processed matrices and metadata. Raw FASTQ/BAM requires an explicit reprocessing decision. Never commit downloaded data, credentials, or controlled-access tokens.

The weekly GitHub Action runs metadata scans only and opens a draft PR for review when scan output changes. Approved P0 downloads remain a separate, explicitly reviewed change.
