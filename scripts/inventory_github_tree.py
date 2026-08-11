#!/usr/bin/env python3
"""Inventory GitHub tree metadata without reading blob contents or downloading files."""
from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
from pathlib import Path
from urllib.request import Request, urlopen


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Write fixed-commit GitHub tree metadata for selected path prefixes."
    )
    parser.add_argument("--repo", required=True, help="GitHub repository, e.g. owner/name")
    parser.add_argument("--commit", required=True, help="Full 40-character commit SHA")
    parser.add_argument("--prefix", action="append", default=[], help="Path prefix; repeat for multiple prefixes")
    parser.add_argument("--output", type=Path, help="TSV output path; stdout if omitted")
    parser.add_argument("--timeout", type=float, default=30.0)
    return parser.parse_args()


def fetch_tree(repo: str, commit: str, timeout: float) -> dict:
    url = f"https://api.github.com/repos/{repo}/git/trees/{commit}?recursive=1"
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "CRC-Atlas-tree-inventory/0.1"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    with urlopen(Request(url, headers=headers), timeout=timeout) as response:
        return json.load(response)


def main() -> int:
    args = parse_args()
    prefixes = args.prefix or [""]
    if not re.fullmatch(r"[0-9a-fA-F]{40}", args.commit):
        raise SystemExit("--commit must be a full 40-character hexadecimal commit SHA")
    if any(prefix.startswith("/") for prefix in prefixes):
        raise SystemExit("prefixes must be repository-relative and must not start with '/'")
    payload = fetch_tree(args.repo, args.commit, args.timeout)
    if payload.get("truncated"):
        raise SystemExit("GitHub returned a truncated tree; narrow --prefix or use a paginated API workflow")
    rows = []
    for entry in payload.get("tree", []):
        path = entry.get("path", "")
        if entry.get("type") != "blob" or not any(path.startswith(prefix) for prefix in prefixes):
            continue
        rows.append({
            "repository": args.repo,
            "commit": args.commit,
            "path": path,
            "entry_type": entry.get("type", ""),
            "size_bytes": entry.get("size", ""),
            "git_blob_sha": entry.get("sha", ""),
            "source_url": f"https://github.com/{args.repo}/blob/{args.commit}/{path}",
        })
    rows.sort(key=lambda row: row["path"])
    fields = ["repository", "commit", "path", "entry_type", "size_bytes", "git_blob_sha", "source_url"]
    output = sys.stdout
    handle = None
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        handle = args.output.open("w", newline="")
        output = handle
    try:
        writer = csv.DictWriter(output, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    finally:
        if handle:
            handle.close()
    print(json.dumps({"repository": args.repo, "commit": args.commit, "files": len(rows)}), file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
