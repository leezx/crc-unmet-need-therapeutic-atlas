# Horizontal evidence-pattern comparison — five CRC-precedented targets

2026-08-24. First cross-target synthesis after PR #76: `CEACAM5`, `ERBB2`, `F3`, `NECTIN4`, `TACSTD2` now all have structurally parallel Module B (prevalence-screen) + Module E (normal-tissue) evidence for `indication_id=mcrc_preop_chemotherapy_crlm` — same schema, same pipeline per module, run side by side, not a claim that the underlying measurement scales are calibrated across targets (see the two comparability limits below). This compares them side by side — no new data, no new script runs; every number below already exists in `schemas/target_evidence.tsv` and its cited `analysis_contracts/tgt_<x>.md` files.

**Update note (2026-08-24, PR #81, added after this document's own review completed):** `GSE225857` — described below as "blocked on CNSA access" — has since produced its own real result via GEO's public route (`TE027`-`TE031`, `modules/module_b_mcrc_target_prevalence/analysis_contracts/gse225857_tumor_cell_screen.md`), without ever needing CNSA. The body below is left as originally reviewed and approved; do not read its "blocked" mentions as current state.

## What this is and is not

This is a **first-pass reading of already-collected evidence**, reframed after round-1 review (below) from a "target pruning" comparison to a **next-uncertainty prioritization**: which target's next piece of evidence is most worth going and getting, not which target should be eliminated. It is not a new evidence type and not a formal `KILL`/`HOLD`/`SHORTLIST` schema — no such schema exists yet in this repository. It is submitted for review the same way every other analytical claim in this repository is (`CRC临床适应症地图` conversation), because comparing targets against each other is a real judgment call, not a mechanical validator check, and deserves the same scrutiny as any other finding here.

Every input row is `evidence_directness=UNCALIBRATED_PROXY` (`F3`'s IHC row is `UNKNOWN`) and `evidence_level=SCREENING_LEVEL`. None of the five targets has malignancy-confirmed prevalence — all five Module B rows are the same EPCAM-based epithelial-proxy screen, not CNV-confirmed malignant-cell calling (`tgt_ceacam5` additionally has an ambiguous, nonconfirmatory CNV-lite attempt, `TE006`). **Nothing below should be read as a confirmed biological or clinical conclusion.**

**Two comparability limits, not just a screening-level caveat, apply to everything below** (round-1 review, see "Review history" in `reports/PROJECT_STATUS.md`):

- The Module B numbers are each gene's own detection-fraction in the same epithelial-proxy cell population — the *pipeline* is identical across targets, but the five genes are not: baseline transcript abundance, scRNA-seq dropout propensity, and dynamic range differ per gene. A higher detection fraction for one gene than another is **not** license to say one target has "more prevalent" or "stronger" tumor-cell positivity than another — only that this assay detected it more often. No cross-gene calibration exists in this repository to make that inferential jump.
- The Module E IHC High/Medium levels come from different HPA antibodies per target, in different staining runs — they are categorical calls within one target's own antibody, not a quantitative scale calibrated across targets. `TACSTD2`'s "High" is not license to say it carries more accessible antigen than `ERBB2`'s "Medium" — that would need a real cross-target surface-density assay, which does not exist here.

## Cross-target observed RNA detection-fraction screen (Module B) — not a calibrated prevalence ranking

QC and epithelial-proxy cell counts are identical across all five targets (same pipeline, target-independent) — only each gene's own positive fraction differs. `n_epi` per sample: `COL15` 378/841 (primary/LM), `COL17` 50/25, `COL18` 132/360. `COL17`/`COL18`'s small `n_epi` (25-360 cells) make their fractions noisier than `COL15`'s (378-841 cells).

| Target | `COL15` CRC / LM | `COL17` CRC / LM | `COL18` CRC / LM | Samples at `RNA_no` (<5%) | Any `RNA_high` (>50%)? |
|---|---:|---:|---:|---:|---|
| `CEACAM5` | 59.5% / 33.3% | 20.0% / 12.0% | 35.6% / 23.1% | 0 of 6 | Yes — `COL15` CRC |
| `TACSTD2` | 24.9% / 17.2% | 8.0% / 20.0% | 3.0% / 4.4% | 2 of 6 (`COL18`) | No |
| `ERBB2` | 27.0% / 15.2% | 6.0% / 4.0% | 10.6% / 6.1% | 1 of 6 (`COL17` LM) | No |
| `F3` | 7.4% / 5.5% | 4.0% / 4.0% | 3.0% / 1.7% | 4 of 6 | No |
| `NECTIN4` | 9.0% / 4.6% | 0.0% / 4.0% | 0.0% / 1.1% | 4 of 6 (two at exactly 0%) | No |

Read within its own row (never across rows as a strength ranking): `CEACAM5`'s detection fraction reaches `RNA_high` in its largest sample; `TACSTD2`/`ERBB2` are moderate but patchy across samples; `F3`/`NECTIN4` are low across most samples, `NECTIN4` including two samples at exactly zero detected-positive cells. Whether that pattern reflects true biological prevalence differences between targets, or just each gene's own detectability in this assay, is exactly what an orthogonal, cross-gene-calibrated readout (a different platform, or protein-level detection) would need to resolve — this table alone cannot.

## Normal-tissue pattern (Module E): RNA + cell-type IHC, within-target distribution only

The only cross-target statement this section safely supports is a **count of distinct HPA tissues each target's own IHC scores at least one High/Medium cell-type row in** — a fixed, countable unit, not an intensity or risk comparison. Counted this way, from each target's own table:

| Target | Colon / rectum HPA RNA (nTPM) | IHC High/Medium rows (of total scored) | Distinct HPA tissues with ≥1 High/Medium row |
|---|---:|---:|---:|
| `ERBB2` | 63.8 / 45.5 | 19/126 — 0 High, 19 Medium | **13** — Appendix, Breast, Cervix, Endometrium, Fallopian tube, Heart muscle, Lung, Nasopharynx, Placenta, Skeletal muscle, Skin, Testis, Urinary bladder |
| `TACSTD2` | 0.9 / 0.9 | 15/99 — 7 High (skin only), 8 Medium | **9** — Skin (High), Bronchus, Cervix, Esophagus, Kidney, Nasopharynx, Oral mucosa, Seminal vesicle, Urinary bladder |
| `CEACAM5` | 920.3 / 885.1 | 18/109 — 12 High, 6 Medium | **6** — Appendix, Colon, Rectum (High); Esophagus, Oral mucosa, Stomach (Medium) |
| `NECTIN4` | 1.4 / 1.6 | 8/80 — 0 High, 8 Medium | **6** — Breast, Esophagus, Oral mucosa, Skin, Tonsil, Urinary bladder |
| `F3` | 35.6 / 39.5 | No usable IHC data (1 row, `Reliability=Uncertain`) | Genuine `UNKNOWN` at the protein layer — not favorable, not unfavorable, unassessed |

By this count, `ERBB2` actually has the broadest tissue footprint of the five (an earlier version of this document wrongly called `TACSTD2` the broadest — corrected in round 2 review), followed by `TACSTD2`; `CEACAM5` and `NECTIN4` are both narrower and roughly tied; `F3` is unmeasured. Two things this count does *not* support: it says nothing about exposure "intensity" (`TACSTD2`'s High-level calls and `ERBB2`'s Medium-level calls are not on the same measured scale — different antibodies, different staining runs), and it cannot establish accessible antigen density or a therapeutic window for any target (see "What this comparison cannot do"). `CEACAM5`'s High-level IHC calls are restricted to Appendix/Colon/Rectum, though its broader High/Medium footprint also includes Esophagus, Oral mucosa, and Stomach — GI/oral-mucosal concentrated, not literally confined to colorectal/appendix tissue (round-3 review correction: an earlier version of this sentence said the 6-tissue count "sits entirely inside colorectal/appendix tissue," which the table two lines above it already contradicts). The one non-GI RNA flag, lung, is not corroborated by IHC — lung alveolar cells both Low. `NECTIN4`'s narrow count is concentrated in skin/squamous epithelium instead.

## Reading the two axes together: what's actually worth doing next, not who should be eliminated

No target gets a `KILL`/`HOLD`/`SHORTLIST` call from this pass — the two axes above are screening-level, single-cohort, cross-target-uncalibrated, and malignancy-unconfirmed, which is not strong enough to rank or eliminate a clinically-precedented target. What each target's pattern actually argues for is a different **next piece of evidence**:

- **`CEACAM5`** — RNA detection is the most stable of the five in this assay (reaches `RNA_high` in the largest sample), and its normal-tissue signal is anatomically concentrated in colorectal/GI tissue rather than spread elsewhere. That concentration does **not** by itself resolve normal-tissue risk — normal colon/rectum is still normal tissue, and an accessible antigen there could still carry a real on-target/off-tumor liability regardless of anatomic overlap with the indication (treating organ-overlap as inherently safe would be a dangerous heuristic this repository should not encode). The pattern is anatomically concentrated; the safety implication (accessible antigen, tumor-normal differential, therapeutic window) remains unresolved. What's worth prioritizing next: an independent cohort (`GSE225857`, once unblocked) or real protein/surface evidence, rather than a further CNV-lite iteration (per the PR #75 reviewer's own recommendation).
- **`NECTIN4`** — the lowest RNA detection fraction of the five, including two samples at exactly zero. Worth prioritizing next: verifying whether this low signal actually replicates (a second cohort, or a different detection method) before drawing any conclusion about this target in this indication — a single low reading in a 3-patient cohort is itself an unconfirmed finding, not evidence to act on directly.
- **`ERBB2` / `TACSTD2`** — both show normal-tissue expression spanning many distinct tissues outside the indication's own organ (`ERBB2` the broadest of the five by tissue count, `TACSTD2` second). Worth prioritizing next: real, more direct surface/protein-density or clinical-context evidence before any further investment decision — categorical IHC breadth alone cannot support one.
- **`F3`** — the normal-tissue protein axis is a genuine `UNKNOWN`, not a clean result. Whether it is worth the effort to fill this gap (a different IHC source, a research antibody study) depends on whether `F3`'s other axes (or Module C/D findings) justify the investment first — this comparison alone does not settle that.

## What this comparison cannot do

- It cannot confirm or rule out malignancy for any target — every Module B row is an epithelial-proxy screen.
- It cannot rank targets against each other on either axis as a calibrated, cross-target quantitative scale — Module B's detection fractions are per-gene, uncalibrated across genes; Module E's IHC levels are per-target, antibody-specific categorical calls, not a shared intensity scale.
- It cannot establish a real therapeutic window, accessible antigen density, or clinical-toxicity risk for any target — Module E's RNA/IHC signals are screening-level, not calibrated surface-density or clinical-trial data (no external clinical claims are made anywhere in this repository's canonical evidence, per PR #76 round 2 review).
- It cannot treat a target's normal-tissue signal being anatomically concentrated in the indication's own organ as evidence that normal-tissue risk is resolved or reduced — normal tissue at the same anatomic site as the tumor is still normal tissue.
- It is a single-cohort (`GSE178318`) read for prevalence; `GSE225857`, the second, independent, treatment-exposed CRLM cohort, remains blocked on CNSA access for all five targets and could shift this comparison meaningfully once available.
- `F3`'s normal-tissue-risk axis is not "favorable" — it is simply unmeasured. Treating an `UNKNOWN` as equivalent to a Low/absent finding would be exactly the "no evidence coded as weak evidence" mistake PR #76 corrected in `TE014` itself.

## Suggested next step

Not a ranking or a decision this repository should make unilaterally — see the per-target "next piece of evidence" above. If forced to sequence, `CEACAM5`'s next step (an independent cohort or protein evidence) and `NECTIN4`'s next step (verifying whether its low detection fraction replicates) look like the two highest-information next checks under the current plan (no cost analysis backs a "lowest-cost" claim, and `CEACAM5`'s own suggested next step, `GSE225857`, is itself still blocked on CNSA access); `ERBB2`/`TACSTD2` need a materially different (protein/surface) evidence type before their normal-tissue pattern can be interpreted as risk; `F3`'s gap-filling priority depends on evidence this comparison does not have.
