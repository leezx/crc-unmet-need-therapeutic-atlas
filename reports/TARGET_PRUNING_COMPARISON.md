# Horizontal target pruning comparison — five CRC-precedented targets

2026-08-24. First cross-target synthesis after PR #76: `CEACAM5`, `ERBB2`, `F3`, `NECTIN4`, `TACSTD2` now all have comparable Module B (prevalence) + Module E (normal-tissue risk) evidence for `indication_id=mcrc_preop_chemotherapy_crlm`. This compares them side by side — no new data, no new script runs; every number below already exists in `schemas/target_evidence.tsv` and its cited `analysis_contracts/tgt_<x>.md` files.

## What this is and is not

This is a **first-pass reading of already-collected evidence**, not a new evidence type and not a formal `KILL`/`HOLD`/`SHORTLIST` schema — no such schema exists yet in this repository. It is submitted for review the same way every other analytical claim in this repository is (`CRC临床适应症地图` conversation), because ranking targets against each other is a real judgment call, not a mechanical validator check, and deserves the same scrutiny as any other finding here.

Every input row is `evidence_directness=UNCALIBRATED_PROXY` (`F3`'s IHC row is `UNKNOWN`) and `evidence_level=SCREENING_LEVEL`. None of the five targets has malignancy-confirmed prevalence — all five Module B rows are the same EPCAM-based epithelial-proxy screen, not CNV-confirmed malignant-cell calling (`tgt_ceacam5` additionally has an ambiguous, nonconfirmatory CNV-lite attempt, `TE006`). **Nothing below should be read as a confirmed biological or clinical conclusion** — it is a relative comparison of screening-level signals, intended to help decide where further investment (Module C/D/F, or a higher-power malignancy-confirmation method) is best spent next, per `reports/PROJECT_STATUS.md`'s Next-handoff item 0.

## Prevalence (Module B): treated-cohort (`COL15`/`COL17`/`COL18`) epithelial-proxy positivity

QC and epithelial-proxy cell counts are identical across all five targets (same pipeline, target-independent) — only the gene-positive fraction differs. `n_epi` per sample: `COL15` 378/841 (primary/LM), `COL17` 50/25, `COL18` 132/360. `COL17`/`COL18`'s small `n_epi` (25-360 cells) make their fractions noisier than `COL15`'s (378-841 cells).

| Target | `COL15` CRC / LM | `COL17` CRC / LM | `COL18` CRC / LM | Samples at `RNA_no` (<5%) | Any `RNA_high` (>50%)? |
|---|---:|---:|---:|---:|---|
| `CEACAM5` | 59.5% / 33.3% | 20.0% / 12.0% | 35.6% / 23.1% | 0 of 6 | Yes — `COL15` CRC |
| `TACSTD2` | 24.9% / 17.2% | 8.0% / 20.0% | 3.0% / 4.4% | 2 of 6 (`COL18`) | No |
| `ERBB2` | 27.0% / 15.2% | 6.0% / 4.0% | 10.6% / 6.1% | 1 of 6 (`COL17` LM) | No |
| `F3` | 7.4% / 5.5% | 4.0% / 4.0% | 3.0% / 1.7% | 4 of 6 | No |
| `NECTIN4` | 9.0% / 4.6% | 0.0% / 4.0% | 0.0% / 1.1% | 4 of 6 (two at exactly 0%) | No |

`CEACAM5` is the only target with any `RNA_high` sample, and it is the largest/most reliable sample (`COL15` CRC, n=378). `TACSTD2` and `ERBB2` sit in a comparable moderate-but-patchy middle. `F3` and `NECTIN4` are both weak across the cohort — `NECTIN4` is the weakest overall, with two of six samples showing literally zero positive cells among the epithelial-proxy population.

## Normal-tissue risk (Module E): RNA + cell-type IHC pattern

| Target | Colon / rectum HPA RNA (nTPM) | IHC High/Medium rows (of total scored) | Pattern |
|---|---:|---:|---|
| `CEACAM5` | 920.3 / 885.1 (highest of 5, by far) | 18/109 — **12 High**, all Appendix/Colon/Rectum epithelium; 6 Medium | GI-restricted; the one non-GI RNA flag (lung) is *not* corroborated by IHC (lung alveolar cells both Low) |
| `TACSTD2` | 0.9 / 0.9 (lowest of 5) | 15/99 — **7 High**, all skin (two independent samples); 8 Medium spanning bronchus/cervix/esophagus/kidney/nasopharynx/oral mucosa/seminal vesicle/urinary bladder | Broadest non-colorectal footprint of any target; only other target besides `CEACAM5` with any IHC-High row |
| `ERBB2` | 63.8 / 45.5 (mid-range) | 19/126 — 0 High, **19 Medium** spanning cardiomyocytes/lung alveolar/breast/cervix/endometrium/fallopian tube/placenta/skeletal muscle/skin/testis/urinary bladder | Broadest organ *spread* of any target (no single dominant tissue), all Medium-level |
| `NECTIN4` | 1.4 / 1.6 (near-lowest) | 8/80 — 0 High, **8 Medium**, skin + upper-GI/oropharyngeal squamous (esophagus/oral mucosa/tonsil) | Narrower than `ERBB2`/`TACSTD2` — concentrated in skin/squamous epithelium, not multi-organ |
| `F3` | 35.6 / 39.5 (mid-low) | **No usable IHC data** (1 row, `Reliability=Uncertain`) | Genuine `UNKNOWN` at the protein layer — not favorable, not unfavorable, unassessed |

`CEACAM5` is the only target whose off-tumor signal is concentrated in the tissue the indication itself is defined by (colorectal) rather than spread across unrelated normal tissue. `TACSTD2` has the strongest single non-GI signal (IHC-High in skin, matched by nothing except `CEACAM5`'s own GI-High rows). `ERBB2` has the broadest multi-organ Medium-level spread. `NECTIN4`'s off-tumor signal is real but narrower (skin/squamous only). `F3` cannot be assessed at the protein level at all.

## Reading the two axes together

No target gets a hard `KILL` call from this pass — proxy-only, single-cohort, malignancy-unconfirmed evidence is not strong enough to eliminate a clinically-precedented target outright, and `n_epi`/`n=3 patients` limits are real. What follows is a relative lean, not a final decision:

- **`CEACAM5` — lean toward continued investment.** The only target combining a real, largest-sample prevalence signal (`RNA_high`) with a normal-tissue risk pattern that is tightly matched to the indication's own tissue. The open question is not normal-tissue risk or prevalence-screen existence — it's the malignancy-confirmation gap already tracked in `reports/PROJECT_STATUS.md` (CNV-lite `TE006` was ambiguous, not resolving it).
- **`TACSTD2` — lean toward caution.** Moderate, patchy prevalence signal paired with the single highest-intensity (IHC-High) off-tumor exposure outside `CEACAM5`, spread across skin and several other organs. The risk/benefit balance here looks the least favorable of the five on current evidence: a real accessible-antigen signal at High level, without a correspondingly strong or consistent tumor-side signal.
- **`ERBB2` — lean toward caution.** Consistently low-moderate prevalence (never `RNA_high`) paired with the broadest organ *spread* of Medium-level normal-tissue exposure of any target. Breadth itself is the concern here, independent of intensity.
- **`F3` — cannot currently support a confident call either way.** Weak, mostly-absent prevalence signal (4 of 6 samples `RNA_no`) combined with a genuine, unresolved gap on the protein-safety axis (no usable IHC at all). Both axes are underpowered; a different IHC source (research antibody study, separate tissue atlas) would be needed before this target's risk/benefit balance can be assessed properly, and this is very likely not worth the effort if it's the lowest-prevalence target regardless.
- **`NECTIN4` — weakest primary rationale.** Prevalence is the single most direct read on whether there is even a detectable tumor-positive population to target in this indication, and `NECTIN4`'s is the weakest of the five (two samples at exactly 0%). The off-tumor signal is real but narrower than `ERBB2`/`TACSTD2`'s. Of the five, this is the one where the evidence gathered so far most directly argues for deprioritizing *this specific indication* — though again, not a malignancy-confirmed negative, and could reflect this one 3-patient cohort rather than the target's true biology.

## What this comparison cannot do

- It cannot confirm or rule out malignancy for any target — every Module B row is an epithelial-proxy screen.
- It cannot establish a real therapeutic window, accessible antigen density, or clinical-toxicity risk for any target — Module E's RNA/IHC signals are screening-level, not calibrated surface-density or clinical-trial data (no external clinical claims are made anywhere in this repository's canonical evidence, per PR #76 round 2 review).
- It is a single-cohort (`GSE178318`) read for prevalence; `GSE225857`, the second, independent, treatment-exposed CRLM cohort, remains blocked on CNSA access for all five targets and could shift this comparison meaningfully once available.
- `F3`'s normal-tissue-risk axis is not "favorable" — it is simply unmeasured. Treating an `UNKNOWN` as equivalent to a Low/absent finding would be exactly the "no evidence coded as weak evidence" mistake PR #76 corrected in `TE014` itself.

## Suggested next step

Given the lean above, `tgt_ceacam5` and `tgt_nectin4` are the two clearest candidates for a next real decision: continue investing in `CEACAM5` (most likely via `GSE225857` once unblocked, rather than a further CNV-lite iteration per the PR #75 reviewer's own recommendation), and consider whether `NECTIN4`'s prevalence signal is weak enough in this indication to deprioritize it here specifically — not a judgment this repository should make unilaterally without review.
