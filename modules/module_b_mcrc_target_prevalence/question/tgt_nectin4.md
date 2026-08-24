# Module B question — `tgt_nectin4`

Paired with the Module E run for the same target (`../../module_e_normal_tissue_risk/question/tgt_nectin4.md`). Same `indication_id=mcrc_preop_chemotherapy_crlm` territory and dataset pair as the prior three targets.

> **在 `mcrc_preop_chemotherapy_crlm` 这个 indication 里，NECTIN4 是否有足够多能被地址访问的恶性上皮细胞？**

## Status: `GSE178318` has an epithelial-proxy answer — the malignant-cell question itself is still open

Same method as prior targets (`data_lock/tgt_nectin4.md`, `analysis_contracts/tgt_nectin4.md`): QC-filtered, EPCAM-based epithelial-proxy screen, **not malignancy-confirmed**, no CNV-based confirmation attempt for this target in this pass. `TE020` (3 treated patients) and `TE021` (3 treatment-naive patients, context evidence) are the real, QC-filtered result. `GSE225857`'s CNSA raw-sequencing route was blocked at the time this question was first posed; it has since produced its own real result via GEO's public route -- see `TE030` (2026-08-24, PR #81).

**Gene-symbol note**: `GSE178318`'s own gene index (`archive/.../GSE178318_genes.tsv.gz`) does not contain a `NECTIN4` row — the identical Ensembl gene, `ENSG00000143217`, is indexed there under `NECTIN4`'s prior HGNC symbol, `PVRL4` (confirmed by direct lookup of the Ensembl ID, not assumed). `scripts/annotate_gse178318_cell_types.py --gene PVRL4` was run to resolve this correctly; every downstream artifact (this file, `data_lock`, `analysis_contracts`, `target_evidence.tsv`) reports the result under the canonical symbol `NECTIN4`, with this alias resolution stated explicitly wherever the raw script invocation is cited, so a future agent re-running this does not silently get an empty result from `--gene NECTIN4` against this one dataset.
