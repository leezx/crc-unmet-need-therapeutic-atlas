#!/usr/bin/env python3
"""Validate schemas/target_evidence.tsv and its cross-references.

Checks: header matches the schema exactly, target_evidence_id is unique,
target_id exists in DATA/registry/ADC_TARGET_SEED_UNIVERSE.tsv (a finding
can't be about a target that isn't in the seed universe), target_symbol
matches that target_id's registered symbol, indication_id exists in
schemas/clinical_indications.tsv, module is one of B-F, adc_decision_axis
is in the controlled vocabulary shared with module_classification.tsv,
evidence_directness is in {DIRECT, CALIBRATED_PROXY, UNCALIBRATED_PROXY,
UNKNOWN}, dataset_id (if not NA) exists in DATA/registry/datasets.tsv, and
source_evidence_id (if not NA) exists in schemas/evidence.tsv.
"""
import csv
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

MODULES = {"B", "C", "D", "E", "F"}
DECISION_AXES = {
    "prevalence", "refractory_or_treated_presence", "longitudinal_persistence",
    "clinical_endpoint_context", "protein_endpoint", "normal_tissue_risk",
    "delivery_proof", "population_proof", "functional_dependency",
    "reference_annotation", "none",
}
EVIDENCE_DIRECTNESS = {"DIRECT", "CALIBRATED_PROXY", "UNCALIBRATED_PROXY", "UNKNOWN"}


def load_tsv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def fail(msg):
    print(f"FAIL: {msg}", file=sys.stderr)
    sys.exit(1)


def main():
    schema_path = REPO_ROOT / "schemas" / "target_evidence.tsv"
    if not schema_path.is_file():
        fail(f"schema not found: {schema_path}")
    schema_header = schema_path.read_text().splitlines()[0].split("\t")

    with open(schema_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        if reader.fieldnames != schema_header:
            fail(f"header mismatch: {reader.fieldnames} != {schema_header}")
        rows = list(reader)

    if not rows:
        print("Target evidence validation passed: 0 rows (header-only, nothing to check)")
        return

    seed_path = REPO_ROOT / "DATA" / "registry" / "ADC_TARGET_SEED_UNIVERSE.tsv"
    targets = {r["target_id"]: r for r in load_tsv(seed_path)} if seed_path.is_file() else {}

    indications_path = REPO_ROOT / "schemas" / "clinical_indications.tsv"
    indication_ids = {r["indication_id"] for r in load_tsv(indications_path)}

    datasets_path = REPO_ROOT / "DATA" / "registry" / "datasets.tsv"
    dataset_ids = {r["dataset_id"] for r in load_tsv(datasets_path)}

    evidence_path = REPO_ROOT / "schemas" / "evidence.tsv"
    evidence_ids = {r["evidence_id"] for r in load_tsv(evidence_path)}

    seen_ids = set()
    errors = []
    for i, row in enumerate(rows, start=2):
        teid = row["target_evidence_id"]
        if teid in seen_ids:
            errors.append(f"line {i}: duplicate target_evidence_id {teid}")
        seen_ids.add(teid)

        tid = row["target_id"]
        if tid not in targets:
            errors.append(f"line {i} ({teid}): target_id {tid!r} not found in ADC_TARGET_SEED_UNIVERSE.tsv")
        elif row["target_symbol"] != targets[tid]["target_symbol"]:
            errors.append(
                f"line {i} ({teid}): target_symbol {row['target_symbol']!r} does not match "
                f"{tid}'s registered symbol {targets[tid]['target_symbol']!r}"
            )

        if row["indication_id"] not in indication_ids:
            errors.append(f"line {i} ({teid}): indication_id {row['indication_id']!r} not in schemas/clinical_indications.tsv")

        if row["module"] not in MODULES:
            errors.append(f"line {i} ({teid}): module {row['module']!r} not in {MODULES}")

        if row["adc_decision_axis"] not in DECISION_AXES:
            errors.append(f"line {i} ({teid}): adc_decision_axis {row['adc_decision_axis']!r} not in controlled vocabulary")

        if row["evidence_directness"] not in EVIDENCE_DIRECTNESS:
            errors.append(f"line {i} ({teid}): evidence_directness {row['evidence_directness']!r} not in {EVIDENCE_DIRECTNESS}")

        dsid = row["dataset_id"]
        if dsid and dsid != "NA" and dsid not in dataset_ids:
            errors.append(f"line {i} ({teid}): dataset_id {dsid!r} not found in DATA/registry/datasets.tsv")

        seid = row["source_evidence_id"]
        if seid and seid != "NA" and seid not in evidence_ids:
            errors.append(f"line {i} ({teid}): source_evidence_id {seid!r} not found in schemas/evidence.tsv")

        for field in schema_header:
            if row[field].strip() == "":
                errors.append(f"line {i} ({teid}): empty field {field!r} -- use NA/UNKNOWN, not blank")

    if errors:
        for e in errors:
            print(f"FAIL: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Target evidence validation passed: {len(rows)} rows, {len(seen_ids)} unique target_evidence_id")


if __name__ == "__main__":
    main()
