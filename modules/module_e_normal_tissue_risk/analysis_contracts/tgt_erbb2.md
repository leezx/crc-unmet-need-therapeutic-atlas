# Module E analysis contract — `tgt_erbb2`

## Method

`scripts/extract_normal_tissue_rna.py --gene ERBB2` — same pure extraction as `tgt_ceacam5.md` (no imputation, no cross-source averaging). Pulls every HPA-tissue RNA row, every GTEx-tissue RNA column, and every HPA IHC tissue/cell-type row matching `ERBB2` exactly.

## Results (2026-08-24)

Full tables (not committed — regenerate via the script above): `results/tgt_erbb2_normal_tissue_rna.tsv` (40 HPA + 68 GTEx RNA rows), `results/tgt_erbb2_normal_tissue_ihc.tsv` (126 IHC tissue/cell-type rows).

**RNA, key compartments** (HPA nTPM / GTEx median TPM):

| Compartment | HPA nTPM | GTEx median TPM |
|---|---:|---|
| colon | 63.8 | Colon_Sigmoid 31.9; Colon_Transverse 50.6 |
| rectum | 45.5 | (no GTEx rectum tissue) |
| small intestine | 63.4 | Small_Intestine_Terminal_Ileum 44.0 |
| liver | 28.4 | Liver 13.4 |
| lung | 34.1 | Lung 48.7 |
| kidney | 56.1 | Kidney_Cortex 52.9; Kidney_Medulla 92.5 |
| heart | 44.5 | Heart_Atrial_Appendage 36.8; Heart_Left_Ventricle 20.9 |
| skin | 84.8 | Skin (both sites) 110.3 / 117.6 |
| bone marrow | 1.3 | not in GTEx v11's adult panel |

**RNA, top 5 non-key HPA tissues**: esophagus 77.7, parathyroid gland 76.8, fallopian tube 60.4, duodenum 59.8, salivary gland 54.8.

**IHC, all High/Medium rows (19 of 126, all Medium — none High)**:

| Level | Tissue | Cell type |
|---|---|---|
| Medium | Appendix | glandular cells |
| Medium | Breast | glandular cells, myoepithelial cells |
| Medium | Cervix | glandular cells |
| Medium | Endometrium | glandular cells (x2) |
| Medium | Fallopian tube | ciliated cells (ciliary rootlets) |
| Medium | Heart muscle | cardiomyocytes |
| Medium | Lung | alveolar cells type I |
| Medium | Nasopharynx | ciliated cells (cell body) |
| Medium | Placenta | decidual cells, trophoblastic cells |
| Medium | Skeletal muscle | myocytes |
| Medium | Skin | cells in granular layer, cells in spinous layer, langerhans cells |
| Medium | Testis | elongated/late spermatids, round/early spermatids |
| Medium | Urinary bladder | urothelial cells |

Every other row (107 of 126) is Low or Not detected.

## Interpretation, staying inside what this module can prove

- Unlike `CEACAM5`, `ERBB2` RNA is **not GI-mucosa-dominated** — colon (63.8) and rectum (45.5) are mid-range, well below skin (84.8), esophagus (77.7), parathyroid gland (76.8) and fallopian tube (60.4). Expression is broad across many normal epithelial/glandular tissues, not a GI-restricted antigen (this observation is about this run's own RNA pattern, not a claim about `ERBB2`'s biological role generally).
- The IHC layer shows a real protein-level signal not visible from RNA alone: **cardiomyocytes (Medium)** and **lung alveolar cells type I (Medium)**. This row reports only what HPA's cell-type IHC panel shows for `ERBB2` protein expression in those two cell types — no external clinical, drug, or toxicity context is asserted (corrected 2026-08-24, PR #76 round 2 review: an earlier version of this document, even after round 1's fix, still characterized these tissues as "clinically-monitored toxicity domains for approved anti-HER2 ADCs," itself an uncited external clinical claim; that framing belongs in a future Module F/clinical-precedent pass, not this Module E run — see `../README.md`'s "Cannot prove").
- No cell type scores High anywhere in this panel — every flagged row is Medium, a materially different pattern from `CEACAM5`'s GI-restricted High signal.
- Placenta (decidual + trophoblastic, both Medium) and testis (spermatid stages, both Medium) are reproductive-tissue findings, a separate category from the cardiac/pulmonary signal above, not folded into it.
- **This module alone still cannot and does not conclude a therapeutic window exists or does not exist for `ERBB2`** — see `../README.md`'s "Cannot prove." IHC intensity is not a quantitative surface-density assay, and this run does not use or need external clinical-trial toxicity data to make its own claim; it only reports what this repository's own screen shows.
