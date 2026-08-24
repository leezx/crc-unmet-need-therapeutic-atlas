# Module B analysis contract — `tgt_nectin4`

**Status: `GSE178318` epithelial-proxy screen (QC-filtered, EPCAM-based). NOT malignancy-confirmed. Module B's malignant-cell prevalence question remains open for this target.**

## Method

Identical to `tgt_ceacam5.md`'s corrected method, unchanged, with one target-specific resolution step: `--gene PVRL4` (see `data_lock/tgt_nectin4.md` for why) — the gene symbol passed to `annotate_gse178318_cell_types.py`, not the gene actually reported anywhere else in this repository, which is `NECTIN4` throughout.

## Results (2026-08-24)

Run via `python3 scripts/annotate_gse178318_cell_types.py --gene PVRL4 --out .../tgt_nectin4_cell_type_prevalence.tsv`. Full table: `results/tgt_nectin4_cell_type_prevalence.tsv` (gitignored, not committed — regenerable). QC and epithelial-proxy cell counts per sample are identical to `tgt_ceacam5.md`'s.

**PBMC validation check**: identical to `tgt_ceacam5.md`.

**Treated patients (`COL15`/`COL17`/`COL18`) — primary Module B result for `indication_id=mcrc_preop_chemotherapy_crlm`:**

| Patient | Primary NECTIN4+ (of epithelial-proxy) | LM NECTIN4+ (of epithelial-proxy) | Primary n_epi | LM n_epi | Primary bucket | LM bucket |
|---|---:|---:|---:|---:|---|---|
| COL15 | 9.0% | 4.6% | 378 | 841 | RNA_low | RNA_no |
| COL17 | 0.0% | 4.0% | 50 | 25 | RNA_no | RNA_no |
| COL18 | 0.0% | 1.1% | 132 | 360 | RNA_no | RNA_no |

**Treatment-naive patients (`COL07`/`COL12`/`COL16`) — context evidence for `indication_id=mcrc_liver_metastasis`:**

| Patient | Primary NECTIN4+ (of epithelial-proxy) | LM NECTIN4+ (of epithelial-proxy) | Primary n_epi | LM n_epi | Primary bucket | LM bucket |
|---|---:|---:|---:|---:|---|---|
| COL07 | 11.2% | 8.6% | 5214 | 1246 | RNA_low | RNA_low |
| COL12 | 8.6% | 12.5% | 186 | 176 | RNA_low | RNA_low |
| COL16 | 23.8% | 1.4% | 1220 | 145 | RNA_low | RNA_no |

## Interpretation, staying inside what this screen can prove

- **This is not a malignancy-confirmed result** — same caveat as prior targets.
- `NECTIN4` positivity is sparse in the treated cohort — 4 of 6 treated samples bucket `RNA_no`, `COL15` primary the only one above 5% (9.0%). This is consistent with Module E's finding that `NECTIN4` RNA is essentially absent from colon/rectum bulk tissue (1.4-1.6 nTPM) — a low epithelial-proxy positivity rate in this GI-derived cell population is directionally coherent with that, though Module B and Module E measure different things (single-cell positive-fraction vs. bulk-tissue nTPM) and are not being cross-normalized here.
- `evidence_directness=UNCALIBRATED_PROXY` for both `TE020` (treated) and `TE021` (untreated context) — unchanged reasoning from `tgt_ceacam5`.
