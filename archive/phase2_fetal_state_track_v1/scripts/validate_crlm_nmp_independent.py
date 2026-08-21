#!/usr/bin/env python3
"""External cohort coverage audit of FIG1_MARKER_V1 in CRLM-NMP-ATLAS."""

from __future__ import annotations

import argparse
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


def decode(group: h5py.Group) -> list[str]:
    categories = [x.decode() if isinstance(x, bytes) else str(x) for x in group["categories"][:]]
    return [categories[int(i)] for i in group["codes"][:]]


def sign_flip_p(values: list[float]) -> float | None:
    if not values or len(values) > 20:
        return None
    observed = abs(sum(values) / len(values))
    extreme = sum(abs(sum(v * s for v, s in zip(values, signs)) / len(values)) >= observed - 1e-15 for signs in itertools.product((-1, 1), repeat=len(values)))
    return extreme / (2 ** len(values))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=Path("phase2/03_data/raw/CRLM_NMP_ATLAS/crlm_nmp_atlas.h5ad"))
    parser.add_argument("--output", type=Path, default=Path("phase2/06_results/CRLM_NMP_ATLAS/validation.json"))
    args = parser.parse_args()
    with h5py.File(args.input, "r") as f:
        features = [x.decode() if isinstance(x, bytes) else str(x) for x in f["var"]["gene_symbols"][:]]
        missing = sorted(set(sum(STATE.values(), [])) - set(features))
        if missing:
            raise RuntimeError(f"Missing locked markers: {', '.join(missing)}")
        marker_indices = {role: [features.index(gene) for gene in genes] for role, genes in STATE.items()}
        donors, materials, cell_types = (decode(f["obs"][key]) for key in ("donor_id", "material", "cell_type"))
        x = f["X"]
        grouped = defaultdict(lambda: defaultdict(list))
        for cell, (donor, material, cell_type) in enumerate(zip(donors, materials, cell_types)):
            if cell_type != "malignant cell":
                continue
            start, end = int(x["indptr"][cell]), int(x["indptr"][cell + 1])
            row = {int(col): float(value) for col, value in zip(x["indices"][start:end], x["data"][start:end])}
            for role, cols in marker_indices.items():
                grouped[(donor, material)][role].append(sum(row.get(col, 0.0) for col in cols) / len(cols))
    sample_scores = {f"{donor}_{material}": {"donor_id": donor, "material": material, "n_cells": len(next(iter(scores.values()))), "mean_scores": {role: sum(values) / len(values) for role, values in scores.items()}} for (donor, material), scores in sorted(grouped.items())}
    paired = []
    for donor in sorted(set(donors)):
        crlm, liver = sample_scores.get(f"{donor}_CRLM"), sample_scores.get(f"{donor}_adj.liver")
        if crlm and liver:
            paired.append({"donor_id": donor, "crlm_cells": crlm["n_cells"], "adjacent_liver_cells": liver["n_cells"], "differences_crlm_minus_adjacent_liver": {role: crlm["mean_scores"][role] - liver["mean_scores"][role] for role in STATE}})
    summary = {}
    for role in STATE:
        values = [row["differences_crlm_minus_adjacent_liver"][role] for row in paired]
        summary[role] = {"n_pairs": len(values), "mean_difference": sum(values) / len(values) if values else None, "positive_pairs": sum(v > 0 for v in values), "negative_pairs": sum(v < 0 for v in values), "exact_two_sided_sign_flip_p": sign_flip_p(values)}
    result = {"dataset": "CRLM_NMP_ATLAS", "asset": str(args.input), "n_cells": len(donors), "n_donors": len(set(donors)), "malignant_cells": sum(x == "malignant cell" for x in cell_types), "matched_crlm_adjacent_liver_pairs": len(paired), "marker_coverage": {role: {"genes": genes, "n_present": len(genes)} for role, genes in STATE.items()}, "sample_scores": sample_scores, "paired_effect_summary": summary, "interpretation_boundary": "External cohort coverage and descriptive audit; CRLM-versus-adjacent-liver is not equivalent to the locked primary-versus-metastasis contrast; no independent-validation, causal, target-ranking, therapeutic-window or clinical conclusion."}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"n_cells": result["n_cells"], "n_donors": result["n_donors"], "malignant_cells": result["malignant_cells"], "matched_pairs": result["matched_crlm_adjacent_liver_pairs"], "summary": summary}, indent=2))


if __name__ == "__main__":
    main()
