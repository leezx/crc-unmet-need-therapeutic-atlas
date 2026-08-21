# Module F — DELIVERY_AND_CAUSALITY_LITERATURE

Core support branch, kept inside this repository for management convenience. Not solvable by a single large dataset — it is a literature-extraction contract, split into two questions that must never be merged.

## Delivery Proof

> X 能不能作为 ADC address？

Sources: existing ADC clinical literature, preclinical ADC papers (antibody, epitope, internalization kinetics, lysosomal trafficking, ADC cytotoxicity, antigen-density relation, xenograft), target-expression pathology papers, patent literature, regulatory review/label documents.

## Population Proof

> X-high population 值不值得杀？

Sources: clinical association / biomarker trials, longitudinal/resistance papers, lineage tracing / selective ablation / depletion papers.

## Hard rule

These two proofs are never collapsed into a single claim such as "X has a DepMap dependency, so it is a good ADC target." Every extracted claim keeps its lane (Delivery vs Population) and its evidence type.

## Relationship to `knowledge/`

This module extends the existing source-only evidence-object schema in `../../knowledge/README.md` (`schemas/evidence.tsv`, `schemas/indication_evidence_links.tsv`) rather than replacing it. New evidence objects here should be tagged with `delivery_proof` or `population_proof` as their evidence axis, in addition to whatever indication node they attach to.

## Cannot prove

Precedent in another cancer type ≠ precedent in mCRC. "Target internalizes" is antibody/epitope-specific, not a fixed property of the target. Patent claims are not FTO; that requires separate formal review.

## Status

Not started as a distinct extraction pipeline. `knowledge/README.md` already records 8 source-only evidence objects seeded from the architecture doc; new Module F work should add evidence objects with an explicit `delivery_proof` / `population_proof` tag rather than starting a separate store.
