#!/usr/bin/env python3
"""Compute locked-marker, patient-level descriptive scores for GSE178318."""

from __future__ import annotations

import argparse
import csv
import gzip
import json
import math
import itertools
from collections import defaultdict
from pathlib import Path


RULE = {"detected_genes": 200, "total_counts": 500}


def sample_key(barcode: str) -> str:
    parts = barcode.rsplit("_", 2)
    if len(parts) != 3:
        raise ValueError(f"Unparseable barcode: {barcode}")
    return f"{parts[1]}_{parts[2]}"


def load_sample_map(path: Path) -> dict[str, dict[str, str]]:
    mapping = {}
    with path.open(newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            suffix = {"PRIMARY_CRC": "CRC", "LIVER_METASTASIS": "LM", "PBMC": "PBMC"}.get(row["specimen_type"])
            if suffix:
                mapping[f'{row["patient_id"]}_{suffix}'] = row
    return mapping


def exact_sign_flip_pvalue(values: list[float]) -> float | None:
    if not values:
        return None
    observed = abs(sum(values) / len(values))
    extreme = 0
    total = 0
    for signs in itertools.product((-1, 1), repeat=len(values)):
        permuted = abs(sum(value * sign for value, sign in zip(values, signs)) / len(values))
        extreme += permuted >= observed - 1e-15
        total += 1
    return extreme / total


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw-dir", type=Path, default=Path("phase2/03_data/raw/GSE178318"))
    parser.add_argument("--sample-map", type=Path, default=Path("DATA/registry/GSE178318/sample_map.tsv"))
    parser.add_argument("--marker-set", type=Path, default=Path("phase2/04_analysis_contracts/figure1_marker_set_v1.tsv"))
    parser.add_argument("--output", type=Path, default=Path("phase2/06_results/GSE178318/state_scores.json"))
    args = parser.parse_args()

    with gzip.open(args.raw_dir / "GSE178318_barcodes.tsv.gz", "rt") as handle:
        barcodes = [line.rstrip("\n\r") for line in handle]
    keys = [sample_key(barcode) for barcode in barcodes]
    sample_map = load_sample_map(args.sample_map)
    if set(keys) != set(sample_map):
        raise ValueError("Sample-key reconciliation failed")

    gene_names = []
    with gzip.open(args.raw_dir / "GSE178318_genes.tsv.gz", "rt") as handle:
        for line in handle:
            fields = line.rstrip("\n\r").split("\t")
            gene_names.append(fields[1] if len(fields) > 1 else fields[0])

    marker_sets = defaultdict(list)
    role_alias = {
        "epithelial_identity": "epithelial_identity",
        "healing_plasticity_anchor": "plasticity_anchor",
        "noncanonical_plasticity_anchor": "noncanonical_anchor",
        "noncanonical_lineage_anchor": "noncanonical_anchor",
    }
    with args.marker_set.open(newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            if row["role"] in role_alias and (row["use"] == "state_score" or row["role"] == "epithelial_identity"):
                marker_sets[role_alias[row["role"]]].append(row["gene"])
    roles = ["epithelial_identity", "plasticity_anchor", "noncanonical_anchor"]
    missing = sorted({gene for role in roles for gene in marker_sets[role] if gene not in gene_names})
    if missing:
        raise ValueError(f"Marker reconciliation failed: {missing}")
    target_rows = {index: gene_names[index] for index in range(len(gene_names)) if gene_names[index] in {gene for role in roles for gene in marker_sets[role]}}
    gene_role = {gene: role for role in roles for gene in marker_sets[role]}

    totals = [0] * len(barcodes)
    detected = [0] * len(barcodes)
    marker_counts = {role: {gene: [0] * len(barcodes) for gene in marker_sets[role]} for role in roles}
    entries = 0
    header = None
    with gzip.open(args.raw_dir / "GSE178318_matrix.mtx.gz", "rt") as handle:
        for line in handle:
            if line.startswith("%"):
                continue
            if header is None:
                header = tuple(map(int, line.split()))
                continue
            row, column, value = line.split()
            row_index, cell_index = int(row) - 1, int(column) - 1
            count = int(float(value))
            totals[cell_index] += count
            detected[cell_index] += 1
            if row_index in target_rows:
                gene = target_rows[row_index]
                marker_counts[gene_role[gene]][gene][cell_index] += count
            entries += 1
    if header != (len(gene_names), len(barcodes), entries):
        raise ValueError(f"Matrix mismatch: {header}, genes={len(gene_names)}, cells={len(barcodes)}, entries={entries}")

    by_sample = defaultdict(lambda: {"n_retained_cells": 0, "scores": defaultdict(list)})
    for cell, key in enumerate(keys):
        if detected[cell] < RULE["detected_genes"] or totals[cell] < RULE["total_counts"]:
            continue
        by_sample[key]["n_retained_cells"] += 1
        library_scale = 10000 / totals[cell]
        for role in roles:
            values = [math.log1p(marker_counts[role][gene][cell] * library_scale) for gene in marker_sets[role]]
            by_sample[key]["scores"][role].append(sum(values) / len(values))

    sample_scores = {}
    for key in sorted(by_sample):
        sample_scores[key] = {
            "patient_id": sample_map[key]["patient_id"],
            "specimen_type": sample_map[key]["specimen_type"],
            "n_retained_cells": by_sample[key]["n_retained_cells"],
            "mean_scores": {role: sum(values) / len(values) for role, values in by_sample[key]["scores"].items()},
        }

    patients = sorted({row["patient_id"] for row in sample_map.values() if row["specimen_type"] in {"PRIMARY_CRC", "LIVER_METASTASIS"}})
    paired = []
    for patient in patients:
        primary, metastasis = sample_scores.get(f"{patient}_CRC"), sample_scores.get(f"{patient}_LM")
        if not primary or not metastasis:
            continue
        paired.append({
            "patient_id": patient,
            "primary_retained_cells": primary["n_retained_cells"],
            "metastasis_retained_cells": metastasis["n_retained_cells"],
            "differences_metastasis_minus_primary": {role: metastasis["mean_scores"][role] - primary["mean_scores"][role] for role in roles},
        })
    paired_summary = {}
    for role in roles:
        differences = [row["differences_metastasis_minus_primary"][role] for row in paired]
        paired_summary[role] = {
            "n_pairs": len(differences),
            "mean_difference": sum(differences) / len(differences) if differences else None,
            "positive_pairs": sum(value > 0 for value in differences),
            "negative_pairs": sum(value < 0 for value in differences),
            "zero_pairs": sum(value == 0 for value in differences),
            "exact_two_sided_sign_flip_p": exact_sign_flip_pvalue(differences),
        }

    output = {
        "dataset": "GSE178318",
        "qc_rule": RULE,
        "marker_set_version": "FIG1_MARKER_V1",
        "matrix_nonzero_entries": entries,
        "sample_scores": sample_scores,
        "paired_patient_effects": paired,
        "paired_effect_summary": paired_summary,
        "interpretation_boundary": "Descriptive patient-level marker scores only; no malignancy call, target ranking, therapeutic-window or clinical conclusion.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps({"output": str(args.output), "n_pairs": len(paired), "paired_effect_summary": paired_summary}, indent=2))


if __name__ == "__main__":
    main()
