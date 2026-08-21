#!/usr/bin/env python3
"""Validate the canonical Module B-F activation-priority contract.

Checks DATA/registry/module_classification.tsv against
schemas/module_classification.tsv, a controlled vocabulary for module /
activation_status / adc_decision_axis / activation_rule, per-module
execution-order uniqueness, and full cross-reference against
DATA/registry/datasets.tsv (every dataset row is classified, every
classified id is a real dataset). Does not touch or require biological
data.

Added 2026-08-21 after web-ChatGPT review of PR #70 round 1
(REQUEST_CHANGES, item 2): module_classification.tsv previously had no
schema or controlled vocabulary, so an agent could not mechanically tell
which dataset to touch first, when, or when it's forbidden -- it had to
read free-text `reason` prose and interpret it. This script makes that
machine-checkable. datasets.tsv's own `priority` column (P0_DOWNLOAD /
P1_DOWNLOAD / REFERENCE_ONLY) is retained as legacy Phase 1
download-priority metadata only; it is not validated here as an
execution-priority signal -- module_classification.tsv is canonical for
that (see CONTRIBUTING.md).

Extended after round 2 review (REQUEST_CHANGES again): added
`clinical_endpoint_context` as a distinct adc_decision_axis from
`persistence` (a first-line/pretreatment response-association cohort is
not evidence of post-treatment target persistence), and added the
`activation_context` column + controlled vocabulary so a `context_specific`
activation_rule names its actual molecular/clinical territory instead of
leaving it in free-text `reason`.

Extended again after round 3 review (REQUEST_CHANGES a third time): a
bare `persistence` axis was itself a proxy-upgrade risk -- GSE274551 is a
single-timepoint baseline biopsy in refractory tissue (per its official
GEO design), not a paired pre/post-treatment measurement, so calling it
`persistence` silently upgraded "still present in refractory disease" to
"retained across treatment". Retired `persistence`; replaced with
`refractory_or_treated_presence` (single-timepoint presence in
treated/refractory/metastatic tissue) and `longitudinal_persistence`
(a real paired pre/post-treatment design on the same patient/lesion).
"""
from __future__ import annotations

import csv
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

MODULES = {"A", "B", "C", "D", "E", "F", "NONE"}
ACTIVATION_STATUSES = {
    "CORE_ACTIVE",
    "CORE_CONTEXT",
    "CORE_SUPPORT",
    "CONTEXT_ACTIVE",
    "SUPPORT",
    "REFERENCE_CORE",
    "REFERENCE_SUPPORT",
    "SUPPLEMENT",
    "SUPPLEMENT_FROZEN",
}
DECISION_AXES = {
    "prevalence",
    "refractory_or_treated_presence",
    "longitudinal_persistence",
    "clinical_endpoint_context",
    "protein_endpoint",
    "normal_tissue_risk",
    "delivery_proof",
    "population_proof",
    "functional_dependency",
    "reference_annotation",
    "none",
}
ACTIVATION_RULES = {
    "every_target",
    "context_specific",
    "after_shortlist_named_uncertainty",
    "reference_annotation_only",
    "never_default",
}
ACTIVATION_CONTEXTS = {
    "ANY",
    "RAS_MUTANT",
    "RAS_WT",
    "ANTI_EGFR_REFRACTORY",
    "MRD_RECURRENCE",
    "FIRST_LINE_VALIDATION",
}


def main() -> int:
    errors: list[str] = []

    schema = (ROOT / "schemas/module_classification.tsv").read_text().splitlines()[0].split("\t")
    classification_path = ROOT / "DATA/registry/module_classification.tsv"
    with classification_path.open(newline="") as fh:
        rows = list(csv.DictReader(fh, delimiter="\t"))
    for i, row in enumerate(rows, 2):
        if list(row) != schema:
            errors.append(f"row {i}: module_classification columns do not match schema")
            continue
        if row["module"] not in MODULES:
            errors.append(f"row {i} ({row['dataset_id']}): invalid module {row['module']!r}")
        if row["activation_status"] not in ACTIVATION_STATUSES:
            errors.append(f"row {i} ({row['dataset_id']}): invalid activation_status {row['activation_status']!r}")
        if row["adc_decision_axis"] not in DECISION_AXES:
            errors.append(f"row {i} ({row['dataset_id']}): invalid adc_decision_axis {row['adc_decision_axis']!r}")
        if row["activation_rule"] not in ACTIVATION_RULES:
            errors.append(f"row {i} ({row['dataset_id']}): invalid activation_rule {row['activation_rule']!r}")
        context = row["activation_context"]
        if row["module"] == "NONE":
            if context != "NA":
                errors.append(f"row {i} ({row['dataset_id']}): module=NONE rows must have activation_context=NA, got {context!r}")
        elif context not in ACTIVATION_CONTEXTS:
            errors.append(f"row {i} ({row['dataset_id']}): invalid activation_context {context!r}")
        if row["activation_rule"] == "context_specific" and context == "ANY":
            errors.append(f"row {i} ({row['dataset_id']}): activation_rule=context_specific must name a real activation_context, not ANY")
        order = row["default_execution_order"]
        if row["module"] == "NONE":
            if order != "NA":
                errors.append(f"row {i} ({row['dataset_id']}): module=NONE rows must have default_execution_order=NA, got {order!r}")
        else:
            if not order.isdigit() or int(order) < 1:
                errors.append(f"row {i} ({row['dataset_id']}): default_execution_order must be a positive integer for module={row['module']!r}, got {order!r}")

    # Per-module execution-order uniqueness (no two datasets tie for the same slot).
    seen_order: dict[tuple[str, str], str] = {}
    for i, row in enumerate(rows, 2):
        if row.get("module") in (None, "NONE") or not row.get("default_execution_order", "").isdigit():
            continue
        key = (row["module"], row["default_execution_order"])
        if key in seen_order:
            errors.append(
                f"row {i} ({row['dataset_id']}): default_execution_order {row['default_execution_order']} "
                f"in module {row['module']} duplicates {seen_order[key]}"
            )
        else:
            seen_order[key] = row["dataset_id"]

    # Cross-reference against the canonical dataset registry.
    registry_path = ROOT / "DATA/registry/datasets.tsv"
    with registry_path.open(newline="") as fh:
        registry_ids = {r["dataset_id"] for r in csv.DictReader(fh, delimiter="\t")}
    classified_ids = defaultdict(int)
    for row in rows:
        classified_ids[row.get("dataset_id", "")] += 1

    missing_from_classification = sorted(registry_ids - set(classified_ids))
    for dataset_id in missing_from_classification:
        errors.append(f"{dataset_id}: present in datasets.tsv but has no module_classification.tsv row")

    unknown_dataset_ids = sorted(set(classified_ids) - registry_ids)
    for dataset_id in unknown_dataset_ids:
        errors.append(f"{dataset_id}: present in module_classification.tsv but not in datasets.tsv")

    if errors:
        print("MODULE CLASSIFICATION VALIDATION FAILED\n" + "\n".join(f"- {e}" for e in errors))
        return 1
    print(f"Module classification validation passed: {len(rows)} rows, {len(registry_ids)} datasets covered")
    return 0


if __name__ == "__main__":
    sys.exit(main())
