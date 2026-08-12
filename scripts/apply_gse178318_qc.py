#!/usr/bin/env python3
"""Apply the reviewed GSE178318 cell-QC rules and report retention only."""

from __future__ import annotations

import argparse
import csv
import gzip
import json
from collections import defaultdict
from pathlib import Path


RULES = {
    "permissive": {"detected_genes": 100, "total_counts": 300},
    "primary": {"detected_genes": 200, "total_counts": 500},
    "stringent": {"detected_genes": 300, "total_counts": 1000},
}


def sample_key(barcode: str) -> str:
    parts = barcode.rsplit("_", 2)
    if len(parts) != 3:
        raise ValueError(f"Unparseable barcode: {barcode}")
    return f"{parts[1]}_{parts[2]}"


def load_map(path: Path) -> dict[str, dict[str, str]]:
    mapping = {}
    with path.open(newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            suffix = {"PRIMARY_CRC": "CRC", "LIVER_METASTASIS": "LM", "PBMC": "PBMC"}.get(row["specimen_type"])
            if suffix:
                mapping[f'{row["patient_id"]}_{suffix}'] = row
    return mapping


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw-dir", type=Path, default=Path("phase2/03_data/raw/GSE178318"))
    parser.add_argument("--sample-map", type=Path, default=Path("DATA/registry/GSE178318/sample_map.tsv"))
    parser.add_argument("--output", type=Path, default=Path("phase2/06_results/GSE178318/qc_retention.json"))
    args = parser.parse_args()

    barcodes_path = args.raw_dir / "GSE178318_barcodes.tsv.gz"
    matrix_path = args.raw_dir / "GSE178318_matrix.mtx.gz"
    with gzip.open(barcodes_path, "rt") as handle:
        barcodes = [line.rstrip("\n\r") for line in handle]
    keys = [sample_key(barcode) for barcode in barcodes]
    sample_map = load_map(args.sample_map)
    observed = set(keys)
    if observed != set(sample_map):
        raise ValueError(f"Sample-key mismatch: observed_only={sorted(observed - set(sample_map))}; expected_only={sorted(set(sample_map) - observed)}")

    totals = [0] * len(barcodes)
    detected = [0] * len(barcodes)
    entries = 0
    header = None
    with gzip.open(matrix_path, "rt") as handle:
        for line in handle:
            if line.startswith("%"):
                continue
            if header is None:
                header = tuple(map(int, line.split()))
                continue
            row, column, value = line.split()
            cell = int(column) - 1
            totals[cell] += int(float(value))
            detected[cell] += 1
            entries += 1
    if header != (33694, len(barcodes), entries):
        raise ValueError(f"Matrix mismatch: header={header}, cells={len(barcodes)}, entries={entries}")

    per_rule = {}
    for rule_name, thresholds in RULES.items():
        by_sample = defaultdict(lambda: {"total": 0, "retained": 0})
        for key, total, genes in zip(keys, totals, detected):
            by_sample[key]["total"] += 1
            if genes >= thresholds["detected_genes"] and total >= thresholds["total_counts"]:
                by_sample[key]["retained"] += 1
        sample_rows = {}
        for key in sorted(by_sample):
            row = sample_map[key]
            total = by_sample[key]["total"]
            retained = by_sample[key]["retained"]
            sample_rows[key] = {
                "patient_id": row["patient_id"],
                "specimen_type": row["specimen_type"],
                "total_cells": total,
                "retained_cells": retained,
                "retention_fraction": retained / total,
            }
        eligible_patients = sorted({row["patient_id"] for row in sample_map.values() if row["specimen_type"] in {"PRIMARY_CRC", "LIVER_METASTASIS"}})
        paired_patients = [patient for patient in eligible_patients if all(sample_rows[f"{patient}_{suffix}"]["retained_cells"] > 0 for suffix in ("CRC", "LM"))]
        per_rule[rule_name] = {
            "thresholds": thresholds,
            "total_cells": sum(row["total_cells"] for row in sample_rows.values()),
            "retained_cells": sum(row["retained_cells"] for row in sample_rows.values()),
            "sample_rows": sample_rows,
            "matched_primary_liver_patients_with_retained_cells": paired_patients,
            "matched_pair_count": len(paired_patients),
        }

    primary = per_rule["primary"]
    sensitivity_labels = {}
    for name, result in per_rule.items():
        if name == "primary":
            sensitivity_labels[name] = "REFERENCE"
            continue
        changes = []
        for key, row in result["sample_rows"].items():
            base = primary["sample_rows"][key]["retained_cells"]
            if base == 0 or abs(row["retained_cells"] - base) / base > 0.20:
                changes.append(f"retention_change_over_20pct:{key}")
        if set(result["matched_primary_liver_patients_with_retained_cells"]) != set(primary["matched_primary_liver_patients_with_retained_cells"]):
            changes.append("matched_pair_set_changed")
        sensitivity_labels[name] = {"label": "QC_RETENTION_STABLE" if changes == [] else "QC_RETENTION_SENSITIVE", "reasons": changes, "direction_gate": "DEFERRED_TO_PATIENT_LEVEL_STATE_ANALYSIS"}

    output = {
        "dataset": "GSE178318",
        "matrix_nonzero_entries": entries,
        "rules": per_rule,
        "sensitivity_labels": sensitivity_labels,
        "interpretation_boundary": "Retention and matched-pair availability only; no state score, malignancy call, target ranking, or clinical conclusion.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps({"output": str(args.output), "rules": {name: {"retained_cells": value["retained_cells"], "matched_pair_count": value["matched_pair_count"]} for name, value in per_rule.items()}, "sensitivity_labels": sensitivity_labels}, indent=2))


if __name__ == "__main__":
    main()
