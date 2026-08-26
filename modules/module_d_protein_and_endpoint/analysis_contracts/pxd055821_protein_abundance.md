# Module D analysis contract — `PXD055821` tumor-tissue protein abundance (all five targets)

**Status: LOCKED, DIA-NN gene-group intensity matrix for the project's 60-specimen "Sydney cohort" sub-cohort. Whole-tissue mass-spec protein abundance, NOT malignant-cell-specific membrane/surface density.**

Built 2026-08-25 (first Module D pass), after the round-3 reviewer of PR #81 (Module B's `GSE225857` second-cohort screen) explicitly recommended returning to gaps that affect ADC asset selection rather than continuing to invest in the same Module B dataset — this is Module D's first real evidence.

Revised 2026-08-25 (PR #82 round 1 review) after independently fetching the publication's own full text (PMC12335997, DOI `10.1016/J.MCPRO.2025.101026`): the original version of this file called the matrix's 60 columns "samples" and left the `63`-vs-`60` filename discrepancy as fully unexplained. Both corrected below — see "What's actually usable" and "Results" for the exact publication text and the resolved unit.

## What's actually usable in this project, and what isn't

`PXD055821` (152 CRC-LM specimens from 111 patients across 3 centers, 3 proteomic phenotypes, Mol Cell Proteomics 2025, DOI `10.1016/J.MCPRO.2025.101026`) is a mixed Proteome Discoverer/DIA-NN search project. The PRIDE API file listing (174 total files) shows:

- ~150 raw `.raw` files (~0.9-1.1 GB each) — **not usable here**, no proteomics search-engine software (MaxQuant, Proteome Discoverer, Spectronaut) is available or installable in this environment.
- Two `.pdResult`/`.msf` Proteome Discoverer result files (44-54 GB) — **not usable here**, proprietary format, no reader available, and far too large to download in any case.
- Two small, already-processed DIA-NN output matrices for the project's Sydney sub-cohort: `220920_PN_CRC_LM_all_63_LM_DIANN.gg_matrix.tsv` (gene-group level, 3.48 MB) and `...pg_matrix.tsv` (protein-group level, 4.06 MB, available from PRIDE but not downloaded/not used). **This contract uses only the gene-group matrix** — it is gene-symbol-indexed, matching this repository's `target_id`/`target_symbol` convention directly.

**The 60 columns correspond exactly to the publication's own "Sydney cohort"** — independently confirmed by fetching the paper's own full text: "the third cohort was from the tumor bank of the Kolling Institute, Royal North Shore Hospital in Sydney, Australia and comprised **60 specimens collected from 51 patients**... samples of the third cohort were processed and measured [by DIA-NN] at the Kolling Institute." (The other two centers — UKSH, 42 specimens/42 patients, and UKE, 50 specimens/18 patients — were processed by Proteome Discoverer, not DIA-NN, and are among the unusable files above.) The filename says `all_63_LM`, but the matrix has exactly **60 columns**, matching the publication's own stated Sydney-cohort size — so the `63` is very likely stale/mismatched naming from an earlier draft of the run, not an unexplained data-content gap; the reason for the stale filename itself remains unresolved.

**Columns are specimens, not independent patients.** 60 specimens from 51 patients means some patients contributed more than one specimen — the exact per-patient breakdown is not stated in the publication text fetched here and is not resolved further. Column headers are the original Windows file paths DIA-NN recorded for each MS run (e.g. `H:\Paula\CRC_LM\...\220624_CRCLM_PN_S24.mzML`) — **not resolved to patient IDs**. Every detection-fraction figure below is a **specimen-level** read, not a patient-level prevalence and not "60 independent patients."

## Method

1. `scripts/extract_pxd055821_protein_abundance.py --gene <SYMBOL>` streams the 9,263-gene matrix, finds the one row matching the gene symbol exactly, and computes: number of specimens with a genuinely nonzero intensity value (`detected` -- a blank cell and a literal `0` are both treated as not detected, matching DIA-NN's convention and this contract's own "nonzero intensity" claim), detection fraction, median/min/max of the detected values.
2. Checksum-verified against `DATA/registry/PXD055821/file_inventory.tsv` before use — fails closed on missing file or checksum mismatch.

## Results (2026-08-25)

Run via `python3 scripts/extract_pxd055821_protein_abundance.py --gene <SYMBOL>` for each of the five targets. Full per-specimen tables: `results/tgt_<target>_pxd055821_protein_abundance.tsv` (gitignored, not committed — regenerable).

| Target | Detected / 60 specimens | Detection fraction | Median | Min | Max |
|---|---:|---:|---:|---:|---:|
| CEACAM5 | 60/60 | 100.0% | 3.715e+07 | 9.083e+05 | 1.83e+08 |
| ERBB2 | 56/60 | 93.3% | 2.191e+05 | 9.508e+04 | 1.12e+06 |
| TACSTD2 | 43/60 | 71.7% | 3.025e+05 | 2.304e+04 | 4.46e+06 |
| F3 | 16/60 | 26.7% | 1.384e+05 | 3.017e+04 | 8.679e+05 |
| NECTIN4 | 13/60 | 21.7% | 6.913e+04 | 4.201e+04 | 1.297e+05 |

(Intensity units are DIA-NN's own arbitrary gene-group intensity scale — **not directly comparable across genes**, since different proteins have different ionization efficiency, peptide count, and MS response; the detection-fraction column is likewise not a calibrated cross-gene abundance ranking, since per-protein MS sensitivity affects it independently of true biological abundance — this table reports target-specific facts side by side for reference, not a ranking.)

## Interpretation, staying inside what this screen can prove

- **CEACAM5 is detected in every one of the 60 specimens (100%)** — consistent with (not confirmatory of) it being a real, MS-detectable tumor-tissue protein in this CRLM cohort, matching the fact that `CEACAM5` is explicitly named as a discovered biomarker in this project's own publication.
- **Each target's own detection fraction is reported on its own terms** (see table) — not compared against the other four as a ranking. The five proteins differ in MS response, peptide count, and ionization efficiency (noted above), so a lower detection fraction for one target than another is not license to call one target's protein signal "weaker" or "sparser" than another's in a calibrated sense.
- **This is whole-tissue mass spectrometry, not malignant-cell-specific proteomics** — a bulk CRC-LM specimen contains tumor, stroma, immune infiltrate, and normal parenchyma; detection in "60/60 specimens" does not mean the protein is present on the surface of malignant cells specifically, let alone at a therapeutically accessible density. Per this repository's Module D contract (`modules/module_d_protein_and_endpoint/README.md`): "Whole-tissue MS ≠ malignant-cell-specific membrane density." `evidence_directness=UNCALIBRATED_PROXY` for all five `target_evidence.tsv` rows (`TE032`-`TE036`).
- **This is a real, independent, protein-layer measurement type** — distinct from every RNA-based read this repository has produced so far (Module B's scRNA screens, Module E's bulk RNA), and a genuinely different failure mode: an RNA-high target with low/no MS protein detection would be a real, actionable discrepancy this repository could not have surfaced from RNA data alone. See `hpa_cancer_ihc.md` for a second, independent (antibody-based IHC) protein-layer read on the same five targets.
- `indication_id=mcrc_liver_metastasis` (anatomy-only, `ANY` treatment_line/prior_therapy) — chosen because this project's own description is explicitly CRC liver metastasis specimens; no treatment-status claim is made, since this sub-cohort's own treatment history is not resolved here.

## Protein-group-level confirmatory check (2026-08-25, Next-handoff item 3e(c); tightened round 1 review of PR #87)

DIA-NN also outputs a protein-group-level matrix, `220920_PN_CRC_LM_all_63_LM_DIANN.pg_matrix.tsv` (4.06 MB, same 60-specimen Sydney-cohort columns; downloaded and checksummed — `DATA/registry/PXD055821/file_inventory.tsv`), separate from the gene-group-level `gg_matrix.tsv` this evidence is actually built from. Protein-group-level output can in principle differ from gene-group-level output when a gene maps to more than one protein group in this DIA-NN output (additional group-level splitting the gene-group summary would collapse) or a protein group's peptides are shared across more than one gene (a multi-gene/multi-accession group DIA-NN could not cleanly assign to one gene). New `scripts/compare_pxd055821_pg_vs_gg_matrix.py` (tested by `scripts/test_compare_pxd055821_pg_vs_gg_matrix.py`, including fixtures asserting that both ambiguity cases are actually flagged as failures, not merely parsed) checks this for the five `A_CLINICAL` targets only — it does not resess DIA-NN's protein inference for the other ~9,250 genes in the matrix, and specimen-column identity/order between the two files is asserted before any value is compared.

**Result: no additional protein-group-level ambiguity is represented for these five targets in this specific DIA-NN output.** Each of the five targets' matching `pg_matrix` row has a `Genes` field naming only that target (not shared with another gene) and a `Protein.Group`/`Protein.Ids` field naming exactly one UniProt accession (`CEACAM5`=P06731, `ERBB2`=P04626, `F3`=P13726, `NECTIN4`=Q96NY8, `TACSTD2`=P09758), and all 60 parsed specimen values match the gene-group matrix row already used in `TE032`-`TE036` exactly. **This does not establish absence of biological isoforms or proteoforms** — an isoform not present in DIA-NN's search database could not appear in this table regardless of protein-group vs. gene-group granularity, and PTM-defined proteoforms are not separately resolved by protein-group-level output either; this file only reports what this specific DIA-NN search/inference run did or didn't split or share. **This is a confirmatory check, not a new evidence source**: it adds no new numeric value and changes no `target_evidence.tsv` field. The gene-group matrix (`gg_matrix.tsv`) remains the source of record for `TE032`-`TE036`.
