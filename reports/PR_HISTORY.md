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
## PR #14 — GSE117548 external file inventory

- URL: [#14](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/14)
- Reviewed head: 26597fd7972f07c18b59a721c70651c3fe2c9271
- Web ChatGPT result: APPROVE; no data/provenance blocker.
- Scope: exact fixed-commit metadata for all 11 data/external blobs; external references remain separate from GSE117548 biological data.

## PR #15 — fixed-commit GitHub tree scanner

- URL: [#15](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/15)
- Initial reviewed head: `8f5059f`; web ChatGPT result: REQUEST_CHANGES because `--commit` accepted floating refs.
- Fix reviewed head: `e03089eea70627c7db51e8521ce139911be0d41d`; web ChatGPT result: APPROVE; CI completed successfully.
- Scope: dependency-free scanner for GitHub Trees API metadata, requiring a full 40-character commit SHA; outputs path, size, Git blob SHA and fixed blob URL, with no blob reads or downloads.
## PR #16 — scheduled fixed GitHub tree metadata scans

- URL: [#16](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/16)
- Initial reviewed head: `09cd65288bd461fa03ecb1ca1d48f8f104ea2f82`; web ChatGPT result: REQUEST_CHANGES for duplicate `target_id`/`output_name` allowing silent TSV overwrite.
- Fix reviewed head: `47846b469f9c2c5a87502512c189eb775f0bcfe0`; web ChatGPT result: APPROVE.
- Scope: reviewed fixed-target configuration, duplicate-output guards, weekly metadata-only scan, and artifact upload; no blob reads, clone, execution, or biological-data download.

## PR #17 — scanner safety regression tests

- URL: [#17](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/17)
- Initial reviewed head: `ba93d992`; web ChatGPT result: REQUEST_CHANGES for output creation before validation and an ineffective temporary-directory assertion.
- Fix reviewed head: `4a1186a31330a63977eaa9ad62f9742dfda88bc6`; web ChatGPT result: APPROVE; Validate registry CI successful.
- Scope: offline tests for floating-ref and duplicate-target rejection, with PR CI coverage; no network or data download.

## PR #18 — pinned GitHub target drift checker

- URL: [#18](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/18)
- Initial reviewed head: `e07078a`; web ChatGPT result: REQUEST_CHANGES because GitHub commits API could return `files[].patch`.
- Fix reviewed head: `b910ea7`; web ChatGPT result: APPROVE; Validate registry CI successful.
- Scope: compare pinned SHA with tracking branch using Git ref metadata only; no automatic pin changes, blob reads, clone, execution, or biological-data download.

## PR #19 — tracked GitHub target update report

- URL: [#19](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/19)
- Reviewed head: `26edd5e`; web ChatGPT result: APPROVE; Validate registry CI successful.
- Scope: version-controlled metadata report and draft-PR update path; pinned commits remain unchanged until separate review.

## PR #20 — drift-checker regression-test hardening

- URL: [#20](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/20)
- Initial reviewed head: `2627269`; web ChatGPT result: REQUEST_CHANGES because the test checked only the first request and reused the pinned SHA as the fake latest SHA.
- Fix reviewed head: `67a6f04`; web ChatGPT result: APPROVE; local regression suite passed (3 tests).
- Scope: strengthen the offline test to require exactly one Git ref metadata request, reject `/commits/`, and prove the returned `object.sha` drives drift detection; no blob reads, patches, clones, downloads, or automatic pin changes.
- Merge: squash-merged on 2026-08-11 as `43037f70b953657c6cbb1c6b5e148ac1ebf11bc0`.

## PR #21 — pinned-target update review checklist

- Scope: document the human review gate for `update_available=TRUE`, including fixed-commit tree comparison, inventory reconciliation, separate pin-update PRs, and no-download boundaries.
- Web ChatGPT result: `APPROVE`; no provenance or metadata-only blocker.

## PR #22 — GSE226997 source metadata

- URL: [#22](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/22)
- Initial reviewed head: `6c4db77`; web ChatGPT result: REQUEST_CHANGES because the not-downloaded raw archive had a non-NA download date.
- Fix reviewed head: `1d1c421`; web ChatGPT result: APPROVE.
- Scope: official GEO source, four sample accessions, processed supplementary-file availability, deferred raw archive, and no inferred treatment context; no biological content downloaded or stored.

## PR #23 — GSE226997 file-level metadata

- URL: [#23](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/23)
- Initial reviewed head: `7a60950`; web ChatGPT result: REQUEST_CHANGES because four sample-level URLs pointed to the series directory and returned 404.
- Fix reviewed head: `a70d5ce`; web ChatGPT result: APPROVE after sample-level URL correction and HTTP HEAD checks.
- Scope: four exact GEO sample archives, byte sizes, fixed download URLs, and raw archive metadata; checksums remain unrecorded and no file content was downloaded.

## PR #24 — GSE159216 provenance

- URL: [#24](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/24)
- Initial reviewed head: `ce4fda2`; web ChatGPT result: REQUEST_CHANGES for `priority=P1_DOWNLOAD` contradicting comparator-only/no-download semantics, followed by a second blocker identifying `n_patients=283` instead of 171.
- Final reviewed head: `f789cf0`; web ChatGPT result: APPROVE after setting `priority=REFERENCE_ONLY`, `n_patients=171`, and `n_samples=283`.
- Scope: official GEO/filelist metadata for 283 samples, 283 processed CHP files, 283 raw CEL files, and aggregate sizes; no biological content downloaded or read.

## PR #25 — reconcile project status with repository state

- URL: [#25](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/25)
- Initial reviewed head: `7178051`; web ChatGPT result: REQUEST_CHANGES because the status report incorrectly said there were no open PRs while PR #25 itself was OPEN / DRAFT.
- Fix reviewed head: `1b4fc99`; web ChatGPT result: APPROVE.
- Scope: replace stale planning status with the current 19-candidate registry, 24 merged PRs, completed provenance components, active gates, and next-step priorities.
- No registry data, candidate status, download policy, or biological-data boundary changed.

## PR #26 — DepMap 26Q1 release provenance

- URL: [#26](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/26)
- Initial reviewed head: `ee4276e`; web ChatGPT result: REQUEST_CHANGES because `download_date` was populated despite no download being performed.
- Fix reviewed head: `cbfd7c8`; web ChatGPT result: APPROVE.
- Scope: official DepMap Public 26Q1 release and release-notes provenance, release-level file families, and interactive portal verification gate; no CRC subset extraction, biological data, exact download files, or checksums.

## PR #27 — HPA 25.1 file provenance

- URL: [#27](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/27)
- Reviewed head: `41da9cd`; web ChatGPT result: APPROVE.
- Scope: HPA v25.1/Ensembl v109, four official downloadable endpoints, CC BY 4.0 and third-party constraint caveat; no HPA file download, checksum capture, therapeutic-window claim, or candidate approval.

## PR #28 — CRLM PDO biobank repository

- URL: [#28](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/28)
- Reviewed head: `2dd9751`; web ChatGPT result: APPROVE.
- Scope: Mendeley Data v3 accession `hr94h42xdc.3`, DOI `10.17632/hr94h42xdc.3`, CC BY 4.0, and five Data S1–S5 processed/derived files; no file download, checksum capture, raw-sequencing claim, or candidate approval.

## PR #29 — P0 Phase 1 admission matrix

- URL: [#29](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/29)
- Initial reviewed head: `8643557`; web ChatGPT result: REQUEST_CHANGES because CRLM PDO `license_access=PASS` contradicted the stated pending third-party-term review.
- Fix reviewed head: `4b291c8`; web ChatGPT result: APPROVE.
- Scope: ten P0 candidate gate states across publication/context, treatment, molecular annotation, processed inventory, license/access and update audit; all decisions remain HOLD and all registry statuses remain CANDIDATE.

## PR #30 — GSE178318 admission-gate reconciliation

- URL: [#30](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/30)
- Reviewed head: `af49234`; web ChatGPT result: APPROVE.
- Scope: reconcile the completed 15-sample/6-patient treatment and pairing metadata with the P0 matrix; treatment context is PASS, while molecular annotation, PI-contact terms, checksums and final admission remain open; dataset status remains CANDIDATE.

## PR #31 — PXD038149 sample-metadata gate

- URL: [#31](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/31)
- Reviewed head: `ec01bef`; web ChatGPT result: APPROVE.
- Scope: distinguish `SamplesDescriptionFINAL.xlsx` and `SamplesDescription.xlsx`, define explicit staging/schema/checksum stop conditions, and retain PXD038149 as P0_DOWNLOAD/CANDIDATE/HOLD; no workbook download or parsing.

## PR #32 — source-only knowledge/review layer skeleton

- URL: [#32](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/32)
- Initial reviewed head: `2f2d619`; web ChatGPT result: REQUEST_CHANGES because PROJECT_STATUS incorrectly said the CRLM PDO accession was not located.
- Fix reviewed head: `79cdc46`; web ChatGPT result: APPROVE.
- Scope: seed clinical-indication ontology and dataset evidence links with `SOURCE_INDEXED_NOT_ANALYZED` / `SEED_UNREVIEWED` statuses; no biological data, target ranking, therapeutic-window claim or dataset approval.

## PR #33 — source-only evidence objects

- URL: [#33](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/33)
- Initial reviewed head: `b9bd08d`; web ChatGPT result: REQUEST_CHANGES because EV003 used an invalid Mendeley v3 URL with a dot instead of the `/3` path.
- Fix reviewed head: `72b31d3`; web ChatGPT result: APPROVE for the URL-only follow-up.
- A subsequent audit of documentation head `3bc1a11` found a second blocker: EV008 structured value said `16 patients; 25 samples`, while the source supports 16 CRC PDOs and 25 samples. Corrected locally to `16 CRC PDOs; 25 samples`; final web review is pending.
- Review of head `e3e1223` found a third blocker: EV001/EV002 supporting-text paths omitted the `reports/` prefix. Corrected locally to the existing `reports/` paths; final web review is pending.
- Final reviewed head: `35a34df`; web ChatGPT result: APPROVE after confirming all three corrections and the source-only boundary.
- Merge-prep audit of head `c0324f7` found stale PROJECT_STATUS wording that said no evidence object existed; corrected to distinguish eight source-only evidence objects from absent biological/clinical conclusions. Final review is pending.
- Follow-up audit of head `b97f5bd` found PROJECT_STATUS file-level inventory count stale at 5; corrected to 7 and added HPA_normal_tissue plus MCRC_liver_metastasis_PDO_2026 to the list. Final review is pending.
- Follow-up audit of head `71afa13` found PROJECT_STATUS incorrectly called the older `35a34df` approval the latest approval; corrected to distinguish historical approval from the current pending head. Final review is pending.
- Follow-up audit of head `99c7722` found the pending-head pointer still named `71afa13`; corrected to the current head. Final review is pending.
- Final pointer correction is recorded in the next commit because the status file itself remained at `99c7722` after the `f60bf9a` documentation commit.
- Removed the self-referential current-head pointer from PROJECT_STATUS; it now records the historical approved head and stable pending-review state.
- Planning review of head `a50ddf0` found the next-step text still requested a new knowledge/review layer PR despite PR #32/#33 establishing the skeleton; updated to continuation and human review of the existing layer.
- Scope: eight source-only evidence objects, evidence IDs linked to indication links, provenance/confidence/version fields, and missing-information notes; no biological data, target ranking, therapeutic-window claim or dataset approval.
- Local validation: registry validator passed, 3 unit tests passed, diff check passed, and both TSV files passed independent column-count checks.
- Merge: squash-merged on 2026-08-11 as `c830dba7b5fa78de4abb3234bb86c35e94795cd1`.

## PR #34 — reconcile PR #33 merge status

- URL: [#34](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/34)
- Reviewed head: `b7f52d6`; web ChatGPT result: APPROVE.
- Scope: synchronize post-merge status, PR history and ChatGPT feedback; no registry, evidence schema, biological data or clinical/target conclusion changes.

## PR #35 — PXD038149 provenance hygiene

- URL: [#35](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/35)
- Reviewed head: `3934be9`; web ChatGPT result: APPROVE.
- Scope: correct no-download manifest fields and stale inventory wording; PXD038149 remains P0_DOWNLOAD/CANDIDATE with workbook staging, parsing and checksum gates blocked.
- No biological data downloaded or committed.

## PR #36 — reconcile PR #35 status

- URL: [#36](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/36)
- Reviewed head: `b95f1fc`; web ChatGPT result: APPROVE.
- Scope: update project status after PR #35 merge and move the next-step emphasis from PXD038149 inventory to its remaining workbook gate plus DepMap/HPA/CRLM provenance; no data or schema changes.

## PR #37 — DepMap release evidence object

- URL: [#37](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/37)
- Initial reviewed head: `37b6bb5`; web ChatGPT result: REQUEST_CHANGES because EV009/IEL009 duplicated existing EV004/IEL004.
- Fix reviewed head: `5863b1d`; web ChatGPT result: APPROVE after consolidating the update into EV004/IEL004 and restoring the count to eight source-only evidence objects.
- Scope: strengthen DepMap 26Q1 release-level provenance; no CRC subset, dependency result, biological data, target ranking or approval status.

## PR #38 — batch HPA/CRLM provenance status

- URL: [#38](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/38)
- Initial reviewed head: `add076e`; web ChatGPT result: REQUEST_CHANGES because HPA `cell.svg` was incorrectly grouped with versioned endpoints.
- Fix reviewed head: `aed039c`; web ChatGPT result: APPROVE after separating three v25.1 atlas exports from one static asset.
- Scope: batch no-download/status hygiene for HPA, CRLM-NMP and main-branch status; no candidate status or biological data changes.
- Existing issue deferred: `reports/P0_SOURCE_VERIFICATION.tsv` has historical row-width inconsistencies outside this PR scope.

## PR #39 — align P0 verification columns

- URL: [#39](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/39)
- Reviewed head: `615a223`; web ChatGPT result: APPROVE.
- Scope: restore the missing `publication_or_record` field in four P0 verification rows, align all rows to the 10-column header, and synchronize post-PR #38 status; no biological or clinical content changes.

## PR #40 — parallel P0 next gates

- URL: [#40](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/40)
- Reviewed head: `caa6f74`; web ChatGPT result: APPROVE.
- Scope: define five blocked/planned source-only gates for DepMap exact-file/filtering, HPA minimum-organ reference, and CRLM-NMP h5ad/sample-map work; no downloads, biological data or approval changes.

## PR #41 — latest CRLM-NMP Zenodo archive inventory

- URL: [#41](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/41)
- Initial reviewed head: `f5b803f`; web ChatGPT result: REQUEST_CHANGES because the file inventory used record-page URLs instead of file-level download endpoints.
- Fix reviewed head: `d81ec41`; web ChatGPT result: APPROVE after changing `source_url` to the Zenodo API `/files/<name>/content` endpoints.
- Scope: correct the latest published Zenodo version, index three archive-level files with source-record sizes/MD5/license and direct download paths, and preserve the explicit no-download/no-inner-h5ad/no-sample-count boundary.
- No biological data downloaded or committed; inner h5ad names and sample-level metadata remain blocked.

## PR #42 — quantified project status

- URL: [#42](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/42)
- Initial reviewed head: `8f7be81`; web ChatGPT result: REQUEST_CHANGES because the 58% progress number had no reproducible denominator or scoring weights.
- Fix reviewed head: `a22f4aa`; web ChatGPT result: APPROVE after adding a fixed 100-point scorecard with explicit engineering/provenance sub-scores and a separate 0/20 scientific/clinical readiness score.
- Scope: reconcile merged PR/status counts and persist quantitative progress reporting; no biological data, candidate approval or clinical conclusion changes.

## PR #43 — HPA minimum organ reference

- URL: [#43](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/43)
- Reviewed head: `87b3c24`; web ChatGPT result: APPROVE.
- Scope: add a 10-organ HPA v25.1 source-derived minimum reference contract with tissue groups, coverage roles and stop conditions; update EV005 and HPA-G1.
- No HPA file downloaded, no checksum captured, no therapeutic-window/toxicity claim and no candidate approval.
