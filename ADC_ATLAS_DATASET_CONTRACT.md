# ADC Atlas dataset contract

Source: `Asset-Generation-OS-architecture.md` → `CRC-Atlas工业化重构` (2026-08-21 pivot). This is the small, fixed contract the architecture doc asked for before any further Codex download or analysis work: for every dataset, what question it is allowed to answer, what it cannot prove, and when it is allowed to be activated. It exists to stop the repository from drifting back from **target-first** to **dataset-first**.

## Repository scope (post-pivot)

> **ADC Target Repurposing Atlas**: only collect public evidence that can move an already-derisked ADC target between KILL / HOLD / SHORTLIST for refractory mCRC.

A dataset that is large, new, or scientifically interesting but does not reduce a specific target-selection uncertainty does not get a default analysis path here. See `modules/README.md` for the module breakdown and `archive/phase2_fetal_state_track_v1/ARCHIVE_NOTE.md` for what this replaces.

## Module A — external, not built in this repository

`DERISKED_TARGET_UNIVERSE` (ADCdb + clinical trials + publications + regulatory + patents) is reused, not redeveloped here. Its two source locations and its output contract are declared in `config/external_sources.yaml`, not hardcoded here — resolve each source via its `path_env_var` on whatever machine runs the pipeline. Module A's output, `ADC_TARGET_SEED_UNIVERSE.tsv`, must conform to `schemas/target_seed.tsv`, so it is a portable, machine-readable list of `target_id`s — not free text.

This repository consumes Module A output as an input list of candidate targets, keyed by `target_id`; it does not maintain its own copy of the underlying ADCdb source data.

## Modules B–F — developed and reviewed in this repository, all output keyed by `target_id`

Each module folder under `modules/` carries its own README with allowed questions and forbidden claims (summarized below). Every dataset keeps a row in `DATA/registry/datasets.tsv` (unchanged schema) plus a classification row in `DATA/registry/module_classification.tsv` — `module`, `activation_status`, `adc_decision_axis`, `activation_rule`, `default_execution_order`, validated by `scripts/validate_module_classification.py` against a controlled vocabulary (additive; does not change `datasets.tsv`'s own schema or validator). `datasets.tsv`'s `priority` column (`P0_DOWNLOAD` etc.) is legacy Phase 1 download-priority metadata only — `module_classification.tsv` is canonical for what to analyze, when, and under what rule; see `CONTRIBUTING.md`.

Every concrete finding a module produces — a prevalence call, a persistence direction, a protein-concordance result, a normal-tissue flag, a delivery/population-proof claim — must be a row keyed by `target_id` in `schemas/target_evidence.tsv` (or the existing `schemas/evidence.tsv` / `schemas/indication_evidence_links.tsv`, which now also carry `target_id`). A claim that only exists as a gene name inside prose does not count as retrievable evidence.

| Module | Question it answers | Primary inputs | Cannot prove |
| --- | --- | --- | --- |
| B — `MCRC_TARGET_PREVALENCE` | 是否有足够多能被 X 地址访问的 mCRC 癌细胞？(malignant-cell detection, X-high fraction, patient-positive fraction, between/within-patient heterogeneity) | GSE225857, GSE178318, refractory/clinical bulk datasets | Output must stay `RNA_no/RNA_low/RNA_high`, never `surface-density high` before protein calibration. |
| C — `REFRACTORY_PERSISTENCE` | X 到了真正的 2/3L refractory patient 身上还剩多少？(post-treatment persistence, acquired-resistance direction, primary→metastasis / CRLM / recurrent-lesion retention) | GSE274551, GSE84267, GSE178318, GSE225857, target-specific clinical literature | Enrichment in a small paired cohort ≠ causal population-level claim (GSE84267 n=2). |
| D — `PROTEIN_AND_ENDPOINT` | 把"漂亮的 RNA target"砍掉一大批：tumor protein evidence, RNA↔protein concordance, recurrence/PFS/OS association | PXD055821, PXD022613, mCRC PDO 2026 (`MCRC_liver_metastasis_PDO_2026`), HPA/CPTAC support | Whole-tissue MS ≠ malignant-cell-specific membrane density; association ≠ "killing X-high cells prevents recurrence". |
| E — `NORMAL_TISSUE_RISK` | 明显不值得继续的正常组织 liability（不是一个安全分数） | HPA normal IHC / cell-type protein + MS (`HPA_normal_tissue`); GTEx / normal scRNA as support | HPA-negative ≠ safe; IHC intensity ≠ accessible antigen density; never conclude a therapeutic window from this module alone. |
| F — `DELIVERY_AND_CAUSALITY_LITERATURE` | Delivery Proof (can X be an ADC address?) and Population Proof (is X-high population worth killing?) — kept as two separate questions | Existing ADC / antibody internalization / epitope / trafficking literature; clinical association, longitudinal enrichment, lineage tracing, selective ablation literature | Never merge Delivery Proof and Population Proof into "X has a DepMap dependency, so it is a good ADC target." |

## Two unknowns this Atlas is not allowed to pretend it has solved

1. **Real membrane antigen density (molecules/cell).** RNA → tumor protein → IHC → surfaceome precedent is the ceiling of what public data gives; it stays `UNKNOWN` per candidate unless a dedicated quantitative assay exists.
2. **Selective X-high population depletion → clinical endpoint rescue.** Public data can only approach `association → longitudinal selection → phenotype → causal-adjacent literature`; it may not be filled in as `PASS` without a target-specific depletion/ADC experiment.

Exposing these two as explicit `UNKNOWN` outputs is a correct result of this Atlas, not a gap to paper over.

## Frozen by default (`SUPPLEMENT_FROZEN`)

DepMap, Perturb-seq, HTAN plasticity, GSE117548, generic primary CRC scRNA, generic spatial, and NMF/fetal-state cell-state discovery are not on a default analysis path (`module = NONE`, `activation_rule = never_default` or `after_shortlist_named_uncertainty`). They activate only when a target has already reached shortlist and a specific question needs them (example: "why are X-high models sensitive to TOP1 payload?" → activate DepMap for that target only). See `DATA/registry/module_classification.tsv` for the per-dataset disposition and reason, and run `python3 scripts/validate_module_classification.py` to check it stays internally consistent and fully cross-referenced against `datasets.tsv`.

## Governance

Adding or reclassifying a dataset here follows the same review workflow as everywhere else in this repository — see `CONTRIBUTING.md`. New candidate rows stay `CANDIDATE` with `UNKNOWN` fields until source-verified; this contract does not by itself authorize a download.
