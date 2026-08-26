# Module B — real gene-window InferCNV for `GSE178318`'s epithelial-proxy cells

**Status: LOCKED. Materially different result from the arm-level CNV-lite attempt — real, but still expression-based, not DNA-level. Revised in round 1 review of PR #89 (a real mitochondrial-chromosome bug fixed and fully re-run; population identity now verified by direct cell-set comparison, not just population counts; `infercnvpy`'s evidentiary status corrected; a block-coherence sanity check and a leave-`CEACAM5`-out sensitivity control added).**

Written for Next-handoff item 1: `infercnv_lite_gse178318.md`'s own "Explicit limitations" section named the coarse arm-level method's two biggest gaps relative to a real InferCNV-style workflow — no gene-order local structure (a moving window along genes in true genomic order) and no explicit centering/reference-subtraction step. This file's method addresses both directly, using `infercnvpy` — a maintained, `inferCNV`-inspired Python reimplementation, confirmed pip-installable and network-reachable in this environment 2026-08-26.

## What `infercnvpy` is, precisely (corrected in round 1 review of PR #89)

An earlier version of this file described `infercnvpy` as a "real, actively-maintained scanpy-ecosystem reimplementation of the Broad Institute's `inferCNV` algorithm" and "the field-standard approach" — this overstated its evidentiary status. `infercnvpy`'s own documentation states it is "heavily inspired by" Broad `inferCNV` but is a separate, more computationally efficient implementation, and that it is **still experimental — results have not been formally validated, except that they look similar, but not identical, to `inferCNV`**. Broad `inferCNV` itself is the mature, widely-used method; `infercnvpy` is a maintained, `inferCNV`-inspired Python implementation with its own explicitly-stated experimental status, not a validated equivalent. This does not mean the analysis below shouldn't be run — it means it is appropriate as a **screening-level** result, not evidence of a formally-validated method's output, and this distinction is why the sanity checks in this file's Results section (not merely disclosed limitations) are what actually determine whether this row's confidence tier is defensible, not the identity of the software package alone.

## What this is and is not

This is expression-based CNV *inference* — a moving-window average of reference-centered log expression across genes in genomic order — not a DNA-level (WGS/WES/array) copy-number call. This is an independent run against this repository's own reference-population choice, not a reproduction of `GSE178318`'s own publication's exact numbers, thresholds, or reference set (not disclosed in the Methods excerpt available to this analysis). `evidence_directness` stays `UNCALIBRATED_PROXY` — an expression-based CNV score is still an indirect readout of malignancy, not malignancy itself, and not a surface/membrane density claim.

## Method (locked before running results were known — population definitions, split seed, and package defaults chosen first)

