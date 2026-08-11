#!/usr/bin/env python3
"""Compare pinned GitHub commits with a tracking ref using metadata only."""
from __future__ import annotations

import argparse
import csv
import json
import os
import re
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description="Check configured GitHub target refs for new commits.")
    parser.add_argument("--config", type=Path, default=ROOT / "config/github_tree_targets.tsv")
    parser.add_argument("--output", type=Path, default=ROOT / "reports/github_tree_scan/update_candidates.tsv")
    args = parser.parse_args()
    config = args.config if args.config.is_absolute() else ROOT / args.config
    output = args.output if args.output.is_absolute() else ROOT / args.output
    with config.open(newline="") as handle:
        targets = list(csv.DictReader(handle, delimiter="\t"))
    required = {"target_id", "repository", "commit", "tracking_ref"}
    if not targets or not required.issubset(targets[0]):
        raise SystemExit(f"config must contain columns: {', '.join(sorted(required))}")
    if len({row["target_id"] for row in targets}) != len(targets):
        raise SystemExit("config contains duplicate target_id values")
    rows = []
    for target in targets:
        if not re.fullmatch(r"[0-9a-fA-F]{40}", target["commit"]):
            raise SystemExit(f"invalid pinned commit for {target['target_id']}")
        url = f"https://api.github.com/repos/{target['repository']}/commits/{quote(target['tracking_ref'], safe='')}"
        headers = {"Accept": "application/vnd.github+json", "User-Agent": "CRC-Atlas-update-check/0.1"}
        token = os.environ.get("GITHUB_TOKEN")
        if token:
            headers["Authorization"] = f"Bearer {token}"
        request = Request(url, headers=headers)
        with urlopen(request, timeout=30) as response:
            payload = json.load(response)
        latest = payload.get("sha", "")
        if not re.fullmatch(r"[0-9a-fA-F]{40}", latest):
            raise SystemExit(f"GitHub returned invalid commit SHA for {target['target_id']}")
        rows.append({"target_id": target["target_id"], "repository": target["repository"], "tracking_ref": target["tracking_ref"], "pinned_commit": target["commit"], "latest_commit": latest, "update_available": str(latest.lower() != target["commit"].lower()).upper(), "source_url": url})
    output.parent.mkdir(parents=True, exist_ok=True)
    fields = ["target_id", "repository", "tracking_ref", "pinned_commit", "latest_commit", "update_available", "source_url"]
    with output.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(json.dumps({"targets": len(rows), "updates": sum(row["update_available"] == "TRUE" for row in rows)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
