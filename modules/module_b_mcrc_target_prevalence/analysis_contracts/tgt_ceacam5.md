# Module B analysis contract — `tgt_ceacam5`

Written before running the analysis (per `modules/README.md`'s working-structure convention), locking the method and thresholds so they aren't picked after seeing the result.

## What this analysis does and does not attempt

This is a **marker-gene-score cell-compartment split**, not malignancy calling. It separates cells into epithelial / immune / fibroblast / endothelial / unassigned using the fixed marker panel in `cell_type_marker_set_v1.tsv` (17 canonical markers, rationale documented per gene). It does **not** attempt to distinguish malignant epithelium from normal/reactive epithelium within a tumor specimen — that would require CNV inference (e.g. inferCNV-style) or a matched-normal comparison, neither of which is done here. `PRIMARY_CRC` and `LIVER_METASTASIS` specimens are tumor-site biopsies, so "epithelial cell in a tumor-site specimen" is used as the closest available proxy for "malignant/tumor epithelial cell," not a confirmed malignancy call. This is stated explicitly in every output row's `notes`.

## Method (locked before running)

1. Parse `GSE178318_barcodes.tsv.gz`; each barcode already encodes `<10x_barcode>_<patient_id>_<specimen_material>` (e.g. `AAACCTGAGAAACCTA_COL07_CRC`) — same parsing rule as the archived `qc_gse178318.py`, reconciled against `DATA/registry/GSE178318/sample_map.tsv`'s 15 patient/specimen keys (hard fail on any unparseable or unmapped barcode).
2. Single streaming pass over `GSE178318_matrix.mtx.gz` (33,694 genes x 140,281 cells, 166,681,072 nonzero entries) accumulating, per cell: total UMI count, raw sum per marker category (epithelial/immune/fibroblast/endothelial), and raw `CEACAM5` count. No full dense or sparse matrix is materialized in memory.
3. Per-cell category score = category's raw marker sum / total UMI count (a simple CP-normalized proportion, not a full library-size-normalized/log-transformed pipeline). A cell is assigned to the category with the highest score; a cell with all four category scores at zero is `Unassigned`.
4. Restrict the headline prevalence question to `PRIMARY_CRC` and `LIVER_METASTASIS` specimens (6 patients x 2 specimen types = 12 samples, per `sample_map.tsv`). `PBMC` specimens (3 samples) are **not** part of the prevalence question — they serve as a built-in validation check: a PBMC sample should type as ~100% immune, and any large deviation would flag the marker-score method itself as unreliable before trusting its tumor-tissue output.
5. Within `epithelial`-typed cells in `PRIMARY_CRC`/`LIVER_METASTASIS` samples: `CEACAM5`-positive fraction (raw count > 0), and the module's `RNA_no/RNA_low/RNA_high` bucket per Module B's naming rule, computed per patient/specimen so between-patient and within-patient (primary vs LM) heterogeneity is visible, not averaged away.
6. `RNA_no/RNA_low/RNA_high` thresholds, locked before seeing the result: `RNA_no` = CEACAM5-positive fraction < 5% of epithelial cells; `RNA_low` = 5-50%; `RNA_high` = >50%. This is a coarse, explicitly-arbitrary triage threshold (Module B's own README requires a bucket, not a continuous score) — not a validated clinical cutoff.

## Exclusion / caveats (locked before running)

- n=6 patients is a within-cohort descriptive statistic, not a population-prevalence claim, per Module B's own "Cannot prove."
- Marker-score cell typing has known failure modes: doublets, low-count cells, and genuinely intermediate/hybrid states (e.g. EMT-like tumor cells) can be misassigned. No per-cell QC filter (e.g. minimum UMI/gene count) is applied in this pass — a cell with very few UMIs contributes a noisy score. This is recorded as a real limitation, not silently absorbed into the headline number.
- CEACAM5 raw-count positivity (count > 0) is itself a permissive proxy for "detectable transcript," subject to scRNA-seq dropout — a `RNA_no` call at the single-cell level does not mean the gene is truly absent in that cell.
- This produces `evidence_directness=UNCALIBRATED_PROXY` input for Module B's `prevalence` axis (scRNA epithelial-restricted proportion, not malignancy-confirmed, not surface protein) — never `DIRECT`, and never silently upgraded by any later Module D protein calibration (per Module B's own naming rule).

## Results (2026-08-23)

Run via `python3 scripts/annotate_gse178318_cell_types.py --gene CEACAM5`, 85s single streaming pass, 166,681,072 matrix entries, no dimension mismatch. Full table: `results/tgt_ceacam5_cell_type_prevalence.tsv` (not committed — `modules/*/results/` is gitignored; regenerate via the script).

**PBMC validation check** (3 samples, should be ~all immune, near-zero epithelial): `COL12_PBMC` 89.5% immune / 0.1% epithelial (17/12400 cells); `COL17_PBMC` 94.4% immune / 0.1% epithelial (6/6700 cells); `COL18_PBMC` 93.7% immune / 0.1% epithelial (5/7850 cells). All three behave as expected for a pure-blood specimen — this is a real, passing sanity check on the marker-score method, not a guarantee the method is correct on tumor tissue, but it rules out a gross labeling or parsing error.

**`PRIMARY_CRC` / `LIVER_METASTASIS` samples** (12 samples, 6 patients):

| Patient | Primary CEACAM5+ (of epithelial) | LM CEACAM5+ (of epithelial) | Primary bucket | LM bucket | Primary→LM direction |
|---|---:|---:|---|---|---|
| COL07 | 18.4% (n=8497 epi) | 47.7% (n=3787 epi) | RNA_low | RNA_low | up |
| COL12 | 36.1% (n=617 epi) | 66.7% (n=538 epi) | RNA_low | **RNA_high** | up |
| COL15 | 37.9% (n=1357 epi) | 32.8% (n=2509 epi) | RNA_low | RNA_low | down |
| COL16 | 23.7% (n=2749 epi) | 17.7% (n=379 epi) | RNA_low | RNA_low | down |
| COL17 | 15.9% (n=452 epi) | 12.8% (n=109 epi) | RNA_low | RNA_low | down |
| COL18 | 25.0% (n=609 epi) | 36.1% (n=543 epi) | RNA_low | RNA_low | up |

**11 of 12 samples bucket `RNA_low`; one (`COL12_LM`) buckets `RNA_high`. None bucket `RNA_no`** — every patient's epithelial compartment, in both primary and liver-metastasis tissue, contains a detectable CEACAM5-positive subpopulation.

**Primary-to-LM direction is not consistent**: 3 of 6 patients (`COL07`, `COL12`, `COL18`) show a higher CEACAM5+ fraction in the liver metastasis than the matched primary; the other 3 (`COL15`, `COL16`, `COL17`) show the opposite. This is reported as a genuine even split, not smoothed into a directional claim either way.

**Epithelial-cell yield varies widely by sample** (1.1%-50.0% of all cells), reflecting real differences in tumor cellularity/dissociation across specimens — noted as context, not a CEACAM5 finding.

**Cohort composition caveat, carried into the `target_evidence.tsv` row's notes**: this dataset's `indication_id=mcrc_preop_chemotherapy_crlm` dossier assignment (matching Module E's `tgt_ceacam5` rows, so this stays one dossier, not two) is an imperfect fit for the full 6-patient cohort — per `DATA/registry/GSE178318/sample_map.tsv`, only 3 patients (`COL15`, `COL17`, `COL18`) actually received a preoperative-chemotherapy regimen; the other 3 (`COL07`, `COL12`, `COL16`) are treatment-naive. All 6 are reported together because they are all matched primary/CRLM specimen pairs (this indication node's anatomical/timing scope), but the treatment-exposure criterion in its name does not describe half the cohort. Flagged explicitly rather than silently treated as uniform.

