# Module E analysis contract — `tgt_ceacam5`

Revised 2026-08-23 (PR #73 round 1 review): adds the HPA IHC extraction, corrects "HPA RNA tissue consensus" to the correct product name, and softens two claims that had drifted past what bulk RNA alone supports. See `data_lock/tgt_ceacam5.md` for the full provenance correction.

## Method

`scripts/extract_normal_tissue_rna.py --gene CEACAM5` — a pure extraction (no imputation, no cross-source averaging, no download). Pulls every HPA-tissue RNA row, every GTEx-tissue RNA column, and every HPA IHC tissue/cell-type row matching `CEACAM5` exactly. Writes RNA and IHC results as two separate tables and prints the module's named "key compartments" (colon, small intestine, liver, lung, kidney, heart, skin, bone marrow), the top 5 non-key HPA RNA tissues by value, and every IHC row scored High or Medium — so a surprising tissue or cell type is never silently dropped from either layer.

## Thresholds / naming rule

No `RNA_no/low/high` bucket rule here (that is Module B's malignant-cell-fraction rule, not applicable to normal-tissue bulk RNA). The judgment made is **"worth a closer protein/IHC look" (RNA) vs "confirmed by IHC" (or not)**, using each source's own units at face value, no cross-source unit conversion (HPA nTPM, GTEx median TPM, HPA IHC categorical level are three different scales, read within themselves, never blended into one number).

## Results (2026-08-23)

Full tables (not committed — `modules/*/results/` is gitignored, regenerate via the script above): `results/tgt_ceacam5_normal_tissue_rna.tsv` (40 HPA + 68 GTEx RNA rows), `results/tgt_ceacam5_normal_tissue_ihc.tsv` (109 IHC tissue/cell-type rows).

**RNA, key compartments** (HPA nTPM / GTEx median TPM):

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

**RNA, GTEx colon/esophagus subregions**: `Colon_Transverse_Mucosa` 1069.6, `Colon_Transverse_Mixed_Cell` 1120.6, `Colon_Transverse_Muscularis` 75.4; `Esophagus_Mucosa` 277.8 vs `Esophagus_Muscularis` 0.14. `Colon_Sigmoid` (0.74) vs `Colon_Transverse` (243.7) is an unexplained within-organ discrepancy, not resolved by this data.

**RNA, top 5 non-key HPA tissues**: appendix 175.2, stomach 154.1, esophagus 148.8, tonsil 34.6, smooth muscle 26.8.

**IHC, all High/Medium rows (18 of 109)**:

| Level | Tissue | Cell type |
|---|---|---|
| High | Appendix / Colon / Rectum | enterocytes, enterocytes - Microvilli, endocrine cells, goblet cells (12 rows total) |
| Medium | Colon / Rectum | mucosal lymphoid cells |
| Medium | Esophagus, Oral mucosa | squamous epithelial cells |
| Medium | Stomach | glandular cells (x2, two stomach sub-samples) |

Every other row, including **lung alveolar cells type I and II (both Low)**, **bone marrow hematopoietic cells (Low)**, and tonsil/smooth muscle (not scored High/Medium in any cell type present in those tissues), is Low or Not detected.

## Interpretation, staying inside what this module can prove

- CEACAM5's RNA and IHC signal is **predominantly enriched in GI tissues** (colon, rectum, appendix, small intestine, stomach, esophagus) — matches, does not contradict, its known role as a GI epithelial differentiation antigen.
- The IHC layer **does not corroborate** the RNA-only flag on lung, tonsil and smooth muscle from the earlier round of this run: none of them show a High or Medium signal in any HPA-scored cell type. Lung alveolar cells (type I and II, the two cell types HPA scored) are both Low — the RNA-level lung signal (28.5 HPA nTPM) does not correspond to a strong protein signal in those specific cell types. This lowers, but does not eliminate, the concern: HPA's cell-type panel is not exhaustive, and Low is not zero accessible surface antigen.
- Within GI tissue, IHC also shows a real gradient the RNA alone didn't resolve: small intestine/duodenum enterocytes are Not detected while colon/rectum/appendix enterocytes are High — CEACAM5 protein expression is distally weighted along the GI tract, not uniform across all small-and-large-intestine epithelium.
- Mucosal lymphoid cells (Colon/Rectum, Medium) are immune infiltrate, not epithelium — a separate finding, not folded into the epithelial pattern.
- **This module alone still cannot and does not conclude a therapeutic window exists or does not exist for CEACAM5** — see `../README.md`'s "Cannot prove." IHC intensity is not a quantitative surface-density assay. Whether CEACAM5-directed ADCs in the clinic have or have not managed GI toxicity is an external clinical-literature question this run does not speak to and does not claim to answer.
