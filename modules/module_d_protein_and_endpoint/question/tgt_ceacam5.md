# Module D question — `tgt_ceacam5`

First real target run through Module D (2026-08-25), all five `A_CLINICAL` targets run together (same two data sources, same method per target).

> **CEACAM5's RNA signal (Module B: broad detection across two independent CRLM cohorts; Module E: strong GI-tissue-concentrated bulk RNA) — does independent protein-level evidence corroborate it, or does it fall apart at the protein layer?**

Not asking for a surface-density number — neither `PXD055821` (whole-tissue mass spec) nor `HPA_CRC_cancer_tissue` (whole-tumor-section IHC) can establish that. Asking the narrower, real question this repository's own Module D contract exists to answer: does the RNA-based case for this target survive contact with a genuinely different measurement type, or was it an RNA-layer artifact?

See `data_lock/tgt_ceacam5.md` and `analysis_contracts/pxd055821_protein_abundance.md`/`analysis_contracts/hpa_cancer_ihc.md` for the real, checksummed result: yes, on both counts — `CEACAM5` is detected in 100% of `PXD055821`'s MS samples and is the only target with any `High` HPA cancer-IHC calls. This corroborates, and does not by itself confirm, the RNA-based case; ADC precedent for `CEACAM5` is recorded in Module A (`DATA/registry/ADC_TARGET_SEED_UNIVERSE.tsv`) and not restated here.
