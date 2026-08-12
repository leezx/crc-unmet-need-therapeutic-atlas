# Figure 1 analysis contract — GSE178318

## Biological question

在 GSE178318 的 matched primary CRC / liver-metastasis 单细胞数据中，是否存在跨患者复现的恶性上皮 plasticity program，并且该 program 在 metastasis 或治疗暴露背景下具有患者级差异？

## Null and alternative hypotheses

- H0: after patient pairing and cell/QC correction, the candidate program score does not differ systematically between matched primary and liver-metastasis specimens.
- H1: the program shows a consistent paired direction in liver metastasis and/or a prespecified treatment-context interaction across patients.

## Inputs

- Official processed GSE178318 barcodes, genes and Matrix Market files.
- `DATA/registry/GSE178318/sample_map.tsv` for patient/specimen/treatment context.
- `phase2/03_data/data_lock_GSE178318.tsv` for checksum and dimension lock.

## Unit of analysis

- QC is performed at cell level.
- Inference is performed at patient level or matched-pair level; cells are never treated as independent patients.
- Cells without a recoverable sample/patient label are excluded from inferential comparisons and counted in a missingness report.

## QC contract

1. Verify gzip and Matrix Market dimensions against the data lock.
2. Verify barcode-derived sample IDs are present in the reviewed sample map.
3. Report per-sample cell count, detected genes and total counts.
4. Prespecify mitochondrial/ribosomal thresholds only after inspecting distributions; do not silently apply generic cutoffs.
5. Exclude doublets/low-quality cells only with a recorded rule and sensitivity table.

## State scoring contract

- The first pass is descriptive and uses the locked `phase2/04_analysis_contracts/figure1_marker_set_v1.tsv` marker set. The file version is part of the analysis input and cannot be changed after QC without a new reviewed contract.
- `FIG1_MARKER_V1` separates epithelial identity anchors, plasticity/non-canonical anchors and confounder genes; confounders are reported but excluded from the state score.
- Candidate programs must be separated from cell-cycle, stress and ribosomal programs.
- State scores are summarized by patient/specimen, not by pooled cells.
- A program is not called malignant without epithelial identity and malignant-cell context checks.

## Primary comparison

- Matched primary vs liver metastasis among patients with both specimens.
- Secondary stratification: treatment-naive vs preoperative-chemotherapy context, only if the paired sample count supports the comparison.
- Statistical model: paired effect size with patient as the blocking unit; permutation or Wilcoxon signed-rank as appropriate after checking the number of pairs.

## Outputs

- QC summary table and missingness report.
- Patient-level paired state-score table.
- Figure 1 state definition and replication-ready intermediate objects.
- No target ranking or clinical conclusion at this stage.

## Failure modes / stop conditions

- Barcode labels cannot be reconciled to sample map.
- Matrix orientation or dimensions do not match the data lock.
- Too few matched pairs for a stable paired comparison.
- The signal is explained by cell cycle, stress, mitochondrial content or batch.
- The state is not reproducible after patient-level aggregation.
