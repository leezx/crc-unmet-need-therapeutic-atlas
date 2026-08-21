# HTAN CRC progressive-plasticity source-cohort replication audit

Run date: 2026-08-11  
Input: official CELLxGENE epithelial H5AD, collection `1cbfb478-2c7f-4d15-b522-9f74e9fe52a8`, asset `81bd8922-b69a-45ea-9b2a-032c480c0e37.h5ad`.

The H5AD contains 47,107 epithelial cells from 29 patients and 25 patients with both Primary and Metastasis sample types. All 10 locked Figure 1 markers are present. Patient-level aggregation of the same marker scores produced:

| Program | Mean metastasis − primary | Positive pairs | Negative pairs | Exact two-sided sign-flip p |
|---|---:|---:|---:|---:|
| epithelial identity | -0.16748 | 11 | 14 | 0.17706 |
| plasticity anchor | 0.08382 | 18 | 7 | 0.01302 |
| noncanonical anchor | 0.02137 | 10 | 12 | 0.16645 |

This H5AD is derived from the same progressive-plasticity study that motivated the marker contract, so it is not an independent validation cohort. The plasticity-anchor direction is concordant in 18/25 matched pairs as a source-cohort replication/audit only. It cannot increase the independent-validation completion score. Cell-cycle and stress scores are reported separately and excluded from state scores. The full result remains local and ignored at `phase2/06_results/HTAN_CRC_progressive_plasticity/validation.json`.
