#!/usr/bin/env python3
"""Run configured fixed-commit GitHub tree inventories without fetching blobs."""
from __future__ import annotations

import argparse
import csv
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCANNER = ROOT / "scripts/inventory_github_tree.py"


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan configured GitHub tree metadata targets.")
    parser.add_argument("--config", type=Path, default=ROOT / "config/github_tree_targets.tsv")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "reports/github_tree_scan")
    args = parser.parse_args()
    config_path = args.config if args.config.is_absolute() else ROOT / args.config
    output_dir = args.output_dir if args.output_dir.is_absolute() else ROOT / args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    with config_path.open(newline="") as handle:
        targets = list(csv.DictReader(handle, delimiter="\t"))
    required = {"target_id", "repository", "commit", "prefix", "output_name"}
    if not targets or not required.issubset(targets[0]):
        raise SystemExit(f"config must contain columns: {', '.join(sorted(required))}")
    target_ids = [target["target_id"] for target in targets]
    output_names = [target["output_name"] for target in targets]
    if len(set(target_ids)) != len(target_ids):
        raise SystemExit("config contains duplicate target_id values")
    if len(set(output_names)) != len(output_names):
        raise SystemExit("config contains duplicate output_name values")

    for target in targets:
        if not re.fullmatch(r"[A-Za-z0-9_.-]+", target["target_id"]):
            raise SystemExit(f"invalid target_id: {target['target_id']}")
        output_name = Path(target["output_name"])
        if output_name.name != target["output_name"] or output_name.suffix != ".tsv":
            raise SystemExit(f"output_name must be a plain .tsv filename: {target['output_name']}")
        output_path = output_dir / output_name
        command = [
            sys.executable,
            str(SCANNER),
            "--repo", target["repository"],
            "--commit", target["commit"],
            "--prefix", target["prefix"],
            "--output", str(output_path),
        ]
        subprocess.run(command, cwd=ROOT, check=True)
        print(f"scanned {target['target_id']} -> {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