1. **Population definitions reused byte-for-byte from `infercnv_lite_gse178318.py`'s own `build_populations()`** (imported directly, not reimplemented): reference = QC-passing, `immune`-classified, tumor-site (`PRIMARY_CRC`/`LIVER_METASTASIS`, never `PBMC`), treated-cohort-only (`COL15`/`COL17`/`COL18`) cells; epithelial-proxy = the same restriction with `epithelial`-classified cells.
2. **QC/classification statistics computed by vectorized sparse-matrix reductions**, not `annotate_gse178318_cell_types.py`'s own streaming per-line loop. **Population identity is now directly verified, not just population counts** (round 1 review of PR #89: an earlier version only checked that the vectorized and streaming methods produced the same *sizes* — 38,003/1,786 both ways — which does not prove the same *cell sets*; two different index sets could coincidentally share a cardinality). `scripts/infercnv_gse178318.py` now runs an independent, literal streaming re-implementation of `annotate_gse178318_cell_types.py`'s own QC/classification block (`compute_qc_and_categories_streaming()`/`verify_populations()`) on every invocation and fails closed unless `set(streaming_reference_idx) == set(vectorized_reference_idx)` and the same for epithelial-proxy — **confirmed MATCH on both sets** in the run this file reports.
3. **Reference/epithelial-proxy fit-holdout split**: same seed (`--seed 42`, matching `infercnv_lite_gse178318.py`'s own default) and same 50/50 `random.shuffle` split of the reference population into fit/holdout halves, for direct methodological comparability with the arm-level attempt.
4. **Gene genomic positions**: `DATA/reference/ensembl_gene_positions_grch38_release110.tsv`. 32,807/33,694 (97.4%) of `GSE178318`'s own genes resolve to a position.
5. **Preprocessing**: standard `scanpy` library-size normalization (`sc.pp.normalize_total(target_sum=1e4)`) + `sc.pp.log1p()` on raw UMI counts before CNV inference.
6. **Reference vector**: mean of the normalized/log1p expression across the **fit half of the reference population only**, passed directly to `infercnvpy` via its `reference=` parameter.
7. **`infercnvpy.tl.infercnv()` called with the package's own defaults, not tuned**: `window_size=100` genes, `step=10`, `lfc_clip=3`, `dynamic_threshold=1.5`, `exclude_chromosomes=('chrX','chrY')`.
8. **Chromosome-label mapping, corrected in round 1 review of PR #89**: Ensembl's own chromosome field for the mitochondrial genome is `"MT"`; an earlier version of this script mapped it to `"chrMT"` via a uniform `f"chr{c}"` rule. `infercnvpy`'s own windowing code explicitly skips the mitochondrial contig, but only by the literal string `"chrM"` (`infercnvpy/tl/_infercnv.py`: `x != "chrM"`) — it does not recognize `"chrMT"`. This meant mitochondrial genes were **silently included** in the CNV-window computation in the round-0 run this file originally reported (the 22.79x/407-cell numbers) — mitochondrial RNA expression is a cell-state/QC/metabolism signal, not the nuclear-genome copy-number alteration this analysis is trying to infer. Fixed (`"MT"` now maps to `"chrM"` specifically) and the entire analysis re-run from scratch — every number in this file's Results section is from the corrected, post-fix run; none of the round-0 numbers are carried over or assumed unchanged.
9. **Per-cell CNV score**: `mean(|X_cnv[cell, :]|)` across all smoothed genomic windows for that cell.
10. **`CNV_HIGH`/`CNV_LOW` threshold**: the held-out reference half's own 99th percentile of this per-cell score. **This ratio is a descriptive tail-enrichment statistic, not an independent validation statistic** (round 1 review of PR #89) — the reference's own ~1% exceedance rate at this threshold is true by construction (the threshold is defined as that same half's own 99th percentile), so the enrichment ratio should not, on its own, be used as justification for raising confidence; it is reported as a real, useful descriptive number, alongside (not instead of) the sanity checks below.
11. **Block-coherence sanity check (new, round 1 review of PR #89)**: for each of `CNV_HIGH`-epithelial, `CNV_LOW`-epithelial, and reference-holdout groups, compute the group-mean CNV profile across all smoothed genomic windows, then what fraction of that profile's total `|signal|` is carried by its own top 5% of windows (by magnitude). A perfectly uniform/diffuse profile concentrates ~5% of its own signal in its own top 5% of windows; a profile with a real, focal, block-structured pattern concentrates substantially more. This directly addresses the core question the reviewer raised: does `CNV_HIGH`'s signal look like a genuine, spatially-coherent copy-number pattern, or like a diffuse expression-lineage difference inflating a global aggregate?
12. **Leave-`CEACAM5`-out sensitivity control (new, round 1 review of PR #89)**: `CEACAM5` itself is one of the 32,807 genes fed into the CNV-window computation, so a claim like "`CEACAM5`-positive fraction differs by `CNV_HIGH`/`CNV_LOW`" carries a real, checkable target-leakage risk. Re-ran the entire pipeline with `CEACAM5` excluded from the CNV-inference input (its raw counts are still used as the positivity readout, sourced directly from the raw matrix, never from the modified InferCNV input) and compared the resulting `CNV_HIGH` cell set against the main run's.
13. **Output**: `CEACAM5`-positive fraction recomputed within `CNV_HIGH` epithelial-proxy cells, per sample, for the 3 treated patients.

## Explicit limitations (locked before running)

- **Expression-based, not DNA-level.** A cell scoring `CNV_HIGH` here is malignancy-*consistent*, not malignancy-*confirmed* at the DNA level.
- **`infercnvpy` is explicitly experimental per its own documentation** (see above) — not a formally-validated equivalent of Broad `inferCNV`, appropriate for screening-level use, not for a confidence upgrade based on "using a peer-established package" reasoning alone.
- **Reference genome release mismatch (undisclosed)**: `GSE178318`'s own CellRanger reference release is not stated in its available metadata.
- **Package defaults, not dataset-tuned or independently validated here.**
- **Lineage confounding is reduced, not eliminated** — see the block-coherence Results below for what this analysis actually found on this question, not just the abstract limitation.
- **Not a reproduction of `GSE178318`'s own published InferCNV result.**

## Results (2026-08-26, corrected/re-run in round 1 review of PR #89)

Run via `python3 scripts/infercnv_gse178318.py --gene CEACAM5`. Full table: `results/tgt_ceacam5_infercnv_attempt.tsv` (gitignored, not committed — regenerable). Runtime: ~3m20s on this environment (17 GB RAM / 8 CPU) for the main run, the leave-`CEACAM5`-out control run, and the independent streaming population-verification pass combined.

**Population identity, verified by direct cell-set comparison**: `set(streaming_reference_idx) == set(vectorized_reference_idx)` → **MATCH** (both n=38,003); `set(streaming_epithelial_idx) == set(vectorized_epithelial_idx)` → **MATCH** (both n=1,786). The only variable between this file and the arm-level attempt is confirmed to be the CNV-inference algorithm itself, not a silently different cell-selection pipeline.

- **Fit-half reference CNV score median: 0.00698.**
- **Held-out reference CNV score (n=19,002)**: median=0.00700, p90=0.00918, p99=0.01183 (**threshold=0.01183**).
- **Epithelial-proxy CNV score (n=1,786)**: min=0.00160, p10=0.00559, p25=0.00683, **median=0.00863**, p75=0.01131, p90=0.01389, p99=0.01849, max=0.05494.
- **`CNV_HIGH` (score > threshold): epithelial-proxy 391/1,786 (21.89%) vs. held-out reference's own 190/19,002 (1.00%) — descriptive tail-enrichment ratio 21.89x** (post-`chrM`-fix; the round-0 pre-fix number was 22.79x/407 cells — close, but not identical, confirming the mitochondrial-gene bug had a real, non-negligible effect and must not be assumed immaterial).
- **Per-sample `CNV_HIGH` counts and `CEACAM5`-positive fractions**:

| Sample | n epithelial-proxy | n `CNV_HIGH` | `CEACAM5`-pos frac. in `CNV_HIGH` | n `CNV_LOW` | `CEACAM5`-pos frac. in `CNV_LOW` |
|---|---:|---:|---:|---:|---:|
| `COL15` CRC | 378 | 102 | 0.7353 | 276 | 0.5435 |
| `COL15` LM | 841 | 206 | 0.6456 | 635 | 0.2315 |
| `COL17` CRC | 50 | 5 | 0.6000 | 45 | 0.1556 |
| `COL17` LM | 25 | 1 | 1.0000 | 24 | 0.0833 |
| `COL18` CRC | 132 | 22 | 0.7727 | 110 | 0.2727 |
| `COL18` LM | 360 | 55 | 0.7455 | 305 | 0.1377 |

`CEACAM5`-positive fraction is still higher in `CNV_HIGH` than `CNV_LOW` cells in every one of the 6 sample strata — the direction and approximate magnitude of the round-0 finding survive the `chrM` fix, though the exact numbers changed (as they must be assumed to, not just similar-looking).

### Block-coherence sanity check (new)

| Group | n cells | Top-5%-of-windows share of total `|`mean profile`|` | Top chromosomes in that top 5% |
|---|---:|---:|---|
| `CNV_HIGH` epithelial | 391 | **0.313** | `chr20` (36 windows), `chr7` (34), `chr6` (14), `chr8` (11), `chr17` (10) |
| `CNV_LOW` epithelial | 1,395 | 0.267 | `chr7` (33), `chr20` (25), `chr6` (18), `chr19` (12), `chr8` (12) |
| reference (held-out) | 19,002 | 0.093 | `chr1` (27), `chr4` (13), `chr6` (13), `chr7` (12), `chr3` (12) |

A perfectly uniform/diffuse profile would show ~0.05 concentration in its own top 5% of windows. Both epithelial groups (`CNV_HIGH` and `CNV_LOW`) show real concentration well above that (0.313 and 0.267) — substantially more focal than the reference population's own profile (0.093, close to uniform). `CNV_HIGH`'s top chromosomes (`chr20`, `chr7`) are independently confirmed, real, well-documented recurrent copy-number gain hotspots in colorectal cancer (independently fetched: The Cancer Genome Atlas Network, "Comprehensive molecular characterization of human colon and rectal cancer," *Nature* 2012, PMID 22810696, PMC3401966 — states verbatim: "There were several previously well-defined arm-level changes, including gains of 1q, 7p and q, 8p and q, 12q, 13q, 19q, and 20p and q," with a specific 20q13.12 amplification peak near *HNF4A*) — a genuine, checkable plausibility signal, not proof, that `CNV_HIGH`'s concentrated signal reflects real, biologically-expected CRC copy-number architecture rather than an arbitrary, dataset-specific artifact. This is a real, positive finding for the block-coherence question the reviewer raised — but it is a descriptive observation, not a formal statistical test, and `CNV_LOW` epithelial cells also show real (smaller) concentration on the same chromosomes, so this does not sharply, categorically separate `CNV_HIGH` from `CNV_LOW` — it is evidence of degree, not of a clean binary distinction.

### Leave-`CEACAM5`-out sensitivity control (new)

Re-running the entire pipeline with `CEACAM5` excluded from the 32,806-gene CNV-inference input (`CEACAM5`'s own raw counts still used as the positivity readout) gives: `CNV_HIGH` epithelial-proxy count = 394 (main run: 391); **Jaccard overlap of the two runs' `CNV_HIGH` cell sets = 0.992** (99.2% of the two runs' `CNV_HIGH` cells are the identical cells). `CEACAM5`-positive fractions per sample in the control run are effectively unchanged from the main run (e.g., `COL15` CRC 0.7353 vs. 0.7353 main; `COL15` LM 0.6411 vs. 0.6456 main). **This rules out target leakage as a material driver of this row's finding** — `CEACAM5`'s own inclusion in the CNV-inference input has a negligible effect on which cells are called `CNV_HIGH`.

## Interpretation, and the evidence-tier decision this file's own checks support

Both requested sanity checks were run and both are consistent with (not proof of) a real signal: the block-coherence check shows `CNV_HIGH`'s profile is substantially more spatially concentrated than the reference's, on chromosomes independently confirmed as recurrent CRC CNA hotspots; the leave-`CEACAM5`-out control rules out target leakage as a material confound. Combined with the corrected `chrM` handling and the now-directly-verified population identity, this supports treating `TE043` at `evidence_level=SCREENING_LEVEL`/`confidence=MEDIUM` (an upgrade from the arm-level attempt's `EXPLORATORY_UNDERPOWERED`/`LOW`) — but this remains an expression-based, `infercnvpy`-specific (explicitly experimental per its own docs) inference, not a DNA-level malignancy confirmation, and the block-coherence check is descriptive, not a formal spatial-statistics test. Module B's malignant-cell prevalence question for `tgt_ceacam5` is materially advanced by this result but not fully closed by it.
