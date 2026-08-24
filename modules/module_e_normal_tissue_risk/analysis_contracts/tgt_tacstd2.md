# Module E analysis contract — `tgt_tacstd2`

## Method

`scripts/extract_normal_tissue_rna.py --gene TACSTD2` — same pure extraction as prior targets.

## Results (2026-08-24)

Full tables (not committed — regenerate via the script above): `results/tgt_tacstd2_normal_tissue_rna.tsv` (40 HPA + 68 GTEx RNA rows), `results/tgt_tacstd2_normal_tissue_ihc.tsv` (99 IHC tissue/cell-type rows).

**RNA, key compartments** (HPA nTPM / GTEx median TPM):

| Compartment | HPA nTPM | GTEx median TPM |
|---|---:|---|
| colon | 0.9 | Colon_Sigmoid 1.62; Colon_Transverse 1.66 |
| rectum | 0.9 | (no GTEx rectum tissue) |
| small intestine | 0.6 | Small_Intestine_Terminal_Ileum 2.63 |
| liver | 3.8 | Liver 1.89 |
| lung | 67.1 | Lung 162.0 |
| kidney | 74.5 | Kidney_Cortex 74.9; Kidney_Medulla 339.9 |
| heart | 0.4 | Heart_Atrial_Appendage 0.65; Heart_Left_Ventricle 0.27 |
| skin | 225.6 | Skin (both sites) 928.7 / 898.9 |
| bone marrow | 12.7 | not in GTEx v11's adult panel |

**RNA, top 5 non-key HPA tissues**: esophagus 365.6, urinary bladder 219.0, salivary gland 178.4, tonsil 168.8, breast 127.4.

**IHC, all High/Medium rows (15 of 99)**:

| Level | Tissue | Cell type |
|---|---|---|
| High (x2 samples) | Skin | cells in granular layer, endothelial cells, hair follicles |
| High (x1 sample) | Skin | cells in spinous layer |
| Medium | Bronchus | respiratory epithelial cells |
| Medium | Cervix | squamous epithelial cells |
| Medium | Esophagus | squamous epithelial cells |
| Medium | Kidney | collecting ducts |
| Medium | Nasopharynx | respiratory epithelial cells |
| Medium | Oral mucosa | squamous epithelial cells |
| Medium | Seminal vesicle | glandular cells |
| Medium | Urinary bladder | urothelial cells |

(HPA scores skin from two separate patient samples for this gene, each independently High on granular-layer/endothelial/hair-follicle cell types — recorded as duplicate rows in the raw table, not merged here.) Every other row (84 of 99) is Low or Not detected.

## Interpretation, staying inside what this module can prove

- `TACSTD2` RNA and IHC show **very low colon/rectum/small-intestine signal alongside broad non-colorectal epithelial normal-tissue expression** — not simply "skin-dominated" (corrected 2026-08-24, PR #76 round 1 review; see below for why). Colon/rectum RNA is the lowest of any of the five targets run so far (0.9 nTPM each), with no IHC row scored High/Medium specifically in colon, rectum, or small intestine. But skin, esophagus (365.6 nTPM — higher than skin's own 225.6), urinary bladder, salivary gland, tonsil, lung and kidney all carry substantial RNA and/or IHC signal (below) — this is a **broad non-colorectal epithelial expression pattern**, not a single-tissue liability. Skin IHC reaches **High** (not just Medium) across multiple cell types in two independent skin samples, the strongest single signal, but not the only one worth carrying forward. No causal clinical-toxicity claim is made here (an earlier version of this document cited sacituzumab govitecan's "well-documented clinical skin toxicity" without a source, and that characterization is itself inaccurate — see `question/tgt_tacstd2.md`).
- Beyond skin, the Medium-level IHC pattern is coherent with a broad squamous/transitional/glandular/respiratory epithelium involvement (esophagus, cervix, oral mucosa — squamous; urinary bladder — urothelial; bronchus, nasopharynx — respiratory epithelium), matching `TACSTD2`'s known biology as a pan-epithelial differentiation marker, not organ-restricted. **Esophagus is itself GI tract** with a real Medium IHC signal — so "no GI tissue scored High/Medium" (an earlier version of this document's claim, directly contradicted by this same table) is wrong; the correct, narrower claim is no High/Medium IHC specifically in colon, rectum, or small intestine.
- Kidney is notable: 74.5 HPA nTPM and the highest single GTEx value across all compartments (Kidney_Medulla 339.9 median TPM), with IHC scoring kidney collecting ducts at Medium — a real, specific renal signal worth carrying forward if this target is shortlisted.
- **This module alone still cannot and does not conclude a therapeutic window exists or does not exist for `TACSTD2`** — see `../README.md`'s "Cannot prove."
