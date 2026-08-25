# Module D analysis contract — `MCRC_liver_metastasis_PDO_2026` multiplex-IHC (`ERBB2` only)

**Status: LOCKED, real per-PDO mIHC values, but with a source-authors'-own reliability caveat this contract must always carry alongside the numbers. Third, independent protein-layer source for `ERBB2` — the only one of this repository's five `A_CLINICAL` targets covered by this dataset's 14-marker panel.**

Built 2026-08-25, per explicit user direction (Next-handoff item `3e(b)` from PR #82's Module D first pass: `MCRC_liver_metastasis_PDO_2026`'s real per-sample `ERBB2` mIHC data was downloaded but not yet incorporated into `target_evidence.tsv`).

## What's actually in `Data S3.xlsx`

`MCRC_liver_metastasis_PDO_2026` (Kryeziu, Sveen, Lothe et al. 2026, "Patient-derived organoids from metastatic colorectal cancer mirror tumor heterogeneity and predict patient survival and drug sensitivity", Mendeley Data v3, `doi:10.17632/hr94h42xdc.3`; publication PMC13293968) is a living biobank of 213 CRC liver-metastasis (CRLM) patient-derived organoids (PDOs) from 102 patients. `Data S3.xlsx` (114.6 KB, downloaded 2026-08-25, checksum-verified) is a small, already-processed multiplex-fluorescent-IHC (mIHC) table: one row per PDO x protein-marker x staining-round, with a continuous `mean_express_PDO` value (mean relative fluorescence intensity per PDO image, normalized to total cellular content — not a raw pixel count and not a High/Medium/Low/Not-detected category, unlike `HPA_CRC_cancer_tissue`'s IHC read).

Per the source publication's own methods text (independently fetched and confirmed 2026-08-25): "Fluorescence-based multiplex immunohistochemistry and digital image analyses were used to analyze in situ expression of fourteen proteins in 136 PDOs and two corresponding tumor tissue samples from 67 patients." The fourteen markers are `ABCB1`/`ABCG2`/`CDH1`/`CDX2`/`CFTR`/`ERBB2`/`HSF1`/`KI67`/`KRT20`/`KRT7`/`RCC2`/`RIPK1`/`TP53`/`UGT1A` — **only `ERBB2` is among this repository's five `A_CLINICAL` targets.**

**Patient count is the publication's own stated denominator (67), not independently re-derived.** Some `PDO_id` values in the raw file carry decimal suffixes (e.g. `Pt54.2`, `Pt54.3`, `Pt6.2`, `Pt22.2`) whose meaning — a distinct patient vs. a second lesion/re-resection from the same patient — is not resolved in the fetched text. Rather than guess (and risk exactly the kind of specimen-vs-patient miscount PR #82 round 1 caught for `PXD055821`), this contract uses the paper's own "136 PDOs ... from 67 patients" statement as the panel-wide denominator and does not compute a separate ERBB2-specific patient count from parsing `PDO_id` strings. PDO-level counts (below) are unambiguous and used instead.

## *** The critical caveat: `ERBB2` was excluded from the source authors' own analysis

The same methods paragraph states, **verbatim**: *"KRT7 and ERBB2 were excluded from analysis due to no or very low expression levels, respectively."*

This means: the 136 raw per-PDO `ERBB2` values are still physically present in `Data S3.xlsx` — this script reads them, unmodified — but **the original authors themselves judged this marker's signal in this 14-plex panel unreliable and excluded it from every downstream analysis in their own paper.** This is not a claim this repository is making about the biology (e.g. "ERBB2 expression is low" as a finding) — it is the source authors' own QC judgment about assay/antibody performance in this specific multiplex context, reported here for that reason, not suppressed.

One piece of corroborating context from elsewhere in the same publication: a *different* `ERBB2` antibody clone (single-plex DAB IHC, clone CB11) was used successfully for a case-report figure (patient `Pt137`, Figure 7A) — "Immunohistochemistry stains show in situ ERBB2 expression in the primary tumor, two CRLMs, and the corresponding PDOs." This is consistent with the multiplex panel's specific `ERBB2` reagent (polyclonal, catalog `AO485`) being the problem, not `ERBB2` IHC in general — but this repository does not use that single-plex figure as quantitative evidence (it is one patient, illustrative, not a systematic measurement across the cohort).

**Every use of this evidence row must carry this caveat.** It is not presented as clean corroborating evidence alongside `PXD055821`'s MS read (`TE033`) or `HPA_CRC_cancer_tissue`'s IHC read (`TE038`) — it is a third, independent protein-layer measurement type, but one the source authors themselves flagged as unreliable.

## Method

1. `scripts/extract_pdo_erbb2_mihc.py --gene ERBB2` opens `Data S3.xlsx`, filters to `Prot_marker == "ERBB2"` rows, and computes: number of PDOs with a genuinely nonzero `mean_express_PDO` value (`detected` — a blank/missing cell and a literal `0` are both treated as not detected), detection fraction, median/min/max of the detected values.
2. Checksum-verified against `DATA/registry/MCRC_liver_metastasis_PDO_2026/file_inventory.tsv` before use — fails closed on missing file or checksum mismatch.
3. The script refuses (fails closed) any `--gene` not among the panel's fourteen markers, rather than silently returning zero rows.

## Results (2026-08-25)

Run via `python3 scripts/extract_pdo_erbb2_mihc.py --gene ERBB2`. Full per-PDO table: `results/tgt_erbb2_pdo_mihc.tsv` (gitignored, not committed — regenerable).

| Marker | Distinct PDOs | Detected (nonzero) / rows | Detection fraction | Median | Min | Max |
|---|---:|---:|---:|---:|---:|---:|
| ERBB2 | 136 | 136/136 | 100.0% | 0.0910 | 0.0154 | 0.5635 |

(`mean_express_PDO` units are this study's own normalized relative fluorescence intensity scale — not comparable to `PXD055821`'s DIA-NN intensity scale or `HPA_CRC_cancer_tissue`'s High/Medium/Low/Not-detected categories. All 136 PDOs that were mIHC-profiled show a nonzero — though, per the source authors' own QC, unreliable — `ERBB2` signal; "detected in 100%" here does not mean "reliably detected," it means the raw value in this specific column was not literally zero.)

## Interpretation, staying inside what this screen can prove — and cannot

- **This is not clean corroborating evidence.** Read alongside `PXD055821`'s MS read (93.3% specimen detection, `TE033`) and `HPA_CRC_cancer_tissue`'s IHC read (mostly `Not detected`, 6/11 patients, `TE038`), a naive reading might treat "100% nonzero in a third source" as further support for `ERBB2` protein presence. That reading is not licensed here: the source authors' own QC excluded this exact marker from this exact assay for unreliable signal, so a nonzero value in every PDO is at least as consistent with assay noise/background as with true expression. This repository reports the number, with the caveat, and draws no directional conclusion from it.
- **PDO-level, not primary-tissue-level.** PDOs are cultured organoids derived from resected CRLM tissue, not the tissue itself — an additional layer of biological distance from any of this repository's other Module D sources (which read primary tumor tissue directly).
- `evidence_level=EXPLORATORY_UNDERPOWERED` and `confidence=LOW` (rather than `SCREENING_LEVEL`/`MEDIUM` like `TE033`/`TE038`) specifically because of the source-authors'-own exclusion — a different kind of weakness than small-n underpowering, but the closest available vocabulary term in this schema, chosen to signal maximum skepticism; the actual reason is always stated in the claim/notes text, never left to the tier alone to convey.
- `evidence_directness=UNCALIBRATED_PROXY` — unchanged either way by this caveat: mIHC (reliable or not) is still not membrane-specific, quantitative antigen density, or a calibrated surface assay. Per this repository's Module D contract (`modules/module_d_protein_and_endpoint/README.md`), this does NOT establish surface density even setting the reliability caveat aside.
- `indication_id=mcrc_liver_metastasis` (anatomy-only, `ANY` treatment_line/prior_therapy) — chosen because the source publication describes this living biobank as patient-derived organoids from resected CRC liver metastases, matching `PXD055821`'s anatomy-only mapping; no treatment-status claim is made.
- One `target_evidence.tsv` row (`TE042`), backed by `EV050`.
