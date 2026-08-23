# Module E data lock — `tgt_ceacam5`

Status: **LOCKED — bulk RNA only**

## Inputs locked for this run

Both resolved via `config/external_sources.yaml`'s `module_e_normal_tissue_bulk_rna_reference` block (fail-closed `path_env_var`, see `scripts/extract_normal_tissue_rna.py`). Neither is a new download — both are already-fetched, checksum-verified local copies of official public resources (see each dataset's own `DATA/1.Databases/<id>/link.md` on the machine that ran this).

- `hpa_rna_tissue_consensus` — HPA RNA tissue consensus, `rna_tissue_hpa.tsv` (long-format gene x tissue nTPM), 40 tissues. Official source: `proteinatlas.org` bulk downloads. MD5 `46b45e4a437884f477749838c712851d` (per that dataset's own `link.md`), originally accessed 2025-11-05.
- `gtex_v11_median_tpm` — GTEx v11 adult gene-level median TPM by tissue, 68 tissues. Official source: GTEx Portal / `storage.googleapis.com/adult-gtex`, GCT format. Accessed 2026-08-13.

## What is explicitly NOT locked / NOT available

- The full `HPA_normal_tissue` registry entry (`DATA/registry/HPA_normal_tissue/`) also covers IHC images and ~76 annotated cell types per Module E's README — **none of that is available locally in this run**, only the RNA-consensus subset. Do not read this run's output as an IHC or cell-type-resolved result.
- `HPA_normal_tissue` and `GTEx_normal_tissue` both remain `status=CANDIDATE` in `DATA/registry/datasets.tsv` — this run does not change that, and does not constitute "APPROVED" for either dataset. It is a read of already-present files for a real analysis, not a new bulk download requiring the Phase 1 download-approval gate.

## Exclusion rules

- Bulk tissue RNA cannot separate a genuinely accessible, cell-surface-positive population from background/stromal/rare-cell contribution within that tissue sample. A high value flags "worth a closer look," not "unsafe"; a low value is not "safe" — see `../README.md`'s "Cannot prove."
- GTEx subregion columns (e.g. `Colon_Transverse_Mucosa` vs `Colon_Transverse_Muscularis`) are treated as informative, not averaged away — see `analysis_contracts/tgt_ceacam5.md`.
