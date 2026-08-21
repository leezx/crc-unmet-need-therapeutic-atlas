# GSE224235 independent-validation audit

Run date: 2026-08-11  
Command: `python3 scripts/audit_gse224235_validation.py`

The official processed series matrix contains 17 samples, including 8 matched colorectal-primary/liver-metastasis pairs. However, only 2 of the 10 locked Figure 1 state markers are present: `EPCAM` and `SOX2`. `KRT8`, `KRT18`, `KRT19`, `TACSTD2`, `L1CAM`, `EMP1`, `CHGA` and `KRT5` are absent.

Validation status: **INSUFFICIENT_FOR_FULL_STATE_VALIDATION**.

This dataset is retained as a documented negative gate. The partial marker overlap is not interpreted as state validation, and no target, malignancy or clinical conclusion is made. A future independent validation requires a cohort with adequate coverage of the locked marker/program set or a separately reviewed cross-platform marker contract.
