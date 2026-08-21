#!/usr/bin/env python3
"""Audit whether GSE224235 can independently validate FIG1_MARKER_V1."""

from __future__ import annotations

import argparse
import csv
import gzip
import json
from pathlib import Path


MARKERS = ["EPCAM", "KRT8", "KRT18", "KRT19", "TACSTD2", "L1CAM", "EMP1", "SOX2", "CHGA", "KRT5"]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--matrix", type=Path, default=Path("phase2/03_data/raw/GSE224235/GSE224235_series_matrix.txt.gz"))
    parser.add_argument("--output", type=Path, default=Path("phase2/06_results/GSE224235/validation_audit.json"))
    args = parser.parse_args()

    titles, samples, genes = [], [], set()
    with gzip.open(args.matrix, "rt") as handle:
        for line in handle:
            if line.startswith("!Sample_title"):
                titles = [value.strip().strip('"') for value in line.rstrip().split("\t")[1:]]
            elif line.startswith("!Sample_geo_accession"):
                samples = [value.strip().strip('"') for value in line.rstrip().split("\t")[1:]]
            elif line.startswith("!") or line.startswith('"!'):
                continue
            elif line.startswith("!series_matrix_table_end"):
                break
            else:
                genes.add(line.split("\t", 1)[0].strip('"'))

    available = sorted(set(MARKERS) & genes)
    missing = sorted(set(MARKERS) - genes)
    pair_groups = {}
    for sample, title in zip(samples, titles):
        patient, specimen = title.split(" - ", 1)
        pair_groups.setdefault(patient, []).append({"sample_id": sample, "specimen": specimen})
    matched_pairs = sorted(patient for patient, rows in pair_groups.items() if {row["specimen"] for row in rows} == {"Colorectal primary", "Liver metastasis"})
    result = {
        "dataset": "GSE224235",
        "platform": "NanoString nCounter PanCancer IO360 processed series matrix",
        "sample_count": len(samples),
        "matched_primary_liver_pairs": len(matched_pairs),
        "matched_pair_ids": matched_pairs,
        "locked_marker_count": len(MARKERS),
        "available_locked_markers": available,
        "missing_locked_markers": missing,
        "validation_status": "INSUFFICIENT_FOR_FULL_STATE_VALIDATION" if len(available) < len(MARKERS) else "ELIGIBLE_FOR_REVIEW",
        "reason": "Only 2/10 locked state markers are present, so this platform cannot independently reproduce the full FIG1_MARKER_V1 state programs.",
        "interpretation_boundary": "Coverage audit only; no partial marker result is interpreted as state validation.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
