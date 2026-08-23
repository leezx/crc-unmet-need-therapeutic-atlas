# Module B analysis contract — `tgt_ceacam5`

**Status: `GSE178318` epithelial-proxy screen (QC-filtered, EPCAM-based). NOT malignancy-confirmed. Module B's malignant-cell prevalence question remains open for this target.**

Revised 2026-08-23 (PR #74 round 1 review): web-ChatGPT independently fetched `GSE178318`'s own publication (Cell Discovery 2021, DOI `10.1038/s41421-021-00312-y` — the round also caught that this repository's `DATA/registry/GSE178318/source_manifest.tsv` had recorded a non-existent DOI, `10.1038/s41598-021-96568-3`, now fixed) and found the first version of this analysis fell below that paper's own published standard on four points, all addressed below: no QC filtering, a scoring-math bug that structurally favored categories with more marker genes, an epithelial marker panel that includes genes also expressed in normal hepatic epithelium (a real confound in liver-metastasis samples), and folding treatment-naive patients into a treatment-defined `indication_id` with only a notes-field disclaimer. The paper's own malignant-cell confirmation step (CNV inference via InferCNV, using EPCs as input) is **not reproduced here** — that would need a genomic gene-position reference and a chosen normal-cell reference population, a materially larger undertaking than fixing the four items above. This file and every downstream artifact (`target_evidence.tsv`, module `README.md`, `reports/PROJECT_STATUS.md`) now describe this as an **epithelial-proxy screen**, explicitly not a malignancy-confirmed result, per the reviewer's own sanctioned fallback path.

## Method (corrected, locked before re-running)

1. Same barcode parsing / patient-specimen reconciliation as before (`<10x_barcode>_<patient_id>_<specimen_material>`, validated against `DATA/registry/GSE178318/sample_map.tsv`'s 15 keys).
2. **QC filtering, a paper-aligned operationalization of the source publication's own criteria** (Methods, Cell Discovery 2021), not a line-by-line reproduction: detected genes >= 500 (paper states this cutoff explicitly) and mitochondrial UMI fraction <= 15% (also stated explicitly; 13 canonical `MT-` protein-coding genes present in the gene index) apply as written; per-sample (used as this dataset's "batch" unit) 3-SD outlier removal on `log10(total UMI)` is per the paper's own stated rule, but the paper's gene-count outlier step only says "remove cells that showed an unusually high or low number of genes" without stating 3-SD for that step specifically — the same 3-SD rule is applied here as the most direct reading, not because the paper states it for gene count too. This run: 123,330 of 140,281 barcodes pass (the paper reports 111,292 of 140,281 after its own pipeline — not expected to match exactly, since the paper's batch definition and exact per-cell arithmetic are not independently reproducible from the Methods text alone; reported as a sanity comparison, not a target to hit).
3. **Epithelial identification: EPCAM alone**, matching the paper's own method ("EPCs were identified using the higher expression of EPCAM") — not the prior 5-gene panel (`EPCAM`/`KRT8`/`KRT18`/`KRT19`/`CDH1`), which included genes also expressed in normal hepatic epithelium/hepatocytes, a real risk of misclassifying normal liver tissue as "epithelial" in `LIVER_METASTASIS` samples.
4. **Per-cell category score, fixed**: each category's score is `(sum of its marker genes' counts / number of marker genes in that category) / total UMI` — a marker-gene-average, not a raw sum — so a category is no longer structurally favored purely for having more marker genes in `cell_type_marker_set_v1.tsv`. Immune/fibroblast/endothelial keep their multi-gene panels (unchanged rationale); epithelial uses EPCAM alone as its own single-gene "category." A cell is assigned to the highest-scoring category among QC-passing cells only; `Unassigned` if all scores are zero. Covered by `scripts/test_annotate_gse178318_cell_types.py`'s classification tests (synthetic inputs specifically constructed to catch the old size-bias bug).
5. **Treated and treatment-naive patients are reported and keyed separately**, not folded into one dossier with a caveat:
   - **`COL15`, `COL17`, `COL18`** (received `CAPEOX_3_CYCLES` / `CAPEOX_4_CYCLES` / `FOLFOX_BEV_8_CYCLES` per `sample_map.tsv`) are the primary result, `indication_id=mcrc_preop_chemotherapy_crlm`.
   - **`COL07`, `COL12`, `COL16`** (treatment-naive) are separate context evidence, `indication_id=mcrc_liver_metastasis` (the anatomy-only parent node — matched primary/CRLM pairs without a treatment-exposure claim).
6. `RNA_no`/`RNA_low`/`RNA_high` thresholds unchanged in intent, fixed for consistency (contract said `>50%` for `RNA_high`; code previously used `>=50%` — now both say `>`): `RNA_no` < 5%, `RNA_low` 5-50% inclusive, `RNA_high` > 50% of epithelial-proxy cells CEACAM5-positive.

## Results (2026-08-23, corrected)

Run via `python3 scripts/annotate_gse178318_cell_types.py --gene CEACAM5`, 94s. Full table: `results/tgt_ceacam5_cell_type_prevalence.tsv` (gitignored, not committed — regenerable).

**PBMC validation check** (3 samples, QC-passing cells): `COL12_PBMC` 88.6% immune / 0.0% epithelial (2/12164); `COL17_PBMC` 94.1% immune / 0% epithelial (0/6554); `COL18_PBMC` 92.4% immune / 0% epithelial (0/7679). Still a clean pass with the corrected method.

**Treated patients (`COL15`/`COL17`/`COL18`) — primary Module B result for `indication_id=mcrc_preop_chemotherapy_crlm`:**

| Patient | Primary CEACAM5+ (of epithelial-proxy) | LM CEACAM5+ (of epithelial-proxy) | Primary n_epi | LM n_epi | Primary bucket | LM bucket |
|---|---:|---:|---:|---:|---|---|
| COL15 | 59.5% | 33.3% | 378 | 841 | **RNA_high** | RNA_low |
| COL17 | 20.0% | 12.0% | 50 | 25 | RNA_low | RNA_low |
| COL18 | 35.6% | 23.1% | 132 | 360 | RNA_low | RNA_low |

Epithelial-proxy cell counts are much lower for `COL17`/`COL18` than `COL15` after QC + EPCAM-only identification (50-360 cells vs. 378-841) — directionally consistent with the review's citation that the paper itself reports few EPCs in chemo-treated patients, concentrated in `COL15`. This is a real corroborating signal for the corrected method, not something the prior (uncorrected) version showed clearly.

**Treatment-naive patients (`COL07`/`COL12`/`COL16`) — context evidence for `indication_id=mcrc_liver_metastasis`:**

| Patient | Primary CEACAM5+ (of epithelial-proxy) | LM CEACAM5+ (of epithelial-proxy) | Primary n_epi | LM n_epi | Primary bucket | LM bucket |
|---|---:|---:|---:|---:|---|---|
| COL07 | 20.5% | 68.6% | 5214 | 1246 | RNA_low | **RNA_high** |
| COL12 | 41.4% | 61.4% | 186 | 176 | RNA_low | **RNA_high** |
| COL16 | 40.0% | 15.9% | 1220 | 145 | RNA_low | RNA_low |

## Interpretation, staying inside what this screen can prove

- **This is not a malignancy-confirmed result.** "EPCAM-high, QC-passing cell in a `PRIMARY_CRC`/`LIVER_METASTASIS` specimen" is the closest available proxy for malignant epithelium used here — it is not itself evidence of malignancy. Normal/reactive epithelium and stromal contamination not caught by QC could contribute to this count. Module B's actual malignant-cell prevalence question for `tgt_ceacam5` is **not closed** by this run.
- Across both treated and untreated groups, every patient with a nonzero epithelial-proxy cell count shows a detectable CEACAM5-positive fraction in both primary and metastatic tissue — no sample buckets `RNA_no`. This pattern held in both the corrected and uncorrected runs, so it is a comparatively more robust finding than the exact percentages, which shifted materially between runs (e.g. `COL07_LM` moved from 47.7% to 68.6%, `COL17_LM`'s epithelial-proxy cell count dropped from 109 to 25) once QC and the EPCAM-only marker were applied.
- `evidence_directness=UNCALIBRATED_PROXY` for both `target_evidence.tsv` rows (`TE004` treated, `TE005` untreated context) — never `DIRECT`, and this screen does not by itself upgrade to a stronger directness even with QC applied, since malignancy is still not confirmed.
