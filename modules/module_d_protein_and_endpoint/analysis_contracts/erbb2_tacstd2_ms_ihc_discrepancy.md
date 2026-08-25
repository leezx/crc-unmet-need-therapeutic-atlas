# Module D follow-up — `ERBB2`/`TACSTD2` MS-vs-IHC discrepancy investigation

**Status: LOCKED. Does not resolve the discrepancy. Adds one concrete, checkable partial factor and rules out one candidate explanation as unverifiable from what HPA discloses.**

Built 2026-08-25, per Next-handoff item `3e(a)` (surfaced by the Module D first pass, `reports/PROJECT_STATUS.md`), following explicit user direction to investigate this specific gap.

## The discrepancy, restated precisely

Two independent protein-layer sources for the same two targets disagree in direction:

| Target | `PXD055821` MS (whole-tissue, CRC-LM-specific) | `HPA_CRC_cancer_tissue` IHC (cancer-cell-focused, generic CRC cohort) |
|---|---|---|
| `ERBB2` | detected (nonzero) in 56/60 specimens (93.3%) — TE033 | n=11: High=0, Medium=3, Low=2, **Not detected=6** — TE038 |
| `TACSTD2` | detected (nonzero) in 43/60 specimens (71.7%) — TE036 | n=12: High=0, Medium=0, Low=3, **Not detected=9** — TE041 |

Frequent MS detection, mostly `Not detected`/`Low` by IHC — the two sources point in different directions. This file investigates why, without guessing at an answer the data doesn't support.

## Investigated: cohort-composition difference (checked, not resolved either way)

`PXD055821`'s Sydney-cohort matrix is explicitly CRC **liver-metastasis** specimens (`pxd055821_protein_abundance.md`). `HPA_CRC_cancer_tissue`'s `cancer_data.tsv` "colorectal cancer" category is `indication_id=surface_target_therapeutic_window` in this repository's own `target_evidence.tsv` precisely because it is **not** documented as liver-metastasis-specific (`hpa_cancer_ihc.md`). If HPA's cohort is primary-tumor-only or a primary/met mix different from PXD055821's, that alone could produce a real biological difference in measured `ERBB2`/`TACSTD2` protein level between the two cohorts — not an assay artifact at all.

Independently fetched HPA's own pathology pages for `ERBB2` 2026-08-25 (`proteinatlas.org/ENSG00000141736-ERBB2/pathology` and `.../pathology/colorectal+cancer`) to check this directly. **HPA does not state whether its colorectal-cancer IHC cohort is primary, metastatic, or a mix** — this question is genuinely unanswerable from what HPA discloses on these pages. The pages also list four `ERBB2` antibodies (`HPA001383`, `CAB000043`, `CAB020416`, `CAB062555`) without identifying which one(s) generated the colorectal-cancer-category staining specifically, so a per-antibody reliability comparison isn't possible either. One general reliability note found: "Medium consistency between antibody staining and RNA expression data" (stated for the normal-tissue reliability score, not specific to the cancer atlas) — not strong enough to draw a conclusion from on its own. **This candidate explanation is left open, not ruled in or out.**

## Investigated: same-matrix relative-abundance percentile (new, computed here)

What can be checked directly, with no new data source, is where `ERBB2`/`TACSTD2` sit in `PXD055821`'s own whole-matrix abundance distribution — i.e., are they high-abundance or modest-abundance proteins in this specific mass-spec run, among everything else it measured. New `scripts/analyze_pxd055821_abundance_percentile.py` computes, for every one of the matrix's 9,263 genes, the same detection-fraction and median-intensity statistics `extract_pxd055821_protein_abundance.py` already computes per-target, then ranks each `A_CLINICAL` target's own value against that full gene population (percentile = fraction of the matrix's other genes strictly below it; results: `results/pxd055821_abundance_percentile.tsv`, gitignored/regenerable).

| Target | detection fraction | frac. percentile (of 9,263 genes) | median intensity | median percentile (of genes w/ nonzero median) |
|---|---:|---:|---:|---:|
| `CEACAM5` | 60/60 (100%) | 64.2 | 3.715e+07 | **99.3** |
| `ERBB2` | 56/60 (93.3%) | 49.4 | 2.191e+05 | **35.0** |
| `TACSTD2` | 43/60 (71.7%) | 32.5 | 3.025e+05 | **45.2** |
| `F3` | 16/60 (26.7%) | 10.6 | 1.384e+05 | 20.8 |
| `NECTIN4` | 13/60 (21.7%) | 8.3 | 6.913e+04 | 4.8 |

**`ERBB2` and `TACSTD2` are frequently "detected" (nonzero) but sit in the lower half of this matrix's own abundance range** (35th and 45th percentile of median intensity respectively) — a genuinely different pattern from `CEACAM5`, whose median intensity sits at the 99.3rd percentile (the single highest-abundance target of the five, and the only one with any HPA `High` IHC calls or concordant MS/IHC signal). This is one concrete, checkable partial factor consistent with — **not proof of** — the idea that DIA-NN's very permissive "any nonzero signal" detection threshold registers modest-abundance proteins that a categorical IHC staining call (which typically requires substantially more signal to score above `Low`) would not. It does not rule out the cohort-composition explanation above, does not establish which factor (or what mix of the two) actually explains the split, and is **not** a claim that `ERBB2`/`TACSTD2` are "unreliable" or "borderline" targets — only that, within this one whole-tissue MS run, their measured abundance is modest relative to everything else the same run measured.

## What remains unresolved

The `ERBB2`/`TACSTD2` MS-vs-IHC split stays exactly what it was before this file: a real, unreconciled cross-source pattern (TE033/TE036/TE038/TE041's own notes), now with one additional data point (same-matrix relative-abundance percentile) and one ruled-in-scope-but-unanswerable candidate factor (cohort composition, which HPA's own public pages don't resolve). Neither MS detection nor IHC staining is upgraded or downgraded by this file — no `evidence_directness`, `evidence_level`, or `confidence` field on TE033/TE036/TE038/TE041 changes. Determining which factor actually explains the split (if either alone does) would require either patient-level HPA cohort metadata (not published on these pages) or a matched primary/metastatic IHC cohort — neither is available in this environment.
