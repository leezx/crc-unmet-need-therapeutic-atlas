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
