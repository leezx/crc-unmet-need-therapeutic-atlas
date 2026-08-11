# Contributing and review workflow

1. Add or edit one row in `DATA/registry/datasets.tsv`.
2. Add the corresponding dataset `README.md` and `source_manifest.tsv` when source verification begins.
3. Keep `status` as `CANDIDATE` until the original publication and repository metadata are inspected. Candidates may exist only in the canonical registry.
4. Move to `APPROVED` only when a dataset directory and verifiable `source_manifest.tsv` exist.
5. Preserve unknowns as `NA` or `UNKNOWN`; never infer treatment or biomarker status.
6. Run `python3 scripts/validate_registry.py` and `python3 scripts/scan_sources.py --offline`.
7. Run `python3 scripts/build_source_only_closure.py` and confirm the generated `reports/SOURCE_ONLY_CLOSURE_MATRIX.tsv` has no diff.
8. Open a draft PR. A human reviewer approves priority and any change to download scope.

8. Capture checksums only from explicitly staged external files with `scripts/capture_checksums.py`. The script is offline-only: missing files remain `MISSING`, and no repository or network download is performed.

The registry is not a downloader. Prefer processed matrices and metadata. Raw FASTQ/BAM requires an explicit reprocessing decision. Never commit downloaded data, credentials, or controlled-access tokens.

The weekly GitHub Action runs metadata scans only and opens a draft PR for review when stable source status output changes. Per-run timestamps are kept in a separate ignored log. Approved P0 downloads remain a separate, explicitly reviewed change.
For public GitHub supplementary repositories, use scripts/inventory_github_tree.py with a full commit SHA and one or more --prefix values. It calls only the Git trees API and records paths, byte sizes, Git blob SHAs, and fixed blob URLs; it never reads blob contents or downloads repository files. A truncated API response is a hard failure and must be narrowed or handled by a separate reviewed workflow.
Configured public GitHub targets live in config/github_tree_targets.tsv. The weekly workflow runs scripts/scan_github_targets.py and uploads the resulting TSV metadata as a workflow artifact; artifact contents are not committed to this repository. Add or change a target only through a reviewed PR, and update the pinned commit intentionally.
