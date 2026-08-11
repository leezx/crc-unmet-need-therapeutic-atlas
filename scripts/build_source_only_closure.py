#!/usr/bin/env python3
"""Build the source-only candidate closure matrix without network or data access."""
from __future__ import annotations

import argparse
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIELDS = [
    "dataset_id",
    "registry_status",
    "source_manifest",
    "file_inventory",
    "download_method_status",
    "update_coverage",
    "review_state",
    "closure_status",
    "remaining_blocker",
    "next_artifact",
]


def first_manifest_value(path: Path, field: str) -> str:
    if not path.exists():
        return ""
    with path.open(newline="") as handle:
        row = next(csv.DictReader(handle, delimiter="\t"), {})
    return row.get(field, "").strip()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=ROOT / "reports/SOURCE_ONLY_CLOSURE_MATRIX.tsv")
    args = parser.parse_args()
    output = args.output if args.output.is_absolute() else ROOT / args.output
    target_ids = set()
    targets = ROOT / "config/github_tree_targets.tsv"
    if targets.exists():
        with targets.open(newline="") as handle:
            target_ids = {row["target_id"].split("_supplementary")[0] for row in csv.DictReader(handle, delimiter="\t")}

    registry = ROOT / "DATA/registry/datasets.tsv"
    rows = []
    with registry.open(newline="") as handle:
        for record in csv.DictReader(handle, delimiter="\t"):
            dataset_id = record["dataset_id"]
            dataset_dir = ROOT / "DATA/registry" / dataset_id
            manifest = dataset_dir / "source_manifest.tsv"
            inventory = dataset_dir / "file_inventory.tsv"
            has_manifest = manifest.exists()
            has_inventory = inventory.exists()
            method = first_manifest_value(manifest, "download_method")
            source_manifest = "PRESENT" if has_manifest else "MISSING_SOURCE_RECORD"
            file_state = "PRESENT" if has_inventory else "NOT_MATERIALIZED"
            method_state = "RECORDED" if method else "MISSING"
            update_state = "WEEKLY_SOURCE_SCAN"
            if dataset_id in target_ids:
                update_state += "+PINNED_GITHUB_TARGET"
            if not has_manifest:
                update_state = "BLOCKED_NO_SOURCE_MANIFEST"
            if not has_manifest:
                closure = "EXTERNAL_BLOCKED"
                blocker = "Source manifest and reproducible landing/download path not yet recorded."
                next_artifact = "Create source_manifest.tsv after source verification."
            elif not has_inventory:
                closure = "EXTERNAL_BLOCKED"
                blocker = "File/archive inventory remains incomplete or source does not expose a reviewed file list."
                next_artifact = "Create file_inventory.tsv or an explicit no-file-inventory disposition."
            else:
                closure = "SOURCE_INDEXED_REVIEW_REQUIRED"
                blocker = "Dataset-specific license, clinical context, checksum or admission review may remain pending."
                next_artifact = "Review dataset checklist and retain UNKNOWN/NA where source evidence is absent."
            rows.append({
                "dataset_id": dataset_id,
                "registry_status": record["status"],
                "source_manifest": source_manifest,
                "file_inventory": file_state,
                "download_method_status": method_state,
                "update_coverage": update_state,
                "review_state": "CANDIDATE_SOURCE_ONLY",
                "closure_status": closure,
                "remaining_blocker": blocker,
                "next_artifact": next_artifact,
            })
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} source-only closure rows to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
