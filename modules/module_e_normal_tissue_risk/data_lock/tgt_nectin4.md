# Module E data lock — `tgt_nectin4`

Status: **LOCKED — bulk RNA + cell-type-resolved IHC**

Same locked inputs as the prior three targets, reused directly.

## Inputs locked for this run

- **HPA RNA + IHC** — same already-downloaded, checksum-verified files. HPA indexes this gene under its current symbol, `NECTIN4` (`scripts/extract_normal_tissue_rna.py --gene NECTIN4` matched all 40 RNA rows and 80 IHC rows exactly — no alias needed for this source).
- **GTEx v11 median TPM** — same external `path_env_var=GTEX_V11_MEDIAN_TPM_PATH` resource, also indexed under `NECTIN4`.

## What is explicitly NOT locked / NOT available

Same as prior targets: `HPA_normal_tissue`/`GTEx_normal_tissue` remain `status=CANDIDATE`; HPA's cell-type panel is not exhaustive.

## Exclusion rules

Same as prior targets: bulk RNA `UNCALIBRATED_PROXY`, IHC `UNCALIBRATED_PROXY` (not `CALIBRATED_PROXY`, not `DIRECT`).
