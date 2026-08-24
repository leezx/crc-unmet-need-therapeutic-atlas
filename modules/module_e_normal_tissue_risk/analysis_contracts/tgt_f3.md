# Module E analysis contract — `tgt_f3`

## Method

`scripts/extract_normal_tissue_rna.py --gene F3` — same pure extraction as prior targets. The IHC extraction ran and returned exactly 1 row (`Tissue=N/A`, `Level=N/A`, `Reliability=Uncertain`) — a genuine HPA data gap, not a script error (script only hard-fails on zero rows; see `data_lock/tgt_f3.md`).

## Results (2026-08-24)

Full tables (not committed — regenerate via the script above): `results/tgt_f3_normal_tissue_rna.tsv` (40 HPA + 68 GTEx RNA rows), `results/tgt_f3_normal_tissue_ihc.tsv` (1 uninformative row).

**RNA, key compartments** (HPA nTPM / GTEx median TPM):

| Compartment | HPA nTPM | GTEx median TPM |
|---|---:|---|
| colon | 35.6 | Colon_Sigmoid 22.5; Colon_Transverse 68.6 |
| rectum | 39.5 | (no GTEx rectum tissue) |
| small intestine | 36.2 | Small_Intestine_Terminal_Ileum 71.4 |
| liver | 4.7 | Liver 2.1 |
| lung | 39.5 | Lung 102.7 |
| kidney | 11.6 | Kidney_Cortex 13.2; Kidney_Medulla 4.8 |
| heart | 34.4 | Heart_Atrial_Appendage 10.9; Heart_Left_Ventricle 13.9 |
| skin | 28.8 | Skin (both sites) 63.1 / 84.9 |
| bone marrow | 3.7 | not in GTEx v11's adult panel |

**RNA, top 5 non-key HPA tissues**: placenta 125.0, adipose tissue 88.4, urinary bladder 61.0, endometrium 57.1, seminal vesicle 56.9.

**IHC**: no usable data (see `data_lock/tgt_f3.md`).

## Interpretation, staying inside what this module can prove

- `F3` RNA is broadly expressed and, notably, **highest in placenta (125.0 nTPM) and adipose tissue (88.4)** — both well above any of the 9 key compartments this module tracks (max: lung 39.5). This matches `F3`'s known biology as tissue factor, constitutively expressed by placental trophoblasts and perivascular/stromal cells as part of normal hemostasis, not a GI- or organ-specific pattern.
- Lung (39.5 HPA nTPM, 102.7 GTEx median TPM — the highest GTEx value among the 9 key compartments) is the highest-RNA key compartment for `F3`, similar in relative rank to what `CEACAM5` showed, but **this cannot be corroborated or de-escalated by IHC** the way `CEACAM5`'s lung signal was, because no usable IHC exists for `F3`. This is a real, stated evidentiary gap, not a finding either way.
- **This module alone still cannot and does not conclude a therapeutic window exists or does not exist for `F3`**, and for this target specifically the module's own core "protein/IHC-first triage" principle (`../README.md`) cannot be applied — the assessment rests on bulk RNA alone. A future pass could look for a different IHC source (a research antibody study, a separate tissue atlas) if this target is shortlisted and this gap becomes decision-relevant; not attempted here.
