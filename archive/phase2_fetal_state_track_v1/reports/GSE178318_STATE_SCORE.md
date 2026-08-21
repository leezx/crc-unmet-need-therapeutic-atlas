# GSE178318 patient-level state-score report

Run date: 2026-08-11  
Command: `python3 scripts/score_gse178318_state.py`

Scores use the locked `FIG1_MARKER_V1` genes and the reviewed primary cell-QC rule (`detected_genes >= 200`, `total_counts >= 500`). Each cell contributes a library-size-normalized mean log1p marker score; inference is summarized across six matched patient pairs, not pooled cells.

The output also reports sample-level mean scores for the excluded cell-cycle genes (`MKI67`, `TOP2A`, `STMN1`) and stress genes (`FOS`, `JUN`, `HSPA1A`). These confounder scores are diagnostic only and are not included in any state score or paired effect.

| Program | Mean metastasis − primary | Positive pairs | Negative pairs | Exact two-sided sign-flip p |
|---|---:|---:|---:|---:|
| epithelial identity | -0.26450 | 2 | 4 | 0.3125 |
| plasticity anchor | -0.06759 | 1 | 5 | 0.21875 |
| noncanonical anchor | -0.00204 | 0 | 6 | 0.03125 |

These are descriptive exploratory outputs from six matched pairs. The p-values are not treated as confirmatory evidence; no multiplicity correction, independent replication, malignancy call, target ranking or clinical conclusion is made here. The full patient-level intermediate object remains local and ignored at `phase2/06_results/GSE178318/state_scores.json`.

The next gate is independent validation and sensitivity to marker/program definition. The current result does not support a therapeutic target claim.
