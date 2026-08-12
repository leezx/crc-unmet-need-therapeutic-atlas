# GSE178318 QC retention report

Run date: 2026-08-11  
Command: `python3 scripts/apply_gse178318_qc.py`

The script applied the reviewed v1 rules to the locked 166,681,072-entry Matrix Market input and enforced exact sample-key and matrix checks.

| Rule | Thresholds (genes / counts) | Retained cells | Matched primary–liver patients | Sensitivity label |
|---|---:|---:|---:|---|
| permissive | 100 / 300 | 140,122 | 6 | QC_RETENTION_STABLE |
| primary | 200 / 500 | 139,543 | 6 | REFERENCE |
| stringent | 300 / 1,000 | 136,373 | 6 | QC_RETENTION_STABLE |

The permissive and stringent runs retained the same six matched patients as the primary rule, and no sample crossed the defined >20% retained-cell change threshold relative to the primary rule. The label is retention-only: paired effect direction is intentionally deferred to the patient-level state analysis and has not been used here. This result does not establish a malignant state, plasticity program, therapeutic target or clinical indication.

The full per-sample output remains local and ignored at `phase2/06_results/GSE178318/qc_retention.json`.
