#!/usr/bin/env python3
"""Validate registry contracts without downloading biological data."""
from pathlib import Path
import csv, sys

ROOT = Path(__file__).resolve().parents[1]
expected = (ROOT / "schemas/dataset_registry.tsv").read_text().splitlines()[0].split("\t")
registry = ROOT / "DATA/registry/datasets.tsv"
errors = []
with registry.open(newline="") as fh:
    rows = list(csv.DictReader(fh, delimiter="\t"))
for i, row in enumerate(rows, 2):
    if list(row) != expected:
        errors.append(f"row {i}: registry columns do not match schema")
    dataset_id = row.get("dataset_id", "")
    if dataset_id and not (ROOT / "DATA/registry" / dataset_id).exists():
        errors.append(f"row {i}: missing directory for {dataset_id}")
    if row.get("status") not in {"CANDIDATE", "APPROVED", "REJECTED", "ARCHIVED"}:
        errors.append(f"row {i}: invalid status {row.get('status')!r}")
manifest_header = (ROOT / "schemas/source_manifest.tsv").read_text().splitlines()[0].split("\t")
for manifest in sorted((ROOT / "DATA/registry").glob("*/source_manifest.tsv")):
    if manifest.read_text().splitlines()[0].split("\t") != manifest_header:
        errors.append(f"{manifest}: header does not match schema")
if errors:
    print("REGISTRY VALIDATION FAILED\n" + "\n".join(f"- {e}" for e in errors))
    sys.exit(1)
print(f"Registry validation passed: {len(rows)} candidates")
