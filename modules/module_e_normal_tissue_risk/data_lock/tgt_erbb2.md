# Module E data lock — `tgt_erbb2`

Status: **LOCKED — bulk RNA + cell-type-resolved IHC**

Same locked inputs as `tgt_ceacam5.md` (this repository's own already-verified local cache + one external `path_env_var` source) — reused directly, not re-fetched:

## Inputs locked for this run

- **HPA RNA + IHC** — `DATA/registry/HPA_normal_tissue/source_manifest.tsv`'s already-downloaded, checksum-verified `rna_tissue_hpa.tsv.zip` (HPA's "RNA expression (HPA)" product, 40 tissues) and `normal_ihc_data.tsv.zip` (cell-type-resolved normal-tissue IHC). `scripts/extract_normal_tissue_rna.py` re-verifies each file's SHA256 against the manifest before use — hard fail on mismatch.
- **GTEx v11 median TPM** — external, resolved via `config/external_sources.yaml`'s `module_e_gtex_bulk_rna_reference` block (fail-closed `path_env_var=GTEX_V11_MEDIAN_TPM_PATH`), same reused `DATA/1.Databases/GTEx_v11_median_tpm` entry as `tgt_ceacam5`.

## What is explicitly NOT locked / NOT available

- `HPA_normal_tissue` and `GTEx_normal_tissue` remain `status=CANDIDATE` in `DATA/registry/datasets.tsv` — unchanged by this run.
- HPA's ~76 annotated cell types cover many tissues but not every conceivable cell population; a Low/Not-detected IHC result means "nothing scored High/Medium in the cell types HPA tested," not an exhaustive negative.

## Exclusion rules

Same as `tgt_ceacam5.md`: bulk RNA (`UNCALIBRATED_PROXY`) cannot separate accessible surface-positive cells from background; cell-type IHC is closer to real biology but is not itself a calibration step (`UNCALIBRATED_PROXY`, not `CALIBRATED_PROXY`, not `DIRECT`); GTEx subregion columns are read individually, not averaged away.
