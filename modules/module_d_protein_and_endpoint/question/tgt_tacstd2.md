# Module D question — `tgt_tacstd2`

Same method and data sources as `tgt_ceacam5.md`.

> **TACSTD2 has the broadest normal-tissue footprint of the five targets (Module E: 13 distinct HPA tissues with High/Medium — see `reports/TARGET_EVIDENCE_PATTERN_COMPARISON.md`) — does its tumor-tissue protein signal look strong enough to be worth pursuing despite that normal-tissue breadth?**

See `data_lock/tgt_tacstd2.md`: mixed. `PXD055821` MS detects `TACSTD2` in 71.7% of samples — the second-highest detection fraction of the five targets — but `HPA_CRC_cancer_tissue` scores 9 of 12 patients `Not detected`. A real, unreconciled cross-source disagreement, the same pattern seen for `ERBB2`. Does not resolve the normal-tissue-breadth question from Module E, which still needs real protein/surface-density evidence specifically in normal tissue (not addressed by this tumor-tissue-only pass). ADC precedent for `TACSTD2` is recorded in Module A and not restated here.
