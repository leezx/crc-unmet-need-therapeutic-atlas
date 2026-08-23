# Module E data lock — `tgt_ceacam5`

Status: **LOCKED — bulk RNA + cell-type-resolved IHC**

Revised 2026-08-23 (PR #73 round 1 review) after web-ChatGPT caught that the first version of this file both mislabeled its HPA RNA source and, more importantly, wrongly said IHC was unavailable when this repository's own `HPA_normal_tissue/source_manifest.tsv` already records it as downloaded.

## Inputs locked for this run

- **HPA RNA + IHC — both from this repository's own tracked local cache, not an external `path_env_var` resource.** `DATA/registry/HPA_normal_tissue/source_manifest.tsv` records `rna_tissue_hpa.tsv.zip` and `normal_ihc_data.tsv.zip` as downloaded 2026-08-11 with SHA256 checksums; both files are physically present (gitignored, never deleted) at `archive/phase2_fetal_state_track_v1/phase2/03_data/raw/HPA_normal_tissue/`. `scripts/extract_normal_tissue_rna.py` reads that fixed repo-relative path directly and re-verifies each file's SHA256 against the manifest before use — hard fail on missing file or checksum mismatch.
  - `rna_tissue_hpa.tsv.zip` is HPA's **"RNA expression (HPA)"** product (40 tissues) — **not** the separate 51-tissue **"RNA expression (consensus)"** product (these are two distinct official HPA downloads; the first version of this data lock called it "consensus" in error).
  - `normal_ihc_data.tsv.zip` is HPA's cell-type-resolved normal-tissue IHC data (Gene / Tissue / IHC tissue name / Cell type / Level / Reliability).
- **GTEx v11 median TPM — genuinely external**, resolved via `config/external_sources.yaml`'s `module_e_gtex_bulk_rna_reference` block (fail-closed `path_env_var`, `GTEX_V11_MEDIAN_TPM_PATH`). Reused from a separate project's `DATA/1.Databases/GTEx_v11_median_tpm` entry — this repository does not download or store it. `DATA/registry/GTEx_normal_tissue/source_manifest.tsv` backfilled 2026-08-23 with the exact file/checksum this run used.

## What is explicitly NOT locked / NOT available

- `HPA_normal_tissue` and `GTEx_normal_tissue` both remain `status=CANDIDATE` in `DATA/registry/datasets.tsv` — this run does not change that. Reading an already-fetched local file for a real analysis is not the same as promoting a candidate to `APPROVED`.
- The ~76 HPA-annotated cell types cover many tissues but not every conceivable cell population; a Low/Not-detected IHC result is read as "nothing scored High/Medium in the cell types HPA tested," not as an exhaustive negative.

## Exclusion rules

- Bulk tissue RNA (HPA "RNA expression (HPA)", GTEx) cannot separate a genuinely accessible, cell-surface-positive population from background/stromal/rare-cell contribution — `evidence_directness=UNCALIBRATED_PROXY` for both.
- Cell-type IHC is closer to real biology but is still not a quantitative surface-density assay — `evidence_directness=CALIBRATED_PROXY`, not `DIRECT`. IHC intensity != accessible antigen density.
- GTEx subregion columns (e.g. `Colon_Transverse_Mucosa` vs `Colon_Transverse_Muscularis`) are treated as informative, not averaged away.
