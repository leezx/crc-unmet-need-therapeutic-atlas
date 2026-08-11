#!/usr/bin/env python3
"""Offline regression tests for the metadata-only GitHub scanners."""
from __future__ import annotations

import csv
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class GitHubScannerTests(unittest.TestCase):
    def run_script(self, script: str, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(ROOT / "scripts" / script), *args],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )

    def test_inventory_rejects_floating_ref_without_network(self) -> None:
        result = self.run_script(
            "inventory_github_tree.py",
            "--repo", "owner/name",
            "--commit", "master",
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("full 40-character hexadecimal commit SHA", result.stderr)

    def test_batch_scanner_rejects_duplicate_target_before_scan(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            config = Path(temp_dir) / "targets.tsv"
            output_dir = Path(temp_dir) / "output"
            fields = ["target_id", "repository", "commit", "prefix", "output_name", "notes"]
            rows = [
                ["same", "owner/name", "a" * 40, "data", "one.tsv", ""],
                ["same", "owner/other", "b" * 40, "data", "two.tsv", ""],
            ]
            with config.open("w", newline="") as handle:
                writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
                writer.writerow(fields)
                writer.writerows(rows)
            result = self.run_script(
                "scan_github_targets.py",
                "--config", str(config),
                "--output-dir", str(output_dir),
            )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("duplicate target_id", result.stderr)
        self.assertFalse(output_dir.exists())


if __name__ == "__main__":
    unittest.main()
