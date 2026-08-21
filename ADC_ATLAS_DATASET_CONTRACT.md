# ADC Atlas dataset contract

Source: `Asset-Generation-OS-architecture.md` → `CRC-Atlas工业化重构` (2026-08-21 pivot). This is the small, fixed contract the architecture doc asked for before any further Codex download or analysis work: for every dataset, what question it is allowed to answer, what it cannot prove, and when it is allowed to be activated. It exists to stop the repository from drifting back from **target-first** to **dataset-first**.

## Repository scope (post-pivot)

> **ADC Target Repurposing Atlas**: only collect public evidence that can move an already-derisked ADC target between KILL / HOLD / SHORTLIST for refractory mCRC.

A dataset that is large, new, or scientifically interesting but does not reduce a specific target-selection uncertainty does not get a default analysis path here. See `modules/README.md` for the module breakdown and `archive/phase2_fetal_state_track_v1/ARCHIVE_NOTE.md` for what this replaces.

## Module A — external, not built in this repository

`DERISKED_TARGET_UNIVERSE` (ADCdb + clinical trials + publications + regulatory + patents) is reused, not redeveloped here. Its two source locations and its output contract are declared in `config/external_sources.yaml`, not hardcoded here — resolve each source via its `path_env_var` on whatever machine runs the pipeline. Module A's output, `ADC_TARGET_SEED_UNIVERSE.tsv`, must conform to `schemas/target_seed.tsv`, so it is a portable, machine-readable list of `target_id`s — not free text.

`schemas/target_seed.tsv` is also the admission gate for whether a target is even in scope for active repurposing search:

- `derisking_tier`: `A_CLINICAL` (ADC in human trials/approved), `B_PRECLINICAL_ADC` (preclinical ADC/antibody-internalization evidence exists), or `C_ANTIBODY_OR_BIOLOGY_ONLY` (target biology or a non-ADC antibody exists, no ADC derisking).
- `repurposing_status`: `ACTIVE`, `FUTURE`, or `EXCLUDED`. **Default rule: only `A_CLINICAL` / `B_PRECLINICAL_ADC` targets default to `ACTIVE`; `C_ANTIBODY_OR_BIOLOGY_ONLY` defaults to `FUTURE`.** A target that merely appears in ADCdb is not, by itself, grounds to run it through Modules B–F.

This repository consumes Module A output as an input list of candidate targets, keyed by `target_id`; it does not maintain its own copy of the underlying ADCdb source data.

## Modules B–F — developed and reviewed in this repository, all output keyed by `target_id`

Each module folder under `modules/` carries its own README with allowed questions and forbidden claims (summarized below). Every dataset keeps a row in `DATA/registry/datasets.tsv` (unchanged schema) plus a classification row in `DATA/registry/module_classification.tsv` — `module`, `activation_status`, `adc_decision_axis`, `activation_rule`, `activation_context`, `default_execution_order`, validated by `scripts/validate_module_classification.py` against a controlled vocabulary (additive; does not change `datasets.tsv`'s own schema or validator). `datasets.tsv`'s `priority` column (`P0_DOWNLOAD` etc.) is legacy Phase 1 download-priority metadata only — `module_classification.tsv` is canonical for what to analyze, when, and under what rule; see `CONTRIBUTING.md`. `activation_context` (`ANY`, `RAS_MUTANT`, `RAS_WT`, `ANTI_EGFR_REFRACTORY`, `MRD_RECURRENCE`, `FIRST_LINE_VALIDATION`) names the actual molecular/clinical territory a `context_specific` activation applies to, instead of leaving it in free-text `reason`.

**Two-table evidence model, single source of truth per finding:**

- `schemas/evidence.tsv` (+ `schemas/indication_evidence_links.tsv`) stays the **source/provenance object** layer: what a dataset's registry metadata plausibly indexes, `SOURCE_INDEXED_NOT_ANALYZED` until reviewed. It now also carries `target_id`, but it is not where a Module B–F finding gets recorded.
- `schemas/target_evidence.tsv` is the **canonical, target-level interpreted output** of Modules B–F. Every concrete finding — a prevalence call, a persistence direction, a protein-concordance result, a normal-tissue flag, a delivery/population-proof claim — is a row here, not a gene name mentioned in report prose. Two fields specifically stop evidence from being silently merged or upgraded across territories or measurement types:
  - `indication_id`: which defined mCRC population/territory (e.g. `mcrc_preop_chemotherapy_crlm`, an anti-EGFR-refractory node, a RAS-mutant node) this finding applies to. A target's dossier is `target_id x indication_id`, never a bare `target_id` — the same target can be SHORTLIST in one territory and HOLD in another.
  - `evidence_directness`: `DIRECT`, `CALIBRATED_PROXY`, `UNCALIBRATED_PROXY`, or `UNKNOWN`. RNA, whole-tissue protein, IHC, surfaceome-capture, and a real quantitative surface-density assay are different measurement layers (`measurement_layer` column) with different directness — never distinguishable only by reading the `claim` text.
  - A `target_evidence.tsv` row may point back to its raw source object via `source_evidence_id` (nullable) when one exists in `evidence.tsv`.

| Module | Question it answers | Primary inputs | Cannot prove |
| --- | --- | --- | --- |
| B — `MCRC_TARGET_PREVALENCE` | 是否有足够多能被 X 地址访问的 mCRC 癌细胞？(malignant-cell detection, X-high fraction, patient-positive fraction, between/within-patient heterogeneity) | GSE225857, GSE178318, refractory/clinical bulk datasets | Output must stay `RNA_no/RNA_low/RNA_high`. This can **never** be upgraded to a `surface-density high` claim by Module D calibration alone — Module D only provides protein-level support/concordance (whole-tissue MS ≠ malignant-cell membrane density, PDO protein ≠ tumor surface density); a surface-density claim requires a target-specific quantitative surface assay or equivalent direct evidence. |
| C — `REFRACTORY_PERSISTENCE` | X 到了真正的 2/3L refractory patient 身上还剩多少？(post-treatment persistence, acquired-resistance direction, primary→metastasis / CRLM / recurrent-lesion retention) | GSE274551, GSE84267, GSE178318, GSE225857, target-specific clinical literature | Enrichment in a small paired cohort ≠ causal population-level claim (GSE84267 n=2). A first-line/pretreatment response-association cohort (`clinical_endpoint_context` axis: GSE196576, GSE235919, GSE5851) is **not** evidence of post-treatment persistence (`persistence` axis: GSE178318, GSE225857, GSE84267, GSE294385) — the two axes are validated as distinct in `module_classification.tsv`, never merged. |
| D — `PROTEIN_AND_ENDPOINT` | 把"漂亮的 RNA target"砍掉一大批：tumor protein evidence, RNA↔protein concordance, recurrence/PFS/OS association | PXD055821, PXD022613, mCRC PDO 2026 (`MCRC_liver_metastasis_PDO_2026`), HPA/CPTAC support | Whole-tissue MS ≠ malignant-cell-specific membrane density; association ≠ "killing X-high cells prevents recurrence". Module D output is protein-level support, never a Module B surface-density upgrade (see Module B row above). |
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
