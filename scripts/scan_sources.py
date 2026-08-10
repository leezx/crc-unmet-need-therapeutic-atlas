#!/usr/bin/env python3
"""Probe source landing pages only; never downloads dataset files."""
from pathlib import Path
from urllib.request import Request, urlopen
import argparse, csv, datetime, json

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument("--offline", action="store_true")
args = parser.parse_args()
rows = list(csv.DictReader((ROOT / "DATA/registry/datasets.tsv").open(), delimiter="\t"))
results = []
for row in rows:
    manifest = ROOT / "DATA/registry" / row["dataset_id"] / "source_manifest.tsv"
    url = ""
    if manifest.exists():
        with manifest.open() as fh:
            url = next(csv.DictReader(fh, delimiter="\t"), {}).get("source_url", "")
    result = {"dataset_id": row["dataset_id"], "url": url, "status": "OFFLINE"}
    if url and not args.offline:
        try:
            req = Request(url, method="HEAD", headers={"User-Agent": "CRC-Atlas-source-scan/0.1"})
            with urlopen(req, timeout=20) as response:
                result.update(status="REACHABLE", http_status=response.status)
        except Exception as exc:
            result.update(status="UNREACHABLE_OR_BLOCKED", error=type(exc).__name__)
    results.append(result)
out = ROOT / "reports/generated"
out.mkdir(parents=True, exist_ok=True)
(out / "source_scan.json").write_text(json.dumps(results, indent=2) + "\n")
(out / "source_scan_runs.jsonl").open("a").write(json.dumps({"checked_at": datetime.datetime.now(datetime.timezone.utc).isoformat(), "offline": args.offline, "datasets": len(results)}) + "\n")
print(json.dumps({"datasets": len(results), "output": str(out / 'source_scan.json')}, indent=2))
