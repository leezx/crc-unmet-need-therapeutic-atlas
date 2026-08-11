# GitHub PR history

## Repository

- Repository: [leezx/crc-unmet-need-therapeutic-atlas](https://github.com/leezx/crc-unmet-need-therapeutic-atlas)
- Default branch: `main`
- Feature branch: `feat/registry-first-atlas`

## PR #1

- URL: [#1](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/1)
- Title at creation: `Initial CRC Unmet-Need Therapeutic Atlas registry`
- State: `OPEN / DRAFT`
- Base: `main`
- Head: `feat/registry-first-atlas`
- Head commit: `c8142233fcffc2a8e27df98aae24a015f31e34b1`
- Actual changed file at review time: `reports/PHASE1_REVIEW_CHECKLIST.md`
- External review: `REQUEST_CHANGES`

## Commit history

- `c2ce3dc` — `Initial registry-first CRC therapeutic atlas`
- `c814223` — `docs: add Phase 1 review checklist`

## Review interpretation

The initial implementation was committed to `main` before the feature branch was created. Therefore PR #1 is not a review of the initial implementation; it is an incremental review-gate PR. This distinction is recorded to prevent future audit confusion.

## Review actions

No automatic merge or P0 download was performed. The PR remains draft until the five requested corrections are implemented and re-reviewed.

## Follow-up review

- Review surface: ChatGPT web conversation `CRC临床适应症地图`
- Reviewed head: `47cc25c7995ed997105fd33f9a1a478075a0265f`
- Result: `APPROVE`
- Follow-up: added `.github/workflows/validate.yml` for ordinary push/PR validation; no merge or data download performed.

## Final quick review

- Reviewed head: `f9c7003`
- Result: `APPROVE`
- CI: `Validate registry` completed successfully according to the web review.
- Mergeability: reported as `mergeable: true`.
- Recommendation: merge PR #1, then begin P0 source verification; do not add knowledge layer or data downloader to PR #1.

## Phase 1 source verification

After PR #1 merged at `240473c`, branch `phase1/p0-source-verification` was created for the next scoped change. The branch records first-pass verification for P0/reference candidates without downloading biological data.

## PR #2 — Phase 1 source verification

- URL: [#2](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/2)
- Title: `Phase 1: verify first P0 data sources`
- State: `OPEN / DRAFT`
- Head branch: `phase1/p0-source-verification`
- Scope: first-party metadata verification and source manifests only; no biological data download.

### Review cycle

- Initial web review of head `f4c743b`: `REQUEST_CHANGES`.
- Blockers: duplicate Zenodo package risk, CRLM cell/sample count confusion, GSE224235 over-strong discovery score, and HTAN treatment annotation semantics.
- Fix commit: `34ea67d` (`fix: address atlas review findings`).
- Final web review of head `34ea67d04f3a4bad07a97b5a7bb423087e49e610`: `APPROVE`.
- Final review confirmed `mergeable: true` and successful `Validate registry` CI; no new blockers.
- User-authorized next action: merge PR #2, then continue provenance materialization without downloading biological data.

## PR #2 merge and next phase

- PR #2 was marked ready and squash-merged on 2026-08-11.
- Merge commit: `80a8506`.
- Next branch: `phase1/p1-provenance-inventory`.
- Initial scope: exact processed-file inventory for GSE178318 and GSE224235, with no biological data download.

## PR #3 — processed-file provenance inventory

- URL: [#3](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/3)
- Reviewed head: `56ba66c7adcacba3d8c6d6af0951c11ae59eb9df`
- Web ChatGPT result: `APPROVE`; CI reported `Validate registry` completed successfully.
- Scope: file-level inventory and schema validation only; no biological data downloaded.
- Next gate: checksum capture and sample-level metadata review.

## PR #4 — GSE178318 sample relationships

- URL: [#4](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/4)
- Reviewed head: `69ccbff3d2f157cb90bc3b83fa77954afa85102e`
- Web ChatGPT result: `APPROVE`; CI reported `Validate registry` completed successfully.
- Scope: 15 GEO sample accessions, six patient groups, primary/liver/PBMC pairing, and conservative treatment `UNKNOWN` values.
- Next gate: checksum capture and sample-level metadata reconciliation.

## PR #5 — GSE178318 treatment reconciliation

- URL: [#5](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/5)
- Reviewed head: `cca8f1c8197f25571c4bf4c691ee5dba5d2e8a98`
- Web ChatGPT result: `APPROVE`; CI reported `Validate registry` completed successfully.
- Scope: publication-backed patient-level treatment group, regimen and surgery timing context; no biological data.
- Next gate: checksum capture and reconciliation of the remaining P0 datasets.

## PR #6 — checksum capture and GSE224235 sample map

- URL: [#6](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/6)
- Reviewed head: `d8a6f7633af26928c427deaa0fa4f6379c81667f`
- Web ChatGPT result: `APPROVE`; CI reported `Validate registry` completed successfully.
- Scope: offline-only checksum utility and 17-sample GSE224235 map; no biological data downloaded.
- Next gate: externally staged-file checksum capture and remaining P0 metadata reconciliation.

## PR #7 — PXD038149 PRIDE provenance

- URL: [#7](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/7)
- Reviewed head: `fc5cd950d1c73b0325bf48b44169172c3af36f66`
- Web ChatGPT result: `APPROVE`; CI reported `Validate registry` completed successfully.
- Scope: PRIDE API-backed inventory of seven non-raw files; 44 raw files remain out of default scope.
- No PRIDE files downloaded; PXD038149 remains `CANDIDATE` pending sample-description review and checksum capture.
- Merged on 2026-08-11; squash merge commit: `0b0a41a`.

## PR #8 — PXD038149 sample-metadata gate

- URL: [#8](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/8)
- Reviewed head: `409d6ded96620b82be63403108aee1ced9a2771a`
- Web ChatGPT result: `APPROVE`; CI reported `Validate registry` completed successfully.
- Scope: record the next-stage parsing contract for `SamplesDescription.xlsx`; no file download or biological data commit.
- Gate: sample metadata may be materialized only after an explicitly staged file is provided; checksum capture remains offline-only.

## PR #9 — GSE117548 CRC PDO source expansion

- URL: [#9](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/9)
- Reviewed head: `a35a9b2580583fb85a1059c04bc5a2ba2a2d8b5c`
- Web ChatGPT result: `APPROVE`; CI reported `Validate registry` completed successfully.
- Scope: index GEO GSE117548 plus supplementary GitHub and EGA provenance endpoints; raw CEL and controlled-access files remain out of default scope.

## PR #10 — GSE117548 supplementary repository inventory

- URL: [#10](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/10)
- Reviewed head: `942a1eb3c5c246c6630cff9922f6bfcee1028a03`
- Web ChatGPT result: `APPROVE`; CI reported `Validate registry` completed successfully.
- Scope: fixed-SHA GitHub API tree inventory for supplementary code/data/model/report assets; no clone, download, execution, or checksum capture.

## PR #11 — GSE117548 asset-layer summary

- URL: [#11](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/11)
- Initial reviewed head: `6811d52bb7c4b4457d78b01305f9c4c7b6ef91c9`; web ChatGPT result: `REQUEST_CHANGES` for an aggregate count/size mismatch.
- Fix: `data/root_metadata` records `data/.DS_Store` as 1 blob / 6,148 bytes.
- Final reviewed head: `54a3a499b7d860cb0a1d8de7545fc434d4e69de5`; web ChatGPT result: `APPROVE`, CI successful.
- Scope: reconcile fixed-commit API totals for raw/processed/external/model/table layers; no file content read or downloaded.
## PR #12 — GSE117548 selected file inventory

- URL: [#12](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/12)
- Reviewed head: 196606d; web ChatGPT result: APPROVE; unique blocker: none.
- Scope: exact fixed-commit metadata for four model-layer blobs and one table blob; Git blob SHA is provenance only, not a content checksum.
## PR #13 — GSE117548 processed file inventory

- URL: [#13](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/13)
- Reviewed head: 272b66d2fd48340f193022513d9df3c257a87fc4
- Web ChatGPT result: APPROVE; CI reported Validate registry completed successfully.
- Scope: exact fixed-commit metadata for all 27 data/processed blobs; no content read, clone, execution, download, or checksum capture.
