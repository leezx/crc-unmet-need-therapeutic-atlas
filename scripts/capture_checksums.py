#!/usr/bin/env python3
"""Hash explicitly staged external files; never download or mutate registry data."""
from pathlib import Path
import argparse, csv, hashlib, sys

parser = argparse.ArgumentParser()
parser.add_argument("--data-root", type=Path, required=True, help="External, non-repository data root")
parser.add_argument("--inventory", type=Path, required=True, help="Dataset file_inventory.tsv")
parser.add_argument("--output", type=Path, default=None, help="Optional TSV output path")
args = parser.parse_args()

fields = ["dataset_id", "file_id", "file_name", "path", "size_bytes", "md5", "sha256", "capture_status", "notes"]
rows = []
with args.inventory.open(newline="") as fh:
    for item in csv.DictReader(fh, delimiter="\t"):
        path = args.data_root / item["dataset_id"] / item["file_name"]
        row = {k: "" for k in fields}
        row.update(dataset_id=item["dataset_id"], file_id=item["file_id"], file_name=item["file_name"], path=str(path))
        if not path.is_file():
            row.update(capture_status="MISSING", notes="No local file; script did not download it.")
            rows.append(row)
            continue
        md5 = hashlib.md5()
        sha256 = hashlib.sha256()
        with path.open("rb") as stream:
            for block in iter(lambda: stream.read(1024 * 1024), b""):
                md5.update(block)
                sha256.update(block)
        row.update(size_bytes=str(path.stat().st_size), md5=md5.hexdigest(), sha256=sha256.hexdigest(), capture_status="CAPTURED", notes="Hash computed from explicitly staged local file; no download performed.")
        rows.append(row)

out = sys.stdout
handle = None
if args.output:
    args.output.parent.mkdir(parents=True, exist_ok=True)
    handle = args.output.open("w", newline="")
    out = handle
writer = csv.DictWriter(out, fieldnames=fields, delimiter="\t", lineterminator="\n")
writer.writeheader()
writer.writerows(rows)
if handle:
    handle.close()
print(f"Checksum capture complete: {len(rows)} inventory entries; no files downloaded.", file=sys.stderr)
