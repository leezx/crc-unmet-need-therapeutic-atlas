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

## PR #44 — progress after HPA gate

- URL: [#44](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/44)
- Reviewed head: `f986a66`; web ChatGPT result: APPROVE.
- Scope: reconcile status after PR #43 and update the fixed score from 58/100 to 60/100 (+2) for the HPA source-derived organ contract; no biological or clinical content changes.

## PR #45 — batch P0 provenance contracts

- URL: [#45](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/45)
- Initial reviewed head: `2719e02`; web ChatGPT result: REQUEST_CHANGES because the score incorrectly counted source-only contracts as exact dataset provenance.
- Fix reviewed head: `55bd8c4`; web ChatGPT result: REQUEST_CHANGES only because the PR description retained the stale 66/100 number; description corrected to 65/100 and final review approved.
- Scope: batch DepMap model-filter, CRLM sample-map/window and HPA source-review contracts; add the five-gate crosswalk; preserve exact provenance at 5/15 and raise the auditable overall score from 60/100 to 65/100 through source/index (+1) and P0 gate-design (+4) infrastructure.
- No data downloads, sample rows, dependency results, target ranking, therapeutic-window or clinical conclusion.

## PR #46 — source-only completion framework

- URL: [#46](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/46)
- Initial reviewed head: `4d899bf`; web ChatGPT result: REQUEST_CHANGES because internal closure work could be waived as an external blocker.
- Fix reviewed head: `9ab56c6`; web ChatGPT result: APPROVE after separating mandatory internal requirements from the external-blocker allowlist.
- Scope: define the source-only 100% endpoint, weighted dimensions and closeout checklist; no biological data, analysis or dataset approval.

## PR #47 — source-only closure matrix and CI

- URL: [#47](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/47)
- Initial reviewed head: `e73c908`; web ChatGPT result: REQUEST_CHANGES because missing repository artifacts were automatically classified as external blockers.
- Fix reviewed head: `fb5003e`; web ChatGPT result: REQUEST_CHANGES because the PR description retained stale blocker wording; description corrected and final review approved.
- Scope: add the 19-candidate closure matrix, offline builder, CI freshness check and auditable status update from 65/100 to 70/100; missing artifacts are `INTERNAL_ACTION_REQUIRED`, not waived external blockers.

## PR #48 — update-target disposition

- URL: [#48](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/48)
- Initial reviewed head: `89e09c9`; web ChatGPT result: REQUEST_CHANGES because the configured score weights did not match the PROJECT_STATUS closure/handoff denominator.
- Fix reviewed head: `1d27a62`; web ChatGPT result: APPROVE after defining source-only completion as a 90-point endpoint and separating the 10-point scientific readiness overlay.
- Scope: record the first metadata-only scan for the single configured GitHub target (`NO_UPDATE_PIN_RETAINED`), update the closure checklist and status from 70/100 to 75/100; no blob read, pin change, download or analysis.

## PR #49 — source-only final boundary audit

- Initial reviewed head: `cd9705c` after four targeted corrections in the same PR; web ChatGPT result: APPROVE in the existing conversation “PR审核与错误反馈”.
- Scope: add a deterministic audit script and CI guardrail for forbidden biological suffixes, raw/processed/data paths, tracked files over 50 MiB and required source-only control files; update the auditable project score from 75/100 to 80/100. No data download, analysis, candidate approval or clinical conclusion.

## PR #50 — explicit no-file-inventory dispositions

- Initial reviewed head: `239c4fb`; web ChatGPT result: APPROVE after validating the structured disposition contract, blocker-class mapping, and exact 85/90 score arithmetic in the existing conversation “PR审核与错误反馈”.
- Scope: add four tracked source-only disposition records for candidates with source manifests but intentionally unmaterialized file inventories; update the closure builder and project score from 80/100 to 85/100. No file download, biological data, analysis, candidate approval or clinical conclusion.

## PR #51 — known-source manifest completion

- Scope: add official GEO/GTEx source manifests and structured no-file-inventory dispositions for five known-source candidates; update the project score from 85/100 to 90/100. Two unknown-source candidates remain explicit internal blockers. No file download, biological data, analysis, candidate approval or clinical conclusion.
- Initial web review: `REQUEST_CHANGES`. The 90/90 weighted engineering score was easy to misread as source-only endpoint completion while two candidates remained `INTERNAL_ACTION_REQUIRED`.
- Correction: distinguish the weighted infrastructure score from the completion gate in `config/project_completion.yaml` and `reports/PROJECT_STATUS.md`; endpoint status remains `INCOMPLETE` until the two internal source manifests are materialized.

## PR #52 — remaining source identities

- URL: [#52](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/52)
- Reviewed head: `7ed27b7`; web ChatGPT result: APPROVE in the existing conversation “PR审核与错误反馈”.
- Scope: identify official GEO CRISPR-screen subseries GSE263580/GSE263581/GSE263582 and EGA Perturb-seq study EGAS50000000256; preserve internal scope/access review blockers and update the offline closure test. No file download, biological data, analysis, candidate approval or clinical conclusion.

## PR #53 — source-only final closure

- URL: [#53](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/53)
- Initial reviewed head: `f7e8b12`; web ChatGPT result: REQUEST_CHANGES because the resolved mouse organoid source was still labeled `P0_DOWNLOAD` despite a reference-only scope decision.
- Fix reviewed head: `202427d`; web ChatGPT result: APPROVE after changing the candidate to `REFERENCE_ONLY` and aligning registry, scope review and source manifest semantics.
- Scope: add final scope/access review artifacts, remove all `INTERNAL_ACTION_REQUIRED` rows from the closure matrix, and prepare the source-only endpoint for closure on merge. No download, access request, biological data, analysis, candidate approval or clinical conclusion.

## PR #54 — source-only completion status sync

- Scope: after PR #53 merge, set `completion_endpoint.current_status` to `COMPLETE` and synchronize `PROJECT_STATUS.md` to source-only 100% completion. The weighted project score remains 90/100 because scientific/clinical readiness is explicitly out of scope and remains 0/10.
- Initial reviewed head: `1138690`; web ChatGPT result: REQUEST_CHANGES because residual `SOURCE_INDEXED_REVIEW_REQUIRED` handoffs were not explicitly addressed by the completion rule.
- Fix reviewed head: `e101ec5`; web ChatGPT result: APPROVE after defining the source-only closure rule and distinguishing dataset-review handoffs from internal blockers.

## PR #55 — source-only handoff documentation

- URL: [#55](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/55)
- Initial reviewed head: `57736ee`; web ChatGPT result: REQUEST_CHANGES because registry priority counts were stale.
- Fix head: `f329e1f`; web ChatGPT identified a second documentation contradiction in the closure checklist.
- Final reviewed head: `8dbeb7a`; web ChatGPT result: APPROVE after aligning the checklist with the explicit no-file-inventory disposition rule.
- Scope: synchronize final source-only counts, completion checklist and post-closure handoff. No data download, access request, analysis, candidate approval or clinical conclusion.

## PR #56 — Phase 2 therapeutic state discovery plan

- URL: [#56](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/56)
- Reviewed head: `52bdabe`; web ChatGPT result: APPROVE in the existing conversation “PR审核与错误反馈”.
- Scope: define the falsifiable state-to-target question, novelty/feasibility screen, five-figure skeleton and initial data-lock v0. Planning only; no download, analysis, candidate approval or clinical conclusion.

## PR #57 — GSE178318 data lock

- URL: [#57](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/57)
- Reviewed head: `bfe85e8`; web ChatGPT result: APPROVE in the existing conversation “PR审核与错误反馈”.
- Scope: download and checksum the three official GSE178318 processed inputs into an ignored local Phase 2 directory; record dimensions and data-lock metadata. No biological interpretation, target approval or clinical conclusion.

## PR #58 — Figure 1 GSE178318 analysis contract

- URL: [#58](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/58)
- Initial reviewed head: `5223464`; web ChatGPT result: REQUEST_CHANGES because the marker/program list was not locked.
- Fix reviewed head: `31ad91a`; web ChatGPT result: APPROVE in the existing conversation “PR审核与错误反馈”.
- Scope: lock `FIG1_MARKER_V1`, separate identity/state/confounder genes, and preserve patient-level statistics and no-clinical-claim boundaries. No biological conclusion or target approval.

## PR #59 — GSE178318 structural QC

- URL: [#59](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/59)
- Initial reviewed head: `03a5231`; web ChatGPT result: REQUEST_CHANGES because reconciliation outcomes were reported but not fail-closed.
- Intermediate fix head: `c2c1346`; web ChatGPT requested the reverse expected-key completeness check.
- Final reviewed head: `6e13875`; web ChatGPT result: APPROVE in the existing conversation “PR审核与错误反馈”.
- Scope: run structural QC on locked GSE178318 inputs, enforce matrix/barcode/sample/marker gates, record per-sample distributions, and update progress from 90/100 to 92/100. No cutoff selection, biological claim, target ranking or clinical conclusion.

## PR #60 — GSE178318 cell-QC rules

- URL: [#60](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/60)
- Initial reviewed head: `3fa0767`; web ChatGPT result: REQUEST_CHANGES because `QC_SENSITIVE` lacked a reproducible material-change threshold.
- Fix reviewed head: `efc727e`; web ChatGPT result: APPROVE in the existing conversation “PR审核与错误反馈”.
- Scope: define primary/permissive/stringent cell-QC rules and explicit sensitivity criteria; update progress from 92/100 to 93/100. No malignancy/state claim, target ranking or clinical conclusion.

## PR #61 — GSE178318 QC retention execution

- URL: [#61](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/61)
- Initial reviewed head: `eb3aaf7`; web ChatGPT result: REQUEST_CHANGES because retention-only checks were labeled complete `QC_STABLE` without paired effect-direction analysis.
- Fix reviewed head: `d1d83be`; web ChatGPT result: APPROVE in the existing conversation “PR审核与错误反馈”.
- Scope: execute three reviewed QC rules, report retention and matched-pair availability, label retention stability separately, and update progress from 93/100 to 95/100. No state score, target ranking or clinical conclusion.

## PR #62 — GSE178318 patient-level state scores

- URL: [#62](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/62)
- Initial reviewed head: `7c1639b`; web ChatGPT result: REQUEST_CHANGES because excluded cell-cycle/stress confounders were not reported.
- Fix reviewed head: `55977b6`; web ChatGPT result: APPROVE in the existing conversation “PR审核与错误反馈”.
- Scope: compute locked-marker descriptive patient-level scores, paired metastasis-minus-primary effects and exact sign-flip summaries; report excluded confounder scores; update progress from 95/100 to 97/100. Exploratory only; no target or clinical conclusion.

## PR #63 — GSE224235 independent-validation audit

- URL: [#63](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/63)
- Initial reviewed head: `2cdbf49`; web ChatGPT result: REQUEST_CHANGES because checksum wording in `PROJECT_STATUS.md` contradicted the newly captured Phase 2 checksums.
- Fix reviewed head: `bfcdd89`; web ChatGPT result: APPROVE in the existing conversation “PR审核与错误反馈”.
- Scope: download/checksum and audit GSE224235 coverage; document 17 samples, 8 matched pairs and only 2/10 locked-marker coverage as `INSUFFICIENT_FOR_FULL_STATE_VALIDATION`. No progress increase, target ranking or clinical conclusion.
## PR #64 — HTAN source-cohort replication audit

- URL: [#64](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/64)
- Initial reviewed head: `fffe070`; web ChatGPT result: REQUEST_CHANGES because HTAN is the source study for the marker set and cannot count as independent validation.
- Final reviewed head: `40b29c6`; web ChatGPT result: APPROVE after aligning script/report/PR wording, synchronizing with main and keeping progress at 97/100. Independent validation remains open.

## PR #65 — HPA normal-tissue target audit

- URL: [#65](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/65)
- Initial reviewed head: `d32ade5`; web ChatGPT result: REQUEST_CHANGES because archive return codes and missing-target behavior were not fail-closed.
- Final reviewed head: `55fb4fd`; web ChatGPT result: APPROVE after checking archive return codes, failing on missing RNA targets and explicitly recording IHC targets without records. Overall progress remains 97/100.
- Scope: capture official HPA v25.1 RNA tissue and normal IHC provenance/checksums and audit normal-tissue coverage for six exploratory state markers. No therapeutic-window, safety, target-approval or clinical conclusion.

## PR #67 — superseded CRLM validation submission

- URL: [#67](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/67)
- Closed without merge because the reused branch name pointed to the prior HTAN head `40b29c6` instead of the CRLM commit. The corrected submission was made as PR #68 on a unique branch.

## PR #68 — external CRLM cohort coverage audit

- URL: [#68](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/68)
- Initial reviewed head: `c24ad0a`; web ChatGPT result: REQUEST_CHANGES because CRLM-versus-adjacent-liver is not equivalent to the locked primary-versus-metastasis contrast, so it could not count as independent validation or raise progress to 98/100.
- Final reviewed head: `87ba899`; web ChatGPT result: APPROVE after synchronizing PR metadata, manifest wording and project status to external cohort coverage/descriptive audit, with progress at 97/100.
- Scope: capture and audit an external CRLM cohort; no independent-validation, causal, target-ranking, therapeutic-window or clinical conclusion.

## PR #70 — Pivot to ADC Target Repurposing Atlas (Modules B-F)

- URL: [#70](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/70)
- Initial reviewed head (round 1): initial pivot commit; web ChatGPT result: REQUEST_CHANGES — target-first existed only in prose (no target_id data model, hardcoded Module A paths), module_classification.tsv had no schema/vocabulary and conflicted with datasets.tsv.priority, PROJECT_STATUS.md/knowledge/README.md still presented old Phase 2 state as current, 3 live scripts still defaulted to the old Fig1 marker panel, .gitignore dropped legacy ignore patterns.
- Round 2 head `c7dbdaf`: web ChatGPT result: REQUEST_CHANGES — confirmed the pivot direction was now real, but target_evidence.tsv lacked indication_id/evidence_directness, Module C conflated response-association with persistence, Module B's surface-density wording was scientifically loose, Module A lacked an admission tier, plus a consistency batch.
- Round 3 head `9d47d1e`: web ChatGPT result: REQUEST_CHANGES — independently verified the new candidate datasets against official sources (no issue there); GSE274551 (and GSE178318/GSE225857/GSE294385 in Module C) was mislabeled persistence when it is a single-timepoint refractory-tissue biopsy per official GEO design; B_PRECLINICAL_ADC's admission rule allowed antibody-internalization alone; a "the two CORE_ACTIVE modules" claim was factually wrong.
- Final reviewed head (round 4) `b00d7ec`: retired the persistence axis into longitudinal_persistence (GSE84267 only) and refractory_or_treated_presence (GSE274551/GSE178318/GSE225857/GSE294385); tightened B_PRECLINICAL_ADC to require real preclinical ADC construct evidence; fixed the CORE_ACTIVE wording. Web ChatGPT result: **APPROVE** — no new blockers, explicitly cleared for merge.
- Scope: restructure the repository around Modules A-F of the ADC Target Repurposing Atlas per `Asset-Generation-OS-architecture.md`; archive the old Phase 2 fetal-state/plasticity discovery track (not deleted); add machine-checkable module_classification/target_seed/target_evidence contracts; register 13 new CANDIDATE datasets (source-manifest only, not source-verified, no download authorized). No biological data, no target ranking, no clinical conclusion.

## PR #71 — Phase 1 source verification for 13 pivot-added candidates

- URL: [#71](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/71)
- Initial reviewed head `51b9d8a`: web ChatGPT result: REQUEST_CHANGES — GSE235917 was registered as tumor-cell-localization support but is PBMC/TIL (immune-cell) scRNA-seq; GSE225857's treatment_annotation was wrongly downgraded to UNKNOWN when GEO's Overall design already states it; CPTAC_COAD's publication-only verification was folded into a "13/13 complete" claim; plus GSE196576 sample-count and GSE5851 citation cleanups.
- Round 2 head `f8577d6`: web ChatGPT result: REQUEST_CHANGES — confirmed all 5 round-1 items landed correctly (independently re-verified GSE225857, GSE196576, GSE5851 against official sources), but GSE196576.primary_or_metastatic was still oversimplified as PRIMARY (GEO's design is mixed primary/metastatic/unknown-origin) and CPTAC_COAD's module_classification.tsv reason still said "source-verified."
- Final reviewed head `2a93817` (round 3): fixed both remaining items. Web ChatGPT result: **APPROVE** — one non-blocking wording note (fixed in the same commit before merge).
- Scope: verify all 13 Phase-1 candidates against official landing pages/publications; propagate newly-discovered facts into canonical fields, including downgrading GSE235917 out of its previous (incorrect) Module C role. No biological data downloaded, no candidate reached APPROVED.

## PR #72 — Module A: ADC_TARGET_SEED_UNIVERSE.tsv v1 build

- URL: [#72](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/72)
- Initial reviewed head `01aa76b`: web ChatGPT result: REQUEST_CHANGES — the generator wasn't fail-closed for a canonical artifact (hardcoded env var names instead of reading config/external_sources.yaml, warned-and-skipped instead of hard-failing on a missing/extra crossref row or vanished antigen file), human_adc_exposure_evidence was unconditionally YES (upgrading "clinical stage exists" into "documented human exposure"), the cancer-type distillation had three live bugs (a negative-context indication string counted as CRC-positive precedent, split(";") shredding a cytogenetic-notation label, cap=8 not actually bounding total shown terms), and the PR wasn't draft.
- Round 2 head `a100198`: builder now reads path_env_var from the YAML and hard-fails on any candidate/crossref reconciliation drift or vanished antigen file; crossref gained an explicit resolution_status column (27 RESOLVED_DIRECT / 2 RESOLVED_BACKLINK / 1 UNRESOLVED_SOURCE_GAP); human_adc_exposure_evidence now YES only for targets with an approved asset (UNKNOWN for the 12 clinical-stage-only targets); all three distillation bugs fixed with new regression tests; PR reverted to draft. Web ChatGPT result: **APPROVE** — no new blockers, confirmed all four items genuinely fixed.
- Scope: generate DATA/registry/ADC_TARGET_SEED_UNIVERSE.tsv (23 A_CLINICAL/ACTIVE targets) from the two Module A sources declared in config/external_sources.yaml, joined against a checked-in, source-verified asset-antigen crossref and a UniProt accession map. 5 targets (CEACAM5, ERBB2, F3, NECTIN4, TACSTD2) carry real, source-recorded CRC/mCRC trial precedent (indication text only, not an efficacy claim). Explicitly scoped to the ~30-asset clinically-derisked slice, not ADCdb's broader ~300-antigen pool.

## PR #73 — First Module B + E vertical slice: tgt_ceacam5 (CEACAM5)

- URL: [#73](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/73)
- Initial reviewed head `01aa76b`: web ChatGPT result: REQUEST_CHANGES — TE001/TE002 used a different indication_id than Module B, splitting one target into two dossiers; the HPA RNA file was mislabeled "consensus" and the data lock wrongly said IHC was unavailable when this repository's own source_manifest.tsv already recorded it as downloaded; two claims drifted into a proxy upgrade; Module B's blocker description contradicted this repository's own GSE178318 source_manifest.tsv, which records its matrix/genes/barcodes as already downloaded and checksum-verified.
- Round 2 head `32c4c1c`: TE001-TE003 unified on one indication_id; real HPA cell-type-resolved IHC evidence added (TE003) after confirming the file is genuinely present locally; HPA RNA product renamed correctly; GTEx manifest backfilled; proxy-upgraded claims reworded; Module B data lock corrected to distinguish GSE178318 (data present, cell-type annotation is the real gap) from GSE225857 (genuinely no local data); prior_therapy ontology field loosened to match source support. Web ChatGPT result: REQUEST_CHANGES — one remaining item: TE003 was CALIBRATED_PROXY with no actual calibration step behind it; "resolves" language still too strong in places; PR description still stale.
- Final reviewed head `7474004` (round 3): TE003 corrected to UNCALIBRATED_PROXY; "resolves/confines" language replaced with "does not corroborate ... lowers but does not eliminate the concern" everywhere it appeared; PR description synced. Web ChatGPT result: **APPROVE** — confirmed no fix-vs-document drift; recommended next step is completing GSE178318's malignant/epithelial cell annotation to close this one vertical slice (Module A → B → E for CEACAM5) before replicating to the other four targets.
- Scope: first real target_id x indication_id (tgt_ceacam5 x mcrc_preop_chemotherapy_crlm) through Modules B and E. Module E produced 3 real target_evidence.tsv rows (RNA + HPA cell-type IHC, all evidence_directness=UNCALIBRATED_PROXY) from already-locally-present official sources. Module B honestly recorded as blocked on malignant-cell annotation (GSE178318, data present) and data access (GSE225857, data absent) — no fabricated row.

## PR #74 — GSE178318 epithelial-proxy screen for tgt_ceacam5

- URL: [#74](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/74)
- Initial reviewed head `cf2b6a6`: web ChatGPT result: REQUEST_CHANGES — independently fetched GSE178318's own publication (also found and flagged a non-existent DOI previously recorded in this repo's own source_manifest.tsv) and found the method fell below the dataset's own published standard: no QC filtering applied (paper filters to 111,292 of 140,281 cells via explicit thresholds), a scoring-math bug where every category divided by the same denominator so it cancelled out of the argmax comparison (structurally favoring categories with more marker genes), an epithelial marker panel that risked misclassifying normal hepatic epithelium in liver-metastasis samples, and treatment-naive patients folded into a treatment-defined indication_id with only a notes-field caveat.
- Round 2 head `2ab59fa`: applied the paper's own QC thresholds (>=500 detected genes, <=15% mito UMI, per-sample 3-SD outlier removal; 123,330/140,281 pass); epithelial identification switched to EPCAM alone (matching the paper's method); scoring fixed to a marker-average, resolving the denominator-cancellation bug; treated (COL15/COL17/COL18, TE004) and treatment-naive (COL07/COL12/COL16, TE005, re-keyed to indication_id=mcrc_liver_metastasis) split into separate rows; fixed the wrong DOI; reframed the PR as an "epithelial-proxy screen, not malignancy-confirmed" rather than claiming the vertical slice closed. Web ChatGPT result: **APPROVE** — confirmed all four items genuinely fixed; two small non-blocking wording/maintenance notes (QC description overstated as verbatim paper thresholds; unused marker-panel rows not marked as reference-only) applied before merge.
- Scope: real QC-filtered, EPCAM-based epithelial-proxy screen of GSE178318 for CEACAM5, explicitly not malignancy-confirmed (no InferCNV reproduced) — Module B's actual malignant-cell prevalence question for this target remains open. Corroborating signal: post-correction epithelial-proxy cell counts are low and concentrated in COL15, directionally matching the source paper's own reported EPC distribution among treated patients.

## PR #75 — CNV-lite malignancy confirmation attempt for tgt_ceacam5

- URL: [#75](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/75)
- Initial reviewed head `2fdb7d8`: web ChatGPT result: REQUEST_CHANGES — six items: `resolve_hgnc_path()` hardcoded the `HGNC_GENE_ID_MAPPING_PATH` env var name instead of reading it from `config/external_sources.yaml` (recurrence of the PR #72 round-1 bug class); no checksum lock on the external HGNC reference file; fit-half/holdout-half bookkeeping self-contradiction (reported "reference" numbers came from the fit half while the threshold came from the holdout half, and a fit-half p99 was wrongly called "the threshold, by construction"); "~1% of epithelial-proxy cells clear the threshold" reported without the reference's own exceedance rate at that threshold (the null expectation by construction); output file/console text used "confirmed" language contradicting the PR's own "not confirmatory" conclusion; the "no cross-cell smoothing" explanation mischaracterized real InferCNV's actual primary mechanism (within-cell, genome-ordered smoothing, not cross-cell clustering); one numeric typo (25,390 vs. the canonical 25,376).
- Round 2 head `97c6aa7`: all seven items fixed — config actually parsed via a new `load_gene_position_source_config()`; HGNC file checksum-locked (`DATA/reference/hgnc_gene_id_mapping_source_lock.tsv`); all "reference" comparison numbers switched to the held-out half (n=38,281) consistently; exact exceedance fractions reported (epithelial-proxy 122/9,973=1.22% vs. held-out reference 382/38,281=1.00%, enrichment ratio 1.23x); output renamed to `tgt_ceacam5_cnv_lite_attempt.tsv`; InferCNV-mechanics explanation corrected (missing within-cell gene-order/moving-window smoothing and centering/reference-subtraction, not "no cross-cell smoothing"); 25,376 typo fixed. Web ChatGPT result: REQUEST_CHANGES — confirmed all seven fixes landed, but found a new blocker: `TE006`/`EV014` are keyed to the treated-cohort `indication_id=mcrc_preop_chemotherapy_crlm` (same as `TE004`), but the script's reference and epithelial-proxy populations were never actually restricted to the 3 treated patients (`COL15`/`COL17`/`COL18`) — both pooled all 6 patients, so the reported n=9,973 population was 82% (8,187/9,973) treatment-naive cells reported under a treated-only dossier, the same class of cohort-mismatch bug PR #74 round 1 caught. Also flagged stale GitHub PR title/description (still round-1 "underpowered" text).
- Final reviewed head `3b9cfde` (round 3): added `build_populations()`/`score_population()` helpers, splitting the script into a canonical treated-only run (both populations restricted to `COL15`/`COL17`/`COL18`) and a pooled six-patient diagnostic (explicitly non-canonical, stderr-only, never written to the output TSV or `TE006`/`EV014`). Re-run on LOCAL: treated-only reference n=38,003 (held-out half n=19,002), threshold=12.54, epithelial-proxy n=1,786, median 1.32 vs. held-out reference median 0.63 (~2.1x), CNV_HIGH 36/1,786 (2.02%) vs. held-out reference's own 190/19,002 (1.00%), enrichment ratio 2.02x — a modestly clearer separation than the earlier mistaken pooled 1.23x, but the same conclusion. Propagated to the analysis contract, `TE006`/`EV014`, module docs, `PROJECT_STATUS.md`; GitHub PR title/description synced. Web ChatGPT result: **APPROVE** — confirmed the cohort mismatch was fixed at the execution layer (not just documentation), `indication_id` now matches the actual computed population, and the evidence level was not upgraded just because the treated-only enrichment (2.02x) looked stronger than the mistaken pooled number (1.23x) — still `UNCALIBRATED_PROXY`/`EXPLORATORY_UNDERPOWERED`/`LOW`. One non-blocking note: `evidence_level=EXPLORATORY_UNDERPOWERED` doesn't fully capture that the ambiguity is resolution + lineage confounding, not just statistical power — not worth a controlled-vocabulary redesign to block on. Recommended next step: stop iterating CNV-lite further (risk of local overfitting to this one 6-patient cohort); prioritize unblocking `GSE225857` (a second, independent, treatment-exposed CRLM cohort) over a CNV-lite v2/v3.
- Scope: chromosome-arm-level CNV score (gene→arm mapping via local HGNC gene-position reference) as a coarser, independently-designed approximation of GSE178318's own fine-grained InferCNV — not a reproduction. Honest result: ambiguous, nonconfirmatory CNV-like score shift in treated-cohort epithelial-proxy cells, not a confirmed malignant-cell prevalence number. New `target_evidence.tsv` row `TE006` (`evidence_level=EXPLORATORY_UNDERPOWERED`), backed by `EV014`; does not supersede `TE004`/`TE005`. Module B's malignant-cell prevalence question for `tgt_ceacam5` remains open.

## PR #76 — Module B + E for the remaining four targets (ERBB2, F3, NECTIN4, TACSTD2)

- URL: [#76](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/76)
- Initial reviewed head `651ae72`: web ChatGPT result: REQUEST_CHANGES — the breadth-first scope decision itself was accepted (explicit user direction supersedes PR #75's earlier "don't batch-run" recommendation), and Module B's four new epithelial-proxy screens were fine, but Module E had three issues: (1) F3's IHC row was coded `evidence_directness=UNCALIBRATED_PROXY` despite its own `structured_value` recording `usable_data=NONE` — "no evidence" miscoded as "weak evidence," should be `UNKNOWN`; (2) several canonical claims asserted uncited external clinical-toxicity/biology causality (ERBB2's HPA IHC finding framed as "reproduces a known, real liability" of clinical anti-HER2 ADCs; similar claims for NECTIN4/TACSTD2/F3) — one of them (TACSTD2/sacituzumab govitecan) was also factually wrong, since its urothelial-cancer indication was voluntarily withdrawn (FDA 2024) and its actual boxed-warning toxicities are neutropenia/diarrhea, not skin; (3) two internal contradictions — a false "TACSTD2 is the only target with IHC-High" claim (`CEACAM5` already has 12 from PR #73) and NECTIN4/TACSTD2 both claiming "no GI tissue scored High/Medium" while listing Esophagus (GI tract) as Medium in the same sentence.
- Round 1 head `bd7eff2`: `TE014.evidence_directness` → `UNKNOWN`; removed the visible causal clinical-toxicity claims from ERBB2/NECTIN4/TACSTD2; corrected TACSTD2's factual error; fixed both internal contradictions. Web ChatGPT result: REQUEST_CHANGES — confirmed most fixes landed, but found residual uncited external claims (ERBB2's IHC row still called cardiomyocytes/alveolar cells "clinically-monitored toxicity domains for approved anti-HER2 ADCs"; F3 still said its RNA pattern "matches known F3 biology"; all four `question.md` files still asserted external drug/clinical facts even after TACSTD2's factual correction), a literal self-contradiction in TACSTD2's RNA claim ("skin is the single highest, but esophagus is higher still"), and a stale GitHub PR description.
- Final reviewed head `491794f` (round 2): stripped the remaining uncited external clinical/biology claims from ERBB2 and F3's canonical evidence; rewrote all four `question.md` files to reference Module A (`ADC_TARGET_SEED_UNIVERSE.tsv`, already source-verified) instead of restating drug/clinical facts in a Module E document; fixed the TACSTD2 wording self-contradiction; synced the GitHub PR description. Web ChatGPT result: **APPROVE** — confirmed all three round-1 items genuinely fixed: F3/`TE014` correctly `UNKNOWN` with `usable_data=NONE` preserved, ERBB2's IHC row reports only the HPA finding itself, all four `question.md` files properly defer to Module A, TACSTD2's RNA claim is now logically consistent. One non-blocking wording note (bulk RNA alone can't itself prove an epithelial-cell source, though the same dossier's IHC row does and is cross-referenced) — not worth a further round. Recommended next step: the five CRC-precedented targets now all have comparable Module B+E screening evidence; move to horizontal decision/pruning (comparing which targets are near KILL/HOLD/worth advancing) rather than continuing to add same-type evidence per target.
- Scope: same corrected Module B (QC-filtered epithelial-proxy screen, treated/treatment-naive split) + Module E (HPA RNA/IHC + GTEx) method as `tgt_ceacam5`, applied to `ERBB2`/`F3`/`NECTIN4`/`TACSTD2`. 20 new `target_evidence.tsv` rows (`TE007`-`TE026`), 20 new `evidence.tsv` rows (`EV015`-`EV034`) — 19 `UNCALIBRATED_PROXY`, one `UNKNOWN` (F3's IHC gap). No CNV-based malignancy confirmation attempted for any of the four. All canonical evidence reports only the HPA/GTEx/GSE178318 finding itself, with external ADC precedent left to Module A and no clinical-toxicity causal claims. Real findings: ERBB2 IHC signal in cardiomyocytes/lung alveolar cells; NECTIN4/TACSTD2 strong skin signal (TACSTD2 also broad non-colorectal epithelial expression, esophagus RNA the single highest of any tissue); F3 has no usable HPA IHC data (explicit `UNKNOWN`); `GSE178318`'s gene index carries `NECTIN4` under its prior symbol `PVRL4` (resolved, documented).

## PR #77 — Horizontal evidence-pattern comparison across five CRC-precedented targets

- URL: [#77](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/77)
- Initial reviewed head `40570d4`: web ChatGPT result: REQUEST_CHANGES — clean scope (new comparison report only, no evidence data touched), but the substance had pushed "five targets now have structurally parallel evidence" into "can be quantitatively ranked against each other," which the evidence does not support: (1) Module B's cross-target prevalence ranking was uncalibrated — the five genes differ in transcript abundance, dropout propensity, and dynamic range, so a higher RNA detection fraction for one gene over another cannot license a "stronger/weaker biological prevalence" claim, let alone a deprioritization call for `NECTIN4`; (2) Module E's HPA IHC High/Medium levels come from different antibodies per target and are not a cross-target intensity scale — `TACSTD2` "High" cannot be quantitatively asserted as stronger accessible-antigen exposure than `ERBB2` "Medium," and the document's own later disclaimer ("Module E cannot establish accessible antigen density") directly contradicted its earlier "highest-intensity"/"risk-benefit least favorable" language; (3) a conceptual error treating `CEACAM5`'s normal-tissue signal being anatomically concentrated in the indication's own organ as resolving normal-tissue risk — normal colon/rectum is still normal tissue, and treating organ-overlap with the tumor as inherently safe is a dangerous heuristic. Recommended reframing the whole document from "target pruning lean" to "evidence-based next-step prioritization."
- Round 1 head `aa3a140`: retitled Module B's section to make explicit it is an uncalibrated cross-target RNA detection-fraction screen, not a prevalence ranking (decision language removed, raw table kept); retitled Module E's section to keep only within-target tissue/cell-type distribution counts, removing all cross-target intensity/risk-benefit language; corrected CEACAM5's framing to "pattern is anatomically concentrated, safety implication remains unresolved"; reframed the entire document as "next-uncertainty prioritization." Web ChatGPT result: REQUEST_CHANGES — confirmed the core restructuring was correct, but found one real remaining blocker (the newly-introduced "only safe cross-target metric," a count of distinct tissues with IHC High/Medium, was itself miscounted — `TACSTD2` was called broadest but `ERBB2`'s own table actually lists more distinct tissues, 13 vs. 9) plus two small issues (the file was still named `TARGET_PRUNING_COMPARISON.md`, a semantic trap given the reframing; "comparable Module B + E evidence" could be misread as claiming calibration).
- Round 2 head `400be1d`: recounted distinct HPA tissues with >=1 High/Medium row using a precisely-defined rule — `ERBB2` 13, `TACSTD2` 9, `CEACAM5` 6, `NECTIN4` 6, `F3` unmeasured — and corrected the "TACSTD2 broadest" claim; renamed the file to `TARGET_EVIDENCE_PATTERN_COMPARISON.md`; reworded "comparable" to "structurally parallel"; removed an unsupported "lowest-cost" claim. Web ChatGPT result: REQUEST_CHANGES — confirmed all three items fixed correctly, but caught a fresh, narrow contradiction the round-2 table fix itself introduced: the prose said CEACAM5's 6-tissue footprint "sits entirely inside colorectal/appendix tissue," directly contradicted by the same table two lines above it, which lists Esophagus/Oral mucosa/Stomach among CEACAM5's 6 tissues.
- Final reviewed head `8be320b` (round 3): split the sentence into two precise claims — CEACAM5's High-level IHC calls are restricted to Appendix/Colon/Rectum, while its full High+Medium footprint also includes Esophagus/Oral mucosa/Stomach ("GI/oral-mucosal concentrated," not "entirely colorectal/appendix"). Web ChatGPT final review: **APPROVE** — confirmed every evidence boundary established across the four rounds still holds: Module B stays an uncalibrated per-gene detection-fraction screen, Module E's High/Medium is never a cross-antibody intensity scale, the tissue-breadth count is internally consistent, CEACAM5's anatomic concentration is not misread as a safety resolution, F3 stays a genuine `UNKNOWN`, and the final output is next-uncertainty prioritization, not `KILL`/`HOLD`/`SHORTLIST`. Explicit takeaway: the report's real value is turning "what's still missing" into a target-specific next-acquisition strategy, not a ranking.
- Scope: reads already-collected Module B + E evidence for all five targets side by side — no new data, no script runs. Establishes, and after four review rounds actually enforces, the comparability limits this kind of cross-target synthesis needs: RNA detection fractions are per-gene and uncalibrated; IHC categorical levels are per-target/antibody and uncalibrated; anatomic overlap with the tumor site does not resolve normal-tissue risk. Final framing is next-uncertainty prioritization (which target's next piece of evidence is most worth getting), explicitly not a `KILL`/`HOLD`/`SHORTLIST` decision.

## PR #78 — GSE225857 CNSA access-terms review

- URL: [#78](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/78)
- Initial reviewed head `46ca3d5`: web ChatGPT result: REQUEST_CHANGES — independently re-verified `GSE225857`'s CNSA/CNGBdb access terms (the previously-recorded `source_url` was itself a dead 404 link; found the real `db.cngb.org` project pages) and found three real issues: (1) the conclusion "extending Module B requires a DAC application" overclaimed — the reviewer independently checked `GSE225857`'s own GEO record and found GSM7058754 (immune)/GSM7058755 (non-immune) each publicly provide a downloadable count matrix + per-cell metadata with no access request needed, a real, unverified, materially cheaper alternative route that the "must file DAC" conclusion ignored; (2) "outside what this repository or its operator can satisfy directly (no Chinese-institution affiliation on record here)" was an unsupported eligibility inference — the CNGBdb policy text states controlled data accepts user access requests generally, subject to submitter approval and applicable-law/HGR compliance, not a stated institution-nationality bar; (3) `CNP0002540` (scRNA-seq) and `CNP0003321` (spatial transcriptomics) — two different-modality assets — were combined into one provenance row with only one accession's `source_url`, insufficiently auditable; should be split like the existing `GSE117548`/EGA one-row-per-source-route pattern.
- Round 1 head `408fb36`: independently re-verified the reviewer's GEO findings before fixing (confirmed exact file sizes: 213.9MB+9.6MB and 86.2MB+1.9MB; GEO's own Data Processing field: "Matrix table with raw UMI counts and metadata for every cells"); separated the confirmed fact (CNSA route is `CONTROLLED_ACCESS`) from the unverified claim (whether Module B needs that specific route), rewriting the latter to `UNKNOWN` with the correct cheaper next step recorded (check the two public metadata files' columns before considering a DAC application); removed the unsupported eligibility inference, keeping only what the CNGBdb policy text actually states; split `CNP0002540`/`CNP0003321` into two separate provenance rows, each with its own `source_url`/size/access notes. Web ChatGPT result: REQUEST_CHANGES — confirmed all three round-0 issues genuinely fixed, but found a new, narrower provenance-semantics problem the fix itself introduced: it still called GSM7058754/GSM7058755 a "public raw data" / "raw UMI count matrix" route, but GEO's own per-GSM pages also state "Raw data not provided for this record" / "Processed data provided as supplementary file" — these are processed-data supplementary files whose cell values happen to be raw (unnormalized) UMI counts, not raw sequencing reads; the CNSA route is the actual raw sequencing-data route under `CONTROLLED_ACCESS`. Requested minimal terminology fixes throughout plus a narrower PR title reflecting that the controlled-access blocker is a property of the CNSA raw-sequencing route, not of `GSE225857`'s overall data availability.
- Final reviewed head `c17a0e3` (round 2): fixed the raw-vs-processed terminology throughout `source_manifest.tsv`, `no_file_inventory_disposition.tsv`, `PROJECT_STATUS.md`, `knowledge/README.md`, and `data_lock/tgt_ceacam5.md` per the reviewer's exact wording ("processed count matrix (raw UMI counts, per GEO's own field name)"; "a public processed count-matrix + per-cell metadata route, not a public raw-sequencing-data route"; "publicly accessible processed count/meta files are available without an access request"; CNSA consistently called the "raw sequencing-data route"); narrowed the PR title to "GSE225857 CNSA raw-data access review -- CONTROLLED_ACCESS; public GEO processed route remains open". Web ChatGPT final review: **APPROVE** — confirmed the provenance boundary is now clean: GEO is a public processed count-matrix + per-cell metadata route (values are raw UMI counts, files are processed supplementary data); CNSA is the raw sequencing-data route, `CNP0002540`/`CNP0003321` recorded separately, both `CONTROLLED_ACCESS`; CNSA being controlled-access does not by itself mean `GSE225857` is unusable for Module B, and whether the public GEO route suffices stays explicitly `UNVERIFIED`. One non-blocking wording note (`tgt_ceacam5.md`'s "raw single-cell sequencing data" phrase loosely folds spatial data in, though the same sentence already names `CNP0003321` as spatial separately — not worth another round). Explicit next step: not further access archaeology or a DAC application, but a small GEO-metadata sufficiency check — open `GSM7058754_immune_meta.txt.gz`/`GSM7058755_non_immune_meta.txt.gz` and see whether they already carry patient/site/treatment labels; if so, the `GSE225857` "institutional-access blocker" may resolve itself without ever touching CNSA.
- Scope: pure provenance/access-terms review, no data downloaded, no biological analysis. Splits `GSE225857`'s CNSA-hosted raw sequencing data (`CNP0002540` scRNA-seq 2.38TB, `CNP0003321` spatial 396.46GB) into two auditable `CONTROLLED_ACCESS` provenance rows (DAC application to the original submitter, Wang Fei/Guangdong Academy of Medical Sciences, plus China HGR compliance — applicant eligibility and exact filing obligations left explicitly unresolved). Establishes and enforces a precise raw-sequencing-data-vs-processed-data provenance boundary for `GSE225857`'s public GEO route (GSM7058754/GSM7058755 pooled scRNA count matrices + per-cell metadata, GSM7058756-761 per-sample spatial matrices) as a real, cheaper, still-unverified alternative to filing a CNSA DAC application — recorded as the next concrete artifact in `no_file_inventory_disposition.tsv`, not yet executed.

## PR #79 — GSE225857 public GEO metadata sufficiency check

- URL: [#79](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/79)
- Initial reviewed head `ed424f8`: actually downloaded (real SHA256, gzip-integrity-verified; raw files stay in the already-gitignored `modules/*/data_lock/raw/` pattern, not committed) and column-inspected the two public, no-access-request-needed `GSE225857` metadata files GEO's own record described (`GSM7058754_immune_meta.txt.gz`, `GSM7058755_non_immune_meta.txt.gz`), per PR #78's round-3 reviewer's own explicit next step. Confirmed real patient- and site-level resolution: a `patients` column (7 distinct IDs in the immune file, 5 in the non-immune file), an `organs`/`samples` column (5 site codes in the immune file — CCL/CNL/LCL/LNL/PBL; 2 in the non-immune file — CCT/LCT), and a `patients_organ` combined key. Site codes independently cross-checked against the source publication's methods text (Wang et al., *Sci Adv* 2023, PMID 37327339: primary colorectal cancer / adjacent normal colon / liver metastasis / adjacent normal liver / peripheral blood, CD45+ immune vs. CD45- non-immune sorted fractions), and row counts match the publication exactly (196,473 immune + 41,892 non-immune cells). Recorded one honest, unresolved discrepancy (metadata carries 7 patient IDs against the publication's stated "six patients") rather than investigating or explaining it away. No per-cell treatment column exists, but none is needed since the registry's series-level `treatment_annotation` already applies uniformly. Also transitioned `GSE225857` from `no_file_inventory_disposition.tsv` (deleted) to a real `file_inventory.tsv` (2 rows), matching the same file-inventory-vs-disposition binary convention every one of the registry's 32 datasets already follows.
- Web ChatGPT result: **APPROVE** — clean scope (only the two public metadata files materialized, no count-matrix biological analysis smuggled in); independently confirmed the external-source framing (the publication's own CC-vs-LM nonimmune comparison is itself n=5 patients, so 5 IDs in the non-immune metadata isn't a new anomaly); endorsed the file-inventory transition. Two non-blocking guardrails for the next PR, folded in before merge (head `d31a2ad`, matching the established practice from PR #71 round 3 / PR #74 round 2 of applying non-blocking notes pre-merge rather than opening another round): (1) keep the metadata's 7-vs-6-patient discrepancy explicitly unresolved, don't silently treat the immune file as 7 independent patients before reconciling it; (2) narrow the next concrete step — prioritize downloading only `GSM7058755_non_immune_counts.txt.gz` (86.2 MB) first, not both count matrices, and before rebuilding a fresh EPCAM-only proxy, check whether the metadata's `cluster` column already carries author-provided tumor-cell/fibroblast/endothelial labels reusable directly. Checked at zero additional cost against the already-downloaded metadata: it does — 11 `Tu01`-`Tu11` tumor clusters, exactly matching the publication's stated "11 tumor cell clusters"; 6 `E01`-`E06` endothelial clusters, also an exact match; 6 `F01`-`F06` fibroblast clusters against the publication's stated 8 (not reconciled). Merged.
- Scope: opens and inventories exactly two small, public metadata files; no count matrix opened, no target-gene detectability confirmed, no biological analysis. Converts `GSE225857`'s CNSA access review from an open access-terms question into a scoped, ordered next step: download the non-immune count matrix, confirm cell-ID join, confirm the five `A_CLINICAL` targets exist in the gene index, confirm the author tumor-cell annotation is directly reusable, then compute prevalence — without ever needing to file a CNSA DAC application.
