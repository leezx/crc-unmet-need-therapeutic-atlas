# CRLM-NMP-ATLAS independent validation audit

Run date: 2026-08-11. Official CELLxGENE H5AD export from an external published cohort (Mol Cancer 2025; DOI 10.1186/s12943-025-02430-7).

The export contains 75,104 cells from 6 donors, including 4,051 cells annotated as malignant, with all 10 `FIG1_MARKER_V1` genes present. Six donor-level CRLM-versus-adjacent-liver pairs were available for a descriptive patient-level audit.

Results are exploratory: epithelial identity mean difference was +0.105775 (5/6 positive; exact sign-flip p=0.125), plasticity anchor −0.005247 (4/6 positive; p=0.90625), and noncanonical anchor −0.001571 (2 positive, 1 negative; p=1.0; remaining donors lacked both malignant groups). This is external descriptive replication, not causal evidence, target ranking, therapeutic-window evidence or a clinical recommendation.

Full output remains local and ignored at `phase2/06_results/CRLM_NMP_ATLAS/validation.json`.
