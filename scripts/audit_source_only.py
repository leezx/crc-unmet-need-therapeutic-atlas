#!/usr/bin/env python3
"""Verify that the repository remains source-only and reproducible."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN_SUFFIXES = (
    ".fastq", ".fastq.gz", ".fq", ".fq.gz", ".bam", ".bai", ".cram",
    ".crai", ".h5ad", ".h5", ".loom", ".rds", ".rda", ".mtx", ".mtx.gz",
    ".vcf", ".vcf.gz", ".cel", ".chp",
)
REQUIRED = (
    "config/project_completion.yaml",
    "reports/SOURCE_ONLY_CLOSURE_MATRIX.tsv",
    "reports/updates/UPDATE_TARGET_DISPOSITION.tsv",
    "reports/SOURCE_ONLY_FINAL_AUDIT.tsv",
)


def tracked_files():
    try:
        result = subprocess.run(
            ["git", "ls-files", "-z"], cwd=ROOT, check=True,
            capture_output=True,
        )
    except subprocess.CalledProcessError as exc:
        print(exc.stderr.decode(errors="replace"), file=sys.stderr)
        raise
    return [Path(p) for p in result.stdout.decode().split("\0") if p]


def main():
    files = tracked_files()
    tracked = {p.as_posix() for p in files}
    checks = []
    forbidden = [p.as_posix() for p in files if p.name.lower().endswith(FORBIDDEN_SUFFIXES)]
    raw_paths = [p.as_posix() for p in files if any(x in p.parts for x in ("raw", "processed", "data"))]
    large = [p.as_posix() for p in files if (ROOT / p).stat().st_size > 50 * 1024 * 1024]
    checks.append(("no_forbidden_biological_suffix", "PASS" if not forbidden else "FAIL", ";".join(forbidden) or "none"))
    checks.append(("no_raw_processed_or_data_paths", "PASS" if not raw_paths else "FAIL", ";".join(raw_paths) or "none"))
    checks.append(("no_tracked_file_over_50MiB", "PASS" if not large else "FAIL", ";".join(large) or "none"))
    missing = [p for p in REQUIRED if not (ROOT / p).exists() or p not in tracked]
    checks.append(("required_source_only_control_files", "PASS" if not missing else "FAIL", ";".join(missing) or "all present"))
    report = ROOT / "reports/SOURCE_ONLY_FINAL_AUDIT.tsv"
    report.write_text("audit_id\tstatus\tdetail\n" + "\n".join(f"{name}\t{status}\t{detail}" for name, status, detail in checks) + "\n")
    if any(status != "PASS" for _, status, _ in checks):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
