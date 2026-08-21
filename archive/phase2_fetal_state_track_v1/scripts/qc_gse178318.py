#!/usr/bin/env python3
"""Reproducible structural and cell-level QC for the locked GSE178318 input.

This script deliberately reports distributions and reconciliation status only.
It does not choose QC cutoffs, call malignancy, or make a biological claim.
"""

from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_lines(path: Path) -> list[str]:
    with gzip.open(path, "rt") as handle:
        return [line.rstrip("\n\r") for line in handle]


def sample_key(barcode: str) -> str:
    parts = barcode.rsplit("_", 2)
    if len(parts) != 3:
        return "UNPARSEABLE"
    patient, material = parts[1], parts[2]
    return f"{patient}_{material}"


def quantiles(values: list[int]) -> dict[str, float | int | None]:
    if not values:
        return {"min": None, "p25": None, "median": None, "p75": None, "max": None}
    values = sorted(values)

    def percentile(p: float) -> float:
        pos = (len(values) - 1) * p
        lower, upper = int(pos), min(int(pos) + 1, len(values) - 1)
        return values[lower] + (values[upper] - values[lower]) * (pos - lower)

    return {
        "min": values[0],
        "p25": percentile(0.25),
        "median": percentile(0.50),
        "p75": percentile(0.75),
        "max": values[-1],
    }


def load_sample_map(path: Path) -> dict[str, dict[str, str]]:
    rows = {}
    with path.open(newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            material = {"PRIMARY_CRC": "CRC", "LIVER_METASTASIS": "LM", "PBMC": "PBMC"}.get(
                row["specimen_type"]
            )
            if material:
                rows[f'{row["patient_id"]}_{material}'] = row
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw-dir", type=Path, default=Path("archive/phase2_fetal_state_track_v1/phase2/03_data/raw/GSE178318"))
    parser.add_argument("--sample-map", type=Path, default=Path("DATA/registry/GSE178318/sample_map.tsv"))
    parser.add_argument("--marker-set", type=Path, default=Path("archive/phase2_fetal_state_track_v1/phase2/04_analysis_contracts/figure1_marker_set_v1.tsv"))
    parser.add_argument("--output", type=Path, default=Path("archive/phase2_fetal_state_track_v1/phase2/06_results/GSE178318/qc_summary.json"))
    args = parser.parse_args()

    raw = args.raw_dir
    files = {
        "barcodes": raw / "GSE178318_barcodes.tsv.gz",
        "genes": raw / "GSE178318_genes.tsv.gz",
        "matrix": raw / "GSE178318_matrix.mtx.gz",
    }
    barcodes = read_lines(files["barcodes"])
    genes = read_lines(files["genes"])
    sample_map = load_sample_map(args.sample_map)
    cell_keys = [sample_key(barcode) for barcode in barcodes]
    if any(key == "UNPARSEABLE" for key in cell_keys):
        raise ValueError("Barcode reconciliation failed: at least one barcode is unparseable")
    unmapped_keys = sorted({key for key in cell_keys if key not in sample_map})
    if unmapped_keys:
        raise ValueError(f"Barcode reconciliation failed: unmapped sample keys: {unmapped_keys}")
    missing_expected_keys = sorted(set(sample_map) - set(cell_keys))
    if missing_expected_keys:
        raise ValueError(f"Barcode reconciliation failed: expected sample keys absent: {missing_expected_keys}")

    per_cell_counts = [0] * len(barcodes)
    per_cell_detected = [0] * len(barcodes)
    header = None
    entries = 0
    with gzip.open(files["matrix"], "rt") as handle:
        for raw_line in handle:
            if raw_line.startswith("%"):
                continue
            if header is None:
                dims = raw_line.split()
                if len(dims) != 3:
                    raise ValueError(f"Invalid Matrix Market dimensions: {raw_line!r}")
                header = tuple(map(int, dims))
                continue
            row, column, value = raw_line.split()
            cell = int(column) - 1
            count = int(float(value))
            per_cell_counts[cell] += count
            per_cell_detected[cell] += 1
            entries += 1

    if header != (len(genes), len(barcodes), entries):
        raise ValueError(f"Matrix mismatch: header={header}, genes={len(genes)}, cells={len(barcodes)}, entries={entries}")

    sample_values: dict[str, dict[str, list[int]]] = defaultdict(lambda: {"total_counts": [], "detected_genes": []})
    for key, total, detected in zip(cell_keys, per_cell_counts, per_cell_detected):
        sample_values[key]["total_counts"].append(total)
        sample_values[key]["detected_genes"].append(detected)

    marker_rows = []
    with args.marker_set.open(newline="") as handle:
        marker_rows = list(csv.DictReader(handle, delimiter="\t"))
    gene_names = {name.split("\t", 1)[-1] for name in genes}
    marker_presence = {
        row["gene"]: row["gene"] in gene_names
        for row in marker_rows
    }
    missing_markers = sorted(gene for gene, present in marker_presence.items() if not present)
    if missing_markers:
        raise ValueError(f"Locked marker-set reconciliation failed: missing genes: {missing_markers}")

    summary = {
        "dataset": "GSE178318",
        "input_sha256": {key: sha256(path) for key, path in files.items()},
        "matrix": {
            "dimensions": {"genes": len(genes), "cells": len(barcodes), "nonzero_entries": entries},
            "orientation": "genes_by_cells",
        },
        "barcode_reconciliation": {
            "total_barcodes": len(barcodes),
            "parsed_barcodes": sum(key != "UNPARSEABLE" for key in cell_keys),
            "sample_keys_in_reviewed_map": sum(key in sample_map for key in set(cell_keys)),
            "unmapped_sample_keys": unmapped_keys,
            "missing_expected_sample_keys": missing_expected_keys,
        },
        "per_sample": {
            key: {
                "patient_id": sample_map.get(key, {}).get("patient_id"),
                "specimen_type": sample_map.get(key, {}).get("specimen_type"),
                "n_cells": len(values["total_counts"]),
                "total_counts": quantiles(values["total_counts"]),
                "detected_genes": quantiles(values["detected_genes"]),
            }
            for key, values in sorted(sample_values.items())
        },
        "locked_marker_set": {
            "path": str(args.marker_set),
            "version": "FIG1_MARKER_V1",
            "genes_present": sorted(gene for gene, present in marker_presence.items() if present),
            "genes_missing": missing_markers,
        },
        "interpretation_boundary": "Structural and distributional QC only; no cutoffs, malignancy call, target ranking, or clinical conclusion.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps({"output": str(args.output), "cells": len(barcodes), "entries": entries, "unmapped_sample_keys": summary["barcode_reconciliation"]["unmapped_sample_keys"]}, indent=2))


if __name__ == "__main__":
    main()
