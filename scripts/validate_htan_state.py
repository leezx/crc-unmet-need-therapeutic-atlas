#!/usr/bin/env python3
"""Independent patient-level validation of FIG1_MARKER_V1 in HTAN/CELLxGENE."""

from __future__ import annotations

import argparse
import csv
import itertools
import json
from collections import defaultdict
from pathlib import Path

import h5py


STATE = {
    "epithelial_identity": ["EPCAM", "KRT8", "KRT18", "KRT19"],
    "plasticity_anchor": ["TACSTD2", "L1CAM", "EMP1"],
    "noncanonical_anchor": ["SOX2", "CHGA", "KRT5"],
}
CONFOUNDERS = {
    "cell_cycle_report": ["MKI67", "TOP2A", "STMN1"],
    "stress_report": ["FOS", "JUN", "HSPA1A"],
}


def sign_flip_p(values: list[float]) -> float | None:
    if not values:
        return None
    observed = abs(sum(values) / len(values))
    extreme = 0
    total = 0
    for signs in itertools.product((-1, 1), repeat=len(values)):
        extreme += abs(sum(v * s for v, s in zip(values, signs)) / len(values)) >= observed - 1e-15
        total += 1
    return extreme / total


def decode_categorical(group: h5py.Group) -> list[str]:
    categories = [x.decode() if isinstance(x, bytes) else str(x) for x in group["categories"][:]]
    return [categories[int(i)] for i in group["codes"][:]]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=Path("phase2/03_data/raw/HTAN_CRC_progressive_plasticity/epithelial.h5ad"))
    parser.add_argument("--output", type=Path, default=Path("phase2/06_results/HTAN_CRC_progressive_plasticity/validation.json"))
    args = parser.parse_args()

    with h5py.File(args.input, "r") as f:
        feature_group = f["var"]["feature_name"]
        categories = [x.decode() if isinstance(x, bytes) else str(x) for x in feature_group["categories"][:]]
        features = [categories[int(i)] for i in feature_group["codes"][:]]
        all_groups = {**STATE, **CONFOUNDERS}
        marker_indices = {role: {features.index(gene) for gene in genes} for role, genes in all_groups.items()}
        patients = decode_categorical(f["obs"]["Patient"])
        sample_types = decode_categorical(f["obs"]["Sample Type"])
        sites = decode_categorical(f["obs"]["Site"])
        x = f["X"]
        data, indices, indptr = x["data"], x["indices"], x["indptr"]
        per_cell = []
        for cell in range(len(patients)):
            start, end = int(indptr[cell]), int(indptr[cell + 1])
            row_indices = indices[start:end]
            row_values = data[start:end]
            scores = {}
            for role, cols in marker_indices.items():
                values = [float(value) for col, value in zip(row_indices, row_values) if int(col) in cols]
                scores[role] = sum(values) / len(cols)
            per_cell.append(scores)

    grouped = defaultdict(lambda: defaultdict(list))
    for patient, sample_type, scores in zip(patients, sample_types, per_cell):
        if sample_type not in {"Primary", "Metastasis"}:
            continue
        for role, value in scores.items():
            grouped[(patient, sample_type)][role].append(value)

    sample_scores = {}
    for (patient, sample_type), scores in sorted(grouped.items()):
        sample_scores[f"{patient}_{sample_type}"] = {
            "patient_id": patient,
            "sample_type": sample_type,
            "n_cells": len(next(iter(scores.values()))),
            "mean_scores": {role: sum(values) / len(values) for role, values in scores.items() if role in STATE},
            "confounder_scores": {role: sum(values) / len(values) for role, values in scores.items() if role in CONFOUNDERS},
        }

    paired = []
    for patient in sorted(set(patients)):
        primary, metastasis = sample_scores.get(f"{patient}_Primary"), sample_scores.get(f"{patient}_Metastasis")
        if not primary or not metastasis:
            continue
        paired.append({
            "patient_id": patient,
            "primary_cells": primary["n_cells"],
            "metastasis_cells": metastasis["n_cells"],
            "differences_metastasis_minus_primary": {role: metastasis["mean_scores"][role] - primary["mean_scores"][role] for role in STATE},
        })

    summary = {}
    for role in STATE:
        values = [row["differences_metastasis_minus_primary"][role] for row in paired]
        summary[role] = {
            "n_pairs": len(values),
            "mean_difference": sum(values) / len(values) if values else None,
            "positive_pairs": sum(v > 0 for v in values),
            "negative_pairs": sum(v < 0 for v in values),
            "exact_two_sided_sign_flip_p": sign_flip_p(values),
        }

    result = {
        "dataset": "HTAN_CRC_progressive_plasticity",
        "asset": str(args.input),
        "n_cells": len(patients),
        "n_patients": len(set(patients)),
        "matched_primary_metastasis_pairs": len(paired),
        "marker_coverage": {role: {"present": genes, "n_present": len(genes)} for role, genes in STATE.items()},
        "sample_scores": sample_scores,
        "paired_effect_summary": summary,
        "interpretation_boundary": "Independent patient-level validation of locked marker scores; no causal claim, target ranking, therapeutic-window or clinical conclusion.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"n_cells": result["n_cells"], "n_patients": result["n_patients"], "matched_pairs": len(paired), "summary": summary}, indent=2))


if __name__ == "__main__":
    main()
