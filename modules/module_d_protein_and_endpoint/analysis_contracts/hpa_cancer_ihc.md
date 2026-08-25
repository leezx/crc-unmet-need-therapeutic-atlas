# Module D analysis contract — HPA Pathology Atlas tumor-tissue IHC (all five targets)

**Status: LOCKED, HPA `cancer_data.tsv` colorectal-cancer category. Whole-tumor-section IHC scoring, NOT malignant-cell-specific membrane/surface density.**

Built 2026-08-25, alongside `pxd055821_protein_abundance.md` — this repository's first Module D evidence.

## Source

`DATA/registry/HPA_CRC_cancer_tissue` — distinct dataset entry from `DATA/registry/HPA_normal_tissue` (Module E only). `cancer_data.tsv.zip` (1.72 MB) is the classic HPA "Pathology Atlas" product: one row per gene x cancer type, with patient counts by IHC staining level (`High`/`Medium`/`Low`/`Not detected`).

The HPA `/about/download` page has been redesigned since this repository last used HPA (PR #73, 2026-08-11) into a JS-heavy interactive column builder that now only advertises one bulk `proteinatlas.tsv.zip` mega-file. This smaller, per-category file is still served at its legacy `/download/tsv/` URL — found by fetching `https://www.proteinatlas.org/humanproteome/cancer/data` directly and reading the embedded hrefs, not from the redesigned `/about/download` page. Two related cancer-layer files were also checked but not used: `cancer_prognostic_data.tsv.zip` (RNA/TCGA-based prognostics, not protein-level) and `cancer_cptac.tsv.zip` (CPTAC-MS differential expression — checked and confirmed to return **zero rows** for all five targets in "Colon AC", genuinely not usable).

## Method

1. `scripts/extract_hpa_cancer_ihc.py --gene <SYMBOL>` unzips `cancer_data.tsv`, filters to exact `Gene name` match, reports every cancer type scored for that gene, and specifically the `colorectal cancer` row.
2. Checksum-verified against `DATA/registry/HPA_CRC_cancer_tissue/file_inventory.tsv` before use — fails closed on missing file or checksum mismatch.

## Results (2026-08-25)

Run via `python3 scripts/extract_hpa_cancer_ihc.py --gene <SYMBOL>` for each of the five targets, `colorectal cancer` row only. Full per-cancer-type tables (all 20 tumor types HPA scores): `results/tgt_<target>_hpa_cancer_ihc.tsv` (gitignored, not committed — regenerable).

| Target | n patients | High | Medium | Low | Not detected |
|---|---:|---:|---:|---:|---:|
| CEACAM5 | 10 | 6 | 4 | 0 | 0 |
| ERBB2 | 11 | 0 | 3 | 2 | 6 |
| NECTIN4 | 10 | 0 | 1 | 7 | 2 |
| F3 | 12 | 0 | 0 | 12 | 0 |
| TACSTD2 | 12 | 0 | 0 | 3 | 9 |

## Interpretation, staying inside what this screen can prove

- **CEACAM5 is the only target with any `High` IHC calls in this cohort** (6 of 10 patients) — a real, corroborating protein-layer finding alongside its near-universal MS detection in `PXD055821` (see `pxd055821_protein_abundance.md`); this is a descriptive observation of two independent measurement types pointing the same direction, not a claim that either calibrates the other.
- **F3 is `Low` in all 12 scored patients, never `Not detected`** — a distinct pattern from its sparse MS detection (16/60, 26.7%) in `PXD055821`; these two sources are not directly comparable (different cohorts, different assay sensitivity, different malignant-vs-whole-tissue composition), so this is recorded as a real cross-source difference worth noting, not resolved or explained away.
- **TACSTD2 is `Not detected` in 9 of 12 patients** — despite reasonable MS detection (43/60, 71.7%) in `PXD055821`. Same caveat: different cohorts and assay types, not directly reconcilable here.
- **This is whole-tumor-section IHC, not malignant-cell-specific staining** — a standard HPA Pathology Atlas cohort (n~10-12 patients, one core/section per patient scored by pathologists for overall staining intensity), not a cell-type-resolved read like Module E's `normal_ihc_data.tsv.zip`. Per this repository's Module D contract: does not by itself establish surface/membrane density. `evidence_directness=UNCALIBRATED_PROXY` for all five `target_evidence.tsv` rows (`TE037`-`TE041`).
- `indication_id=surface_target_therapeutic_window` (`TARGET_REVIEW_FRAME`, `ANY` disease_state/treatment_line/prior_therapy) — chosen because HPA's Pathology Atlas cohort is a generic colorectal-cancer cohort, not specifically liver-metastatic or treatment-line-defined; neither `mcrc_liver_metastasis` nor `mcrc_preop_chemotherapy_crlm` is supported by what this source actually states about its own cohort. This is a real, deliberate choice, not a default — flagged here for reviewer scrutiny.
