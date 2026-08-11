# Phase 2 — five-figure skeleton

## Working title

**Therapeutically actionable surface vulnerabilities of plastic malignant epithelial states in metastatic colorectal cancer**

## One-sentence claim to test

跨患者 CRLM malignant epithelial plasticity states can be converted into a prioritized, normal-tissue-filtered surface-target shortlist with independent functional support.

## Figure plan

### Figure 1 — define the malignant state

- Question: which epithelial programs are recurrent across primary/CRLM and independent cohorts?
- Inputs: GSE178318, HTAN progressive plasticity, CRLM_NMP_ATLAS when data lock passes.
- Unit: patient/sample-level malignant epithelial cells or pseudobulk, not individual cells as independent replicates.
- Output: state program, malignant-cell QC, patient-level prevalence and replication score.
- Reviewer concern: state may be proliferation/stress or patient-specific batch.

### Figure 2 — connect state to clinical/metastatic context

- Question: is the state enriched in metastasis, treatment-exposed material or adverse clinical context?
- Inputs: matched primary/metastasis metadata where available; GSE159216 bulk comparator only after reconciliation.
- Output: patient-level enrichment, matched-pair effect, uncertainty and missingness map.
- Reviewer concern: treatment history and metastatic site may be confounded.

### Figure 3 — surface-target nomination and normal-tissue filter

- Question: which state-associated genes are surface-accessible and have a plausible normal-tissue window?
- Inputs: malignant-state scores, HPA normal-tissue references, GTEx comparator, curated surfaceome annotation.
- Output: auditable target funnel with exclusion reasons; no therapeutic claim from expression alone.
- Reviewer concern: transcript expression is not cell-surface protein abundance or internalization.

### Figure 4 — functional vulnerability

- Question: do nominated targets or state-linked genes have independent dependency/drug-response support?
- Inputs: DepMap/functional screens and CRC organoid/PDO resources only after access and file-level lock.
- Output: dependency concordance, context specificity and orthogonal support.
- Reviewer concern: dependency may reflect generic essentiality or model artifact.

### Figure 5 — independent validation and decision map

- Question: does the final shortlist replicate and map to a defined CRC clinical indication?
- Inputs: independent cohort, clinical indication ontology, source evidence and target dossiers.
- Output: target-by-indication matrix, evidence grades, failure modes and next validation experiment.
- Reviewer concern: target ranking must not be presented as clinical efficacy or approval.

## Minimum success criterion

At least one candidate survives all five gates with independent replication and functional support. If none survives, the project reports a negative target-discovery result and identifies the failed gate.
