# Module D analysis contract — `PXD055821` tumor-tissue protein abundance (all five targets)

**Status: LOCKED, DIA-NN gene-group intensity matrix for a 60-sample sub-cohort. Whole-tissue mass-spec protein abundance, NOT malignant-cell-specific membrane/surface density.**

Built 2026-08-25 (first Module D pass), after the round-3 reviewer of PR #81 (Module B's `GSE225857` second-cohort screen) explicitly recommended returning to gaps that affect ADC asset selection rather than continuing to invest in the same Module B dataset — this is Module D's first real evidence.

## What's actually usable in this project, and what isn't

`PXD055821` (152 CRLM samples, 3 centers, 3 proteomic phenotypes, Mol Cell Proteomics 2025, DOI `10.1016/J.MCPRO.2025.101026`) is a mixed Proteome Discoverer/DIA-NN search project. The PRIDE API file listing (174 total files) shows:

- ~150 raw `.raw` files (~0.9-1.1 GB each) — **not usable here**, no proteomics search-engine software (MaxQuant, Proteome Discoverer, Spectronaut) is available or installable in this environment.
- Two `.pdResult`/`.msf` Proteome Discoverer result files (44-54 GB) — **not usable here**, proprietary format, no reader available, and far too large to download in any case.
- Two small, already-processed DIA-NN output matrices for a sub-cohort: `220920_PN_CRC_LM_all_63_LM_DIANN.gg_matrix.tsv` (gene-group level, 3.48 MB) and `...pg_matrix.tsv` (protein-group level, 4.06 MB). **This contract uses only the gene-group matrix** — it is gene-symbol-indexed, matching this repository's `target_id`/`target_symbol` convention directly.

The filename says `all_63_LM`, but the matrix itself has exactly **60 sample columns**, verified by parsing the header — a real filename/content discrepancy, recorded as-is, not "corrected" to match the name and not investigated further (e.g. whether 3 samples were dropped after the file was named, or the name always referred to something else).

Sample columns are the original Windows file paths DIA-NN recorded for each MS run (e.g. `H:\Paula\CRC_LM\...\220624_CRCLM_PN_S24.mzML`) — **not resolved to patient IDs**. This is an aggregate, across-samples read (detection fraction, median, range), not a per-patient breakdown like Module B's screens.

## Method

1. `scripts/extract_pxd055821_protein_abundance.py --gene <SYMBOL>` streams the 9,263-gene matrix, finds the one row matching the gene symbol exactly, and computes: number of samples with a nonzero intensity value (`detected`), detection fraction, median/min/max of the detected values.
2. Checksum-verified against `DATA/registry/PXD055821/file_inventory.tsv` before use — fails closed on missing file or checksum mismatch.
3. Blank cells in the matrix are treated as missing (not detected), matching DIA-NN's own convention.

## Results (2026-08-25)

Run via `python3 scripts/extract_pxd055821_protein_abundance.py --gene <SYMBOL>` for each of the five targets. Full per-sample tables: `results/tgt_<target>_pxd055821_protein_abundance.tsv` (gitignored, not committed — regenerable).

| Target | Detected / 60 samples | Detection fraction | Median | Min | Max |
|---|---:|---:|---:|---:|---:|
| CEACAM5 | 60/60 | 100.0% | 3.715e+07 | 9.083e+05 | 1.83e+08 |
| ERBB2 | 56/60 | 93.3% | 2.191e+05 | 9.508e+04 | 1.12e+06 |
| TACSTD2 | 43/60 | 71.7% | 3.025e+05 | 2.304e+04 | 4.46e+06 |
| F3 | 16/60 | 26.7% | 1.384e+05 | 3.017e+04 | 8.679e+05 |
| NECTIN4 | 13/60 | 21.7% | 6.913e+04 | 4.201e+04 | 1.297e+05 |

(Intensity units are DIA-NN's own arbitrary gene-group intensity scale — **not directly comparable across genes**, since different proteins have different ionization efficiency, peptide count, and MS response; only within-gene comparisons across samples, or the detection-fraction column, carry any cross-gene meaning, and even detection fraction is affected by per-protein MS sensitivity, not purely biological abundance.)

## Interpretation, staying inside what this screen can prove

- **CEACAM5 and ERBB2 are detected in nearly all 60 samples** — consistent with (not confirmatory of) both being real, MS-detectable tumor-tissue proteins in this CRLM cohort, matching the fact that `CEACAM5` is explicitly named as a discovered biomarker in this project's own publication.
- **F3 and NECTIN4 are detected in a minority of samples** (26.7% and 21.7%) — could reflect genuinely lower/more variable protein abundance, or could reflect MS sensitivity limits for lower-abundance proteins; this method cannot distinguish those explanations.
- **This is whole-tissue mass spectrometry, not malignant-cell-specific proteomics** — a bulk CRLM tissue sample contains tumor, stroma, immune infiltrate, and normal parenchyma; detection in "60/60 samples" does not mean the protein is present on the surface of malignant cells specifically, let alone at a therapeutically accessible density. Per this repository's Module D contract (`modules/module_d_protein_and_endpoint/README.md`): "Whole-tissue MS ≠ malignant-cell-specific membrane density." `evidence_directness=UNCALIBRATED_PROXY` for all five `target_evidence.tsv` rows (`TE032`-`TE036`).
- **This is a real, independent, protein-layer measurement type** — distinct from every RNA-based read this repository has produced so far (Module B's scRNA screens, Module E's bulk RNA), and a genuinely different failure mode: an RNA-high target with low/no MS protein detection would be a real, actionable discrepancy this repository could not have surfaced from RNA data alone. See `hpa_cancer_ihc.md` for a second, independent (antibody-based IHC) protein-layer read on the same five targets.
- `indication_id=mcrc_liver_metastasis` (anatomy-only, `ANY` treatment_line/prior_therapy) — chosen because this project's own description is explicitly 152 CRLM samples; no treatment-status claim is made, since this sub-cohort's own treatment history is not resolved here.
