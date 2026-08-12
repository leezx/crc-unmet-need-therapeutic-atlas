# Cell QC rules v1 — GSE178318

Status: proposed for review before patient-level state scoring.  
Input contract: `figure1_gse178318.md`, `data_lock_GSE178318.tsv`, `figure1_marker_set_v1.tsv`.

## Primary rule

For the first descriptive pass, retain cells with:

- `detected_genes >= 200`; and
- `total_counts >= 500`.

These are global lower floors chosen after inspecting the locked per-sample distributions. They are not claims about cell identity and are applied before state scoring. No upper cutoff is applied at v1 because the current structural pass does not provide doublet scores, ambient-RNA estimates or a validated high-count artifact rule.

## Deferred metrics

- Mitochondrial and ribosomal fractions must be calculated from the locked gene index before they can be used.
- No mitochondrial, ribosomal, stress, cell-cycle or doublet threshold may be added silently.
- Cells failing the primary rule are excluded from the primary descriptive score but retained in the QC sensitivity report.

## Sensitivity analysis

Repeat the patient/specimen aggregation under two prespecified alternatives:

1. permissive: `detected_genes >= 100` and `total_counts >= 300`;
2. stringent: `detected_genes >= 300` and `total_counts >= 1,000`.

The direction of any paired primary-versus-liver-metastasis effect must be reported under all three rules. If the number of retained cells or patient-level paired specimens changes materially, the result is QC-sensitive and cannot advance to a state claim without review.

## Statistical and interpretation boundary

- Filtering occurs at cell level; inference remains at patient or matched-pair level.
- PBMC specimens are reconciliation/QC references and are excluded from the primary epithelial comparison.
- QC rules do not establish malignancy, plasticity, therapeutic relevance or clinical indication.
- Failure conditions: missing per-cell metrics, untracked rule version, fewer than three matched patient pairs after filtering, or direction reversal across the primary and sensitivity rules.
