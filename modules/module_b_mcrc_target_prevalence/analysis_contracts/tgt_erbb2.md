# Module B analysis contract — `tgt_erbb2`

**Status: `GSE178318` epithelial-proxy screen (QC-filtered, EPCAM-based). NOT malignancy-confirmed. Module B's malignant-cell prevalence question remains open for this target.**

## Method

Identical to `tgt_ceacam5.md`'s corrected method (`scripts/annotate_gse178318_cell_types.py`, unchanged since PR #74): same barcode parsing, same QC (detected genes >=500, mito UMI <=15%, per-sample 3-SD outlier removal on log-total-UMI and gene count), same EPCAM-alone epithelial identification, same marker-average scoring, same `RNA_no`(<5%)/`RNA_low`(5-50%)/`RNA_high`(>50%) buckets, same treated (`COL15`/`COL17`/`COL18`)/treatment-naive (`COL07`/`COL12`/`COL16`) split into separate `indication_id` rows.

## Results (2026-08-24)

Run via `python3 scripts/annotate_gse178318_cell_types.py --gene ERBB2`. Full table: `results/tgt_erbb2_cell_type_prevalence.tsv` (gitignored, not committed — regenerable). QC and epithelial-proxy cell counts per sample are identical to `tgt_ceacam5.md`'s (same QC/classification pipeline, target-independent) — only the `ERBB2`-positive fraction differs.

**PBMC validation check**: identical to `tgt_ceacam5.md` (88.6% / 94.1% / 92.4% immune, ~0% epithelial across the 3 PBMC samples) — this check does not depend on the scored gene.

**Treated patients (`COL15`/`COL17`/`COL18`) — primary Module B result for `indication_id=mcrc_preop_chemotherapy_crlm`:**

| Patient | Primary ERBB2+ (of epithelial-proxy) | LM ERBB2+ (of epithelial-proxy) | Primary n_epi | LM n_epi | Primary bucket | LM bucket |
|---|---:|---:|---:|---:|---|---|
| COL15 | 27.0% | 15.2% | 378 | 841 | RNA_low | RNA_low |
| COL17 | 6.0% | 4.0% | 50 | 25 | RNA_low | RNA_no |
| COL18 | 10.6% | 6.1% | 132 | 360 | RNA_low | RNA_low |

**Treatment-naive patients (`COL07`/`COL12`/`COL16`) — context evidence for `indication_id=mcrc_liver_metastasis`:**

| Patient | Primary ERBB2+ (of epithelial-proxy) | LM ERBB2+ (of epithelial-proxy) | Primary n_epi | LM n_epi | Primary bucket | LM bucket |
|---|---:|---:|---:|---:|---|---|
| COL07 | 23.6% | 25.0% | 5214 | 1246 | RNA_low | RNA_low |
| COL12 | 14.5% | 30.7% | 186 | 176 | RNA_low | RNA_low |
| COL16 | 32.0% | 3.5% | 1220 | 145 | RNA_low | RNA_no |

## Interpretation, staying inside what this screen can prove

- **This is not a malignancy-confirmed result** — same caveat as `tgt_ceacam5`: "EPCAM-high, QC-passing cell in a tumor-site specimen" is a proxy, not evidence of malignancy.
- Every patient except `COL17`/`COL16` LM shows `RNA_low` rather than `RNA_no` or `RNA_high` — `ERBB2` positivity sits in a narrower, more uniformly moderate band (4-32%) than `CEACAM5`'s wider spread (12-69%), with no sample reaching `RNA_high`. This is descriptive of this cohort's epithelial-proxy cells, not a claim about `ERBB2` protein expression or accessible antigen density (Module E, not Module B, speaks to normal-tissue protein risk).
- `evidence_directness=UNCALIBRATED_PROXY` for both `TE010` (treated) and `TE011` (untreated context) — unchanged reasoning from `tgt_ceacam5`.
