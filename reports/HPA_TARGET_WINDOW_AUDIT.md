# HPA normal-tissue target-window audit

Run date: 2026-08-11  
Inputs: HPA v25.1 `rna_tissue_hpa.tsv.zip` and `normal_ihc_data.tsv.zip`.

The audit covers `TACSTD2`, `L1CAM`, `EMP1`, `SOX2`, `CHGA` and `KRT5`. It reports normal-tissue RNA nTPM coverage and protein IHC levels, but does not convert expression into a therapeutic window or safety conclusion. A real target decision still requires surface localization, tumor-versus-normal quantitative modeling, antibody/ADC feasibility and functional dependency evidence.

Full output remains local and ignored at `phase2/06_results/HPA_normal_tissue/target_window_audit.json`.
