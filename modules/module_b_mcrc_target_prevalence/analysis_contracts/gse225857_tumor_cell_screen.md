# Module B analysis contract — `GSE225857` non-immune tumor-cell screen (second CRLM cohort)

**Status: LOCKED, author-cluster-based tumor-cell screen for all five `A_CLINICAL` targets. NOT malignancy-confirmed by CNV inference (same caveat as `GSE178318`), but built on the source publication's own validated tumor-cell clusters, not a single-gene proxy invented for lack of an alternative.**

Built 2026-08-24 (PR #81), per PR #79 round-1 reviewer's own stated 3-step order once the count matrix is opened: (1) confirm cell-ID join between counts and metadata; (2) confirm the five targets exist in the gene index; (3) confirm the author tumor-cell annotation is directly reusable — only then compute prevalence.

## Pre-flight checks (all three passed; see `scripts/annotate_gse225857_tumor_cells.py`'s built-in, fail-closed verification)

1. **Cell-ID join**: `GSM7058755_non_immune_counts.txt.gz`'s header cell IDs (41,892) join 1:1, in identical row order, to `GSM7058755_non_immune_meta.txt.gz`'s row names, after normalizing the counts file's `.` back to `-` (an R `write.table` syntactic-name substitution — R replaces disallowed characters like `-` with `.` when writing column names by default — not a real ID mismatch). Verified programmatically, not assumed; the script fails closed (`sys.exit(1)`) if this join is ever not exact.
2. **Gene index**: all five `A_CLINICAL` targets (`CEACAM5`, `ERBB2`, `F3`, `NECTIN4`, `TACSTD2`) present under their canonical HGNC symbols. Unlike `GSE178318`, no alias workaround (e.g. `PVRL4` for `NECTIN4`) was needed.
3. **Author tumor-cell annotation, directly reusable**: the metadata's `cluster` column is 100% populated (0 empty values across 41,892 rows) with real author-provided cell-type labels — 11 distinct `Tu01`-`Tu11` tumor clusters (23,954 of 41,892 cells, 57.2%), exactly matching the source publication's stated "11 tumor cell clusters" (Wang et al., *Sci Adv* 2023, PMID 37327339); 6 `E01`-`E06` endothelial clusters, exactly matching the publication's stated 6; 6 `F01`-`F06` fibroblast clusters vs. the publication's stated 8 (not reconciled, non-blocking — this screen only uses the `Tu0N` tumor clusters). Every cell already has `predicted.doublet=False`/`doublet=singlet` — this is the paper's own deposited, already-QC'd/doublet-filtered release, not a raw unfiltered barcode dump like `GSE178318`'s. No additional QC filtering is applied here.

## Method

1. Restrict to cells whose `cluster` value starts with `Tu` (author-defined tumor cells) — **not** an EPCAM-only proxy. This is a materially stronger starting point than `GSE178318`'s screen (see that dataset's own `analysis_contracts/tgt_ceacam5.md`): tumor-cell identity here is the source publication's own validated cluster call, not a single-gene marker score invented because no author annotation existed.
2. For each target gene, stream `GSM7058755_non_immune_counts.txt.gz` (a dense 17,515-gene x 41,892-cell TSV, not `GSE178318`'s sparse Matrix Market format) to find the one row matching the gene symbol — an O(n_genes) scan, the full matrix is never materialized in memory.
3. Per patient x organ (`CC` = primary colorectal cancer, `LC` = liver metastasis; both `CCT`/`LCT` in the raw organ codes), compute the fraction of tumor cells with a nonzero raw count for the gene.
4. `RNA_no`/`RNA_low`/`RNA_high` buckets, same thresholds as `GSE178318`'s screen: `RNA_no` < 5%, `RNA_low` 5-50% inclusive, `RNA_high` > 50%.
5. All five patients in this file (`s0107`/`s0115`/`s0813`/`s0920`/`s1231`) received uniform preoperative chemotherapy/RT (this dataset's registry-level `treatment_annotation=CHEMOTHERAPY_AND_OR_RT_PREOPERATIVE`) — no treated/treatment-naive split is needed, unlike `GSE178318`. Both `CC` and `LC` sites fall under `indication_id=mcrc_preop_chemotherapy_crlm` (its `anatomy` field is explicitly `PRIMARY_AND_LIVER_METASTASIS`).

## Results (2026-08-24)

Run via `python3 scripts/annotate_gse225857_tumor_cells.py --gene <SYMBOL>` for each of the five targets. Full tables: `results/tgt_<target>_gse225857_tumor_cell_prevalence.tsv` (gitignored, not committed — regenerable).

| Patient | CEACAM5 CC / LC | ERBB2 CC / LC | F3 CC / LC | NECTIN4 CC / LC | TACSTD2 CC / LC | n_tumor CC / LC |
|---|---|---|---|---|---|---|
| s0107 | 61.7%(**HIGH**) / 43.6% | 30.9% / 20.3% | 19.5% / 14.1% | 14.8% / 4.3%(NO) | 34.4% / 22.1% | 1,422 / 163 |
| s0115 | 55.2%(**HIGH**) / 0.0%(NO) | 23.3% / 21.8% | 4.3%(NO) / 9.1% | 5.2% / 3.6%(NO) | 9.5% / 50.9%(**HIGH**) | 116 / 55 |
| s0813 | 95.0%(**HIGH**) / 97.2%(**HIGH**) | 25.6% / 20.7% | 26.3% / 5.5% | 15.5% / 9.6% | 31.4% / 15.4% | 1,573 / 3,140 |
| s0920 | 9.0% / 7.4% | 12.9% / 19.2% | 3.5%(NO) / 3.7%(NO) | 4.2%(NO) / 4.9%(NO) | 21.8% / 29.1% | 6,382 / 9,976 |
| s1231 | 67.9%(**HIGH**) / 29.3% | 15.2% / 7.3% | 38.6% / 10.8% | 11.1% / 10.1% | 27.0% / 20.1% | 396 / 731 |

(`n_tumor` = author-defined `Tu0N`-cluster cell count for that patient x site; all percentages are the fraction of those tumor cells with a nonzero raw count for the gene.)

## Interpretation, staying inside what this screen can prove

- **This is not a CNV-confirmed malignancy result** — `Tu0N` cluster membership is the source publication's own single-cell clustering call, cross-checked here only by cluster count (11/11 exact match) and cell-count plausibility, not independently re-derived from CNV inference. It is a materially more direct malignant-cell proxy than `GSE178318`'s EPCAM-only screen, but the same `evidence_directness=UNCALIBRATED_PROXY` applies — this is still an RNA detection-fraction read, not a protein/surface-density measurement.
- **CEACAM5 is the only target reaching `RNA_high` in this cohort in more than one patient x site cell** (4 of 5 patients hit `RNA_high` in at least one site; `s0813` hits it in both), consistent with `GSE178318`'s own CEACAM5 screen also showing the broadest `RNA_high` footprint among the five targets there. `TACSTD2` reaches `RNA_high` in exactly one cell (`s0115` LC, n=55, a small sample). `ERBB2` never reaches `RNA_high` or `RNA_no` in any cell — a consistently mid-range detection pattern across all 5 patients and both sites. `F3`/`NECTIN4` each have several `RNA_no` cells, concentrated in the two lowest-yield patients (`s0115`, `s0920`).
- **No target is universally `RNA_no`** — every target has at least some positive detection in every patient, consistent with the pattern already seen in `GSE178318`'s own CEACAM5 screen.
- `s0920`'s tumor population (6,382 CC + 9,976 LC cells) is far larger than the other four patients combined and shows the lowest detection fractions for four of the five targets (all but TACSTD2) — a genuine finding, not investigated further here (could reflect real inter-patient heterogeneity, a distinct tumor subclone composition, or a batch effect; this screen cannot distinguish those explanations).
- `evidence_directness=UNCALIBRATED_PROXY` for all five new `target_evidence.tsv` rows (`TE027`-`TE031`) — same measurement_layer/directness convention as `GSE178318`'s `TE004`/`TE005`, never `DIRECT` or `CALIBRATED_PROXY`.
- This is now a genuine **second, independent, treated CRLM cohort** for all five targets under `indication_id=mcrc_preop_chemotherapy_crlm`, obtained entirely through GEO's public route — no CNSA DAC application was ever filed or needed.
