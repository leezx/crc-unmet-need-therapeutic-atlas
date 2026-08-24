# Module E analysis contract — `tgt_nectin4`

## Method

`scripts/extract_normal_tissue_rna.py --gene NECTIN4` — same pure extraction as prior targets.

## Results (2026-08-24)

Full tables (not committed — regenerate via the script above): `results/tgt_nectin4_normal_tissue_rna.tsv` (40 HPA + 68 GTEx RNA rows), `results/tgt_nectin4_normal_tissue_ihc.tsv` (80 IHC tissue/cell-type rows).

**RNA, key compartments** (HPA nTPM / GTEx median TPM):

| Compartment | HPA nTPM | GTEx median TPM |
|---|---:|---|
| colon | 1.4 | Colon_Sigmoid 0.13; Colon_Transverse 1.87 |
| rectum | 1.6 | (no GTEx rectum tissue) |
| small intestine | 0.5 | Small_Intestine_Terminal_Ileum 1.05 |
| liver | 0.0 | Liver 0.08 |
| lung | 3.3 | Lung 6.64 |
| kidney | 0.9 | Kidney_Cortex 2.95; Kidney_Medulla 3.19 |
| heart | 0.0 | Heart_Atrial_Appendage 0.08; Heart_Left_Ventricle 0.06 |
| skin | 64.1 | Skin (both sites) 227.6 / 227.4 |
| bone marrow | 0.6 | not in GTEx v11's adult panel |

**RNA, top 5 non-key HPA tissues**: esophagus 39.8, urinary bladder 15.7, salivary gland 15.6, tonsil 13.6, breast 12.8.

**IHC, all High/Medium rows (8 of 80, all Medium — none High)**:

| Level | Tissue | Cell type |
|---|---|---|
| Medium | Breast | glandular cells, myoepithelial cells |
| Medium | Esophagus | squamous epithelial cells |
| Medium | Oral mucosa | squamous epithelial cells |
| Medium | Skin | keratinocytes, epidermal cells |
| Medium | Tonsil | squamous epithelial cells |
| Medium | Urinary bladder | urothelial cells |

Every other row (72 of 80) is Low or Not detected.

## Interpretation, staying inside what this module can prove

- `NECTIN4` RNA and IHC are both **strongly skin-dominated**: skin RNA (64.1 HPA nTPM, 227.5 GTEx median TPM) is by far the highest of any compartment tracked (colon/rectum are both <2 nTPM), and the IHC layer directly corroborates this at the protein level — **skin keratinocytes and epidermal cells both score Medium**. Enfortumab vedotin (the approved anti-`NECTIN4` ADC) carries a documented clinical skin-toxicity warning, but this row does not cite that external source and makes no causal on-target/off-tumor claim (corrected 2026-08-24, PR #76 round 1 review) — it reports only the HPA RNA/IHC finding itself.
- The IHC layer also shows squamous-epithelium involvement beyond skin (esophagus, oral mucosa, tonsil — all Medium, squamous epithelial cells), a coherent pattern across squamous/keratinized epithelium, not scattered across unrelated tissues. **Esophagus is itself GI tract** — its Medium IHC signal means this is not a GI-wide absence.
- Colon/rectum RNA is very low (1.4 / 1.6 nTPM) with no IHC row scored High/Medium specifically in colon, rectum, or small intestine — `NECTIN4`'s low signal is **colorectal/lower-intestinal**, not GI-wide (corrected 2026-08-24, PR #76 round 1 review — an earlier version of this line said "no GI-mucosal signal," directly contradicted by the esophagus Medium row two lines above; esophagus, oral mucosa and tonsil are all upper-GI/oropharyngeal tissue with a real Medium signal). This is still a materially different pattern from `CEACAM5`'s colon/rectum-High signal.
- **This module alone still cannot and does not conclude a therapeutic window exists or does not exist for `NECTIN4`** — see `../README.md`'s "Cannot prove."
