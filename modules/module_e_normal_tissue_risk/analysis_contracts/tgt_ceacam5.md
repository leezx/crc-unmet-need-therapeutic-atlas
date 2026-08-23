# Module E analysis contract — `tgt_ceacam5`

## Method

`scripts/extract_normal_tissue_rna.py --gene CEACAM5` — a pure extraction (no download, no imputation, no cross-source averaging). Pulls every HPA-tissue row and every GTEx-tissue column where the gene symbol matches `CEACAM5` exactly, writes them as-is to `results/tgt_ceacam5_normal_tissue_rna.tsv`, and separately prints the module's named "key compartments" (colon, small intestine, liver, lung, kidney, heart, skin, bone marrow) plus the top 5 non-key HPA tissues by value, so a surprising tissue outside the named list is never silently dropped.

## Thresholds / naming rule

This module does not define an `RNA_no/low/high` bucket rule the way Module B does — Module B's rule is about malignant-cell fraction within a tumor, which is not what bulk normal-tissue RNA measures. Here the only judgment made is **"worth a closer protein/IHC look" vs "not"**, using each source's own units at face value (HPA nTPM, GTEx median TPM) with no cross-source unit conversion attempted (nTPM and TPM are not the same normalization; comparing across sources by relative pattern only, never by absolute cross-source ratio).

## Results (2026-08-23)

Full table: `results/tgt_ceacam5_normal_tissue_rna.tsv` (40 HPA + 68 GTEx rows). **Not committed** — `modules/*/results/` is gitignored per this repository's "no biological data" policy (`.gitignore`); regenerate on demand with `python3 scripts/extract_normal_tissue_rna.py --gene CEACAM5` (requires `HPA_RNA_TISSUE_CONSENSUS_PATH`/`GTEX_V11_MEDIAN_TPM_PATH`, see `config/external_sources.yaml`). The key-compartment values below, plus the `TE001`/`TE002` rows in `schemas/target_evidence.tsv`, are the canonical, committed record of this finding.

**Key compartments** (HPA nTPM / GTEx median TPM):

| Compartment | HPA nTPM | GTEx median TPM |
|---|---:|---|
| colon | 920.3 | Colon_Sigmoid 0.74; Colon_Transverse 243.7 |
| rectum | 885.1 | (no GTEx rectum tissue) |
| small intestine | 23.2 | Small_Intestine_Terminal_Ileum 34.8 |
| liver | 0.1 | Liver 0.07 |
| lung | 28.5 | Lung 4.6 |
| kidney | 0.8 | Kidney_Cortex 0.03; Kidney_Medulla 0 |
| heart | 0.1 | Heart_Atrial_Appendage 0.02; Heart_Left_Ventricle 0.02 |
| skin | 3.4 | Skin (both sites) 2.5 / 4.0 |
| bone marrow | 0.1 | not in GTEx v11's adult panel |

**GTEx colon subregions, examined further because of the large Colon_Sigmoid/Colon_Transverse gap above**: `Colon_Transverse_Mucosa` 1069.6, `Colon_Transverse_Mixed_Cell` 1120.6, `Colon_Transverse_Muscularis` 75.4 — i.e. the mucosa/epithelial-enriched subregions are the ones carrying the signal, and `Colon_Transverse_Muscularis` (essentially non-epithelial) is >10x lower. `Esophagus_Mucosa` (277.8) vs `Esophagus_Muscularis` (0.14) shows the same pattern independently. `Colon_Sigmoid`'s low value (0.74) relative to `Colon_Transverse` (243.7) is not explained by this data alone — recorded as an open discrepancy, not resolved by assumption; GTEx's sigmoid sampling may differ in mucosal content, but that is not confirmed here.

**Top 5 non-key HPA tissues** (checking for a liability the named-compartment list would miss): appendix 175.2, stomach 154.1, esophagus 148.8, tonsil 34.6, smooth muscle 26.8.

## Interpretation, staying inside what this module can prove

- The signal is essentially confined to GI mucosal/epithelial tissue (colon, rectum, appendix, small intestine, stomach, esophagus) and consistent with CEACAM5's known role as a GI epithelial differentiation antigen — matches, does not contradict, prior biology. Liver, kidney, heart, bone marrow are all low across both sources.
- **Genuinely new-to-this-run finding**: lung shows a non-trivial HPA value (28.5 nTPM, above small intestine's 23.2) that GTEx does not corroborate as strongly (4.6 median TPM) — flagged as a compartment worth a protein/IHC check, not dismissed and not escalated, since bulk RNA alone cannot resolve which lung cell population (if any) is contributing.
- The mucosa-vs-muscularis contrast within GTEx's own colon/esophagus subregions is itself evidence that this bulk signal tracks epithelial content, which is a mild positive check on data quality, not a target conclusion.
- **This module alone cannot and does not conclude a therapeutic window exists or does not exist for CEACAM5** — see `../README.md`'s "Cannot prove." The GI-mucosal signal is exactly the known, already-managed liability class for CEACAM5-directed ADCs in the field; nothing in this run changes that baseline.
