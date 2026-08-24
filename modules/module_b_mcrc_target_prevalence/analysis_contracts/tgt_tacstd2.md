# Module B analysis contract — `tgt_tacstd2`

**Status: `GSE178318` epithelial-proxy screen (QC-filtered, EPCAM-based). NOT malignancy-confirmed. Module B's malignant-cell prevalence question remains open for this target.**

## Method

Identical to `tgt_ceacam5.md`'s corrected method, unchanged.

## Results (2026-08-24)

Run via `python3 scripts/annotate_gse178318_cell_types.py --gene TACSTD2`. Full table: `results/tgt_tacstd2_cell_type_prevalence.tsv` (gitignored, not committed — regenerable). QC and epithelial-proxy cell counts per sample are identical to `tgt_ceacam5.md`'s.

**PBMC validation check**: identical to `tgt_ceacam5.md`.

**Treated patients (`COL15`/`COL17`/`COL18`) — primary Module B result for `indication_id=mcrc_preop_chemotherapy_crlm`:**

| Patient | Primary TACSTD2+ (of epithelial-proxy) | LM TACSTD2+ (of epithelial-proxy) | Primary n_epi | LM n_epi | Primary bucket | LM bucket |
|---|---:|---:|---:|---:|---|---|
| COL15 | 24.9% | 17.2% | 378 | 841 | RNA_low | RNA_low |
| COL17 | 8.0% | 20.0% | 50 | 25 | RNA_low | RNA_low |
| COL18 | 3.0% | 4.4% | 132 | 360 | RNA_no | RNA_no |

**Treatment-naive patients (`COL07`/`COL12`/`COL16`) — context evidence for `indication_id=mcrc_liver_metastasis`:**

| Patient | Primary TACSTD2+ (of epithelial-proxy) | LM TACSTD2+ (of epithelial-proxy) | Primary n_epi | LM n_epi | Primary bucket | LM bucket |
|---|---:|---:|---:|---:|---|---|
| COL07 | 69.3% | 41.0% | 5214 | 1246 | **RNA_high** | RNA_low |
| COL12 | 18.3% | 21.0% | 186 | 176 | RNA_low | RNA_low |
| COL16 | 66.3% | 13.1% | 1220 | 145 | **RNA_high** | RNA_low |

## Interpretation, staying inside what this screen can prove

- **This is not a malignancy-confirmed result** — same caveat as prior targets.
- `TACSTD2` shows the **widest spread of the five targets run so far**: two treatment-naive primary samples (`COL07`, `COL16`) reach `RNA_high` (>50%), while `COL18` (treated) is `RNA_no` on both specimens. This is descriptive of this cohort's epithelial-proxy cells only, not a malignancy or protein-density claim — Module E's finding that `TACSTD2` bulk-tissue RNA is very low in colon/rectum (0.9 nTPM) describes normal tissue, not the tumor-site epithelial-proxy population this axis measures, and the two are not directly comparable.
- `evidence_directness=UNCALIBRATED_PROXY` for both `TE025` (treated) and `TE026` (untreated context) — unchanged reasoning from `tgt_ceacam5`.
