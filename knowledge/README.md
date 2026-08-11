# Knowledge/review layer — source-only skeleton

This directory links clinical-indication ontology nodes to registry datasets without storing biological measurements or target conclusions.

The initial ontology follows the architecture requirement that a CRC indication is defined by more than a cancer label: disease state, molecular context, treatment line/history and anatomy must remain explicit. The evidence chain is tracked as separate axes:

`patient population → malignant cell state → surface target → functional dependency/payload vulnerability → normal-tissue therapeutic window`

Current links are `SOURCE_INDEXED_NOT_ANALYZED`. They indicate that a dataset is a plausible source for an evidence axis based on its registry metadata; they do not establish a biological claim, therapeutic window, target ranking or clinical efficacy.

Files:

- `schemas/clinical_indications.tsv`: seed indication ontology nodes.
- `schemas/evidence.tsv`: source-only evidence objects with claims, provenance, confidence and explicit review status.
- `schemas/indication_evidence_links.tsv`: source-level links from indication nodes to evidence objects and registry datasets.

The seed source is the user-provided `Asset-Generation-OS-architecture.md`, especially the CRC clinical-indication ontology and evidence-chain sections. Any future claim must add a reviewed source span, evidence object and human-review status.

Current source-only evidence objects: 9. DepMap 26Q1 is represented only at release level; its CRC subset and dependency results remain unmaterialized.
