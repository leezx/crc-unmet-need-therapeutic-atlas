# Module E data lock — `tgt_f3`

Status: **LOCKED — bulk RNA; IHC genuinely absent in HPA for this gene (real source gap, not a script failure)**

Same locked inputs as `tgt_ceacam5.md`/`tgt_erbb2.md` — reused directly, not re-fetched.

## Inputs locked for this run

- **HPA RNA + IHC** — same already-downloaded, checksum-verified `rna_tissue_hpa.tsv.zip`/`normal_ihc_data.tsv.zip` as prior targets. `scripts/extract_normal_tissue_rna.py` re-verifies each file's SHA256 against the manifest before use.
- **GTEx v11 median TPM** — same external `path_env_var=GTEX_V11_MEDIAN_TPM_PATH` resource.

## What is explicitly NOT locked / NOT available

- Same registry-status caveat as prior targets: `HPA_normal_tissue`/`GTEx_normal_tissue` remain `status=CANDIDATE`.
- **`F3` has exactly one row in HPA's normal IHC data, and it carries no real information**: `Tissue=N/A`, `IHC tissue name=N/A`, `Cell type=N/A`, `Level=N/A`, `Reliability=Uncertain`. This is HPA's own real absence of scored IHC data for this gene (confirmed by reading the raw file directly, not a script bug or filtering error) — HPA has not published a usable antibody-validated IHC panel for `F3` across normal tissues. `scripts/extract_normal_tissue_rna.py` does not hard-fail on this (the row exists, it is just uninformative), so this must be called out explicitly here rather than silently treated as "0 rows scored High/Medium," which would misleadingly read as a clean negative.

## Exclusion rules

Same as prior targets for RNA (`UNCALIBRATED_PROXY`). The IHC layer that normally lowers-but-does-not-eliminate an RNA-only concern (as it did for `CEACAM5`'s lung signal) **is not available for `F3`** — this target's normal-tissue risk assessment rests on bulk RNA alone, a real, stated limitation of this pass, not a claim that IHC was checked and came back clean.
