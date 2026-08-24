# Module B analysis contract — `tgt_f3`

**Status: `GSE178318` epithelial-proxy screen (QC-filtered, EPCAM-based). NOT malignancy-confirmed. Module B's malignant-cell prevalence question remains open for this target.**

## Method

Identical to `tgt_ceacam5.md`'s corrected method, unchanged.

## Results (2026-08-24)

Run via `python3 scripts/annotate_gse178318_cell_types.py --gene F3`. Full table: `results/tgt_f3_cell_type_prevalence.tsv` (gitignored, not committed — regenerable). QC and epithelial-proxy cell counts per sample are identical to `tgt_ceacam5.md`'s.

**PBMC validation check**: identical to `tgt_ceacam5.md`.

**Treated patients (`COL15`/`COL17`/`COL18`) — primary Module B result for `indication_id=mcrc_preop_chemotherapy_crlm`:**

| Patient | Primary F3+ (of epithelial-proxy) | LM F3+ (of epithelial-proxy) | Primary n_epi | LM n_epi | Primary bucket | LM bucket |
|---|---:|---:|---:|---:|---|---|
| COL15 | 7.4% | 5.5% | 378 | 841 | RNA_low | RNA_low |
| COL17 | 4.0% | 4.0% | 50 | 25 | RNA_no | RNA_no |
| COL18 | 3.0% | 1.7% | 132 | 360 | RNA_no | RNA_no |

**Treatment-naive patients (`COL07`/`COL12`/`COL16`) — context evidence for `indication_id=mcrc_liver_metastasis`:**

| Patient | Primary F3+ (of epithelial-proxy) | LM F3+ (of epithelial-proxy) | Primary n_epi | LM n_epi | Primary bucket | LM bucket |
|---|---:|---:|---:|---:|---|---|
| COL07 | 40.2% | 10.1% | 5214 | 1246 | RNA_low | RNA_low |
| COL12 | 2.2% | 3.4% | 186 | 176 | RNA_no | RNA_no |
| COL16 | 34.8% | 4.1% | 1220 | 145 | RNA_low | RNA_no |

## Interpretation, staying inside what this screen can prove

- **This is not a malignancy-confirmed result** — same caveat as prior targets.
- `F3` positivity is the **lowest of the four new targets**: 4 of 6 treated-cohort samples bucket `RNA_no` (<5%), and only `COL07` (primary) reaches a substantial fraction (40.2%). This is markedly sparser than `CEACAM5`/`ERBB2`, descriptive of this cohort's epithelial-proxy cells only — not a claim about `F3` protein expression or accessible antigen density.
- `evidence_directness=UNCALIBRATED_PROXY` for both `TE015` (treated) and `TE016` (untreated context) — unchanged reasoning from `tgt_ceacam5`.
