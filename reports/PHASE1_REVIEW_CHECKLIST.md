# Phase 1 review checklist

Use this checklist in the draft PR that admits or changes a dataset candidate. It is a review gate, not an analysis output.

## Per-dataset checks

- [ ] Original publication inspected; DOI or stable citation recorded.
- [ ] Repository accession and landing-page URL verified.
- [ ] Human patient relevance confirmed, including primary vs metastasis and metastatic site.
- [ ] Treatment history and pre/post-treatment timing are explicitly documented or marked `UNKNOWN`.
- [ ] MSI/MMR and RAS/BRAF/HER2 annotations are explicitly documented or marked `UNKNOWN`.
- [ ] Patient/sample pairing fields are available or marked `UNKNOWN`.
- [ ] Processed files, metadata, and expected download size are listed.
- [ ] Raw-file need is justified; default remains processed-first.
- [ ] License, access restrictions, and citation requirements are recorded.
- [ ] Target-discovery contribution is stated as a specific uncertainty it closes.

## Decision

- `P0_DOWNLOAD`: high clinical relevance and directly actionable target-discovery evidence.
- `P1_DOWNLOAD`: useful orthogonal evidence after P0 review.
- `REFERENCE_ONLY`: comparator or safety reference; not a discovery cohort.
- `REJECT`: does not materially support the therapeutic question.

No dataset moves to `APPROVED` until this checklist is completed in a reviewed PR.
