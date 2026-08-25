# Module D analysis contract — HPA Pathology Atlas tumor-tissue IHC (all five targets)

**Status: LOCKED, HPA `cancer_data.tsv` colorectal-cancer category. Cancer-cell IHC staining category (intensity + fraction of positive cancer cells), NOT membrane-specific, NOT quantitative antigen density.**

Built 2026-08-25, alongside `pxd055821_protein_abundance.md` — this repository's first Module D evidence.

Revised 2026-08-25 (PR #82 round 1 review) after independently fetching HPA's own cancer-methods page (`https://www.proteinatlas.org/humanproteome/cancer/method`): the original version of this file called this evidence "whole-tumor-section IHC, NOT malignant-cell-specific" — HPA's own methodology text says otherwise: "All images were then analyzed by pathologists and annotated with respect to **staining intensity and fraction of positive cancer cells** for all approved antibodies. The result of immunohistochemistry-based protein expression was then summarized as high, medium, low or not detected." This is a **cancer-cell-focused** IHC annotation, not a bulk score mixing stromal/immune/background signal with tumor signal — corrected throughout below. This makes the evidence somewhat stronger than the original characterization, but it still does not establish membrane-specific, quantitative antigen density — `evidence_directness` stays `UNCALIBRATED_PROXY`, not upgraded.

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

- **CEACAM5 is the only target with any `High` IHC calls in this cohort** (6 of 10 patients) — a real observation. Its `PXD055821` mass-spec detection (see `pxd055821_protein_abundance.md`) is also 100% (60/60 specimens); these are two independent, cancer-cell-relevant protein-layer sources both showing real signal for `CEACAM5`, reported here as a descriptive observation, not a claim that either source calibrates the other or that the two are being combined into a joint score.
- **F3 is `Low` in all 12 scored patients, never `Not detected`, by IHC** — its `PXD055821` mass-spec detection fraction is 16/60 (26.7%). These are two different measurement types in different cohorts with different assay sensitivity; recorded here as a real, unreconciled pattern specific to `F3`, not resolved or explained away, and not compared against the other four targets as a ranking.
- **TACSTD2 is `Not detected` in 9 of 12 patients by IHC**, despite a 43/60 (71.7%) `PXD055821` mass-spec detection fraction. Same caveat as `F3`: a real, unreconciled cross-source pattern specific to this target, not a cross-target comparison.
- **Every target's IHC and MS reads are reported on their own terms** — the five targets' `PXD055821` detection fractions are not a calibrated cross-protein abundance scale (different MS response per protein), and different HPA target antibodies are not a calibrated cross-antibody intensity scale either (per this repository's Module D contract). Neither source licenses statements like "target X's protein signal is weaker/stronger/sparser than target Y's."
- **This is cancer-cell-focused IHC (intensity + fraction of positive cancer cells, per HPA's own methodology, independently confirmed above), not membrane-specific or quantitative antigen density** — a standard HPA Pathology Atlas cohort (n~10-12 patients, one TMA core per patient), not a cell-type-resolved read like Module E's `normal_ihc_data.tsv.zip`. Per this repository's Module D contract: does not by itself establish surface/membrane density (ADC-relevant evidence needs malignant-cell membrane localization → accessible antigen density → antibody-specific binding/internalization → delivery; this source addresses only the first of those steps, and even there only qualitatively). `evidence_directness=UNCALIBRATED_PROXY` for all five `target_evidence.tsv` rows (`TE037`-`TE041`) — unchanged despite this being a more direct cancer-cell read than originally characterized.
- `indication_id=surface_target_therapeutic_window` (`TARGET_REVIEW_FRAME`, `ANY` disease_state/treatment_line/prior_therapy) — chosen because HPA's Pathology Atlas cohort is a generic colorectal-cancer cohort, not specifically liver-metastatic or treatment-line-defined; neither `mcrc_liver_metastasis` nor `mcrc_preop_chemotherapy_crlm` is supported by what this source actually states about its own cohort. This is a real, deliberate choice, not a default — flagged here for reviewer scrutiny.
