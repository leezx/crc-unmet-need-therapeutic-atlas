#!/usr/bin/env python3
"""Offline regression tests for the metadata-only GitHub scanners."""
from __future__ import annotations

import csv
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

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
            self.assertFalse(output_dir.exists())
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("duplicate target_id", result.stderr)

    def test_drift_checker_uses_ref_metadata_only(self) -> None:
        spec = importlib.util.spec_from_file_location(
            "check_github_target_updates", ROOT / "scripts/check_github_target_updates.py"
        )
        module = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as temp_dir:
            config = Path(temp_dir) / "targets.tsv"
            output = Path(temp_dir) / "updates.tsv"
            with config.open("w", newline="") as handle:
                writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
                writer.writerow(["target_id", "repository", "commit", "tracking_ref", "prefix", "output_name", "notes"])
                writer.writerow(["target", "owner/name", "a" * 40, "main", "", "target.tsv", ""])
            requested_urls = []

            class Response:
                def __enter__(self):
                    return self

                def __exit__(self, *args):
                    return False

                def read(self):
                    return json.dumps({"object": {"sha": "b" * 40}}).encode()

            def fake_urlopen(request, timeout):
                requested_urls.append(request.full_url)
                return Response()

            argv = ["check_github_target_updates.py", "--config", str(config), "--output", str(output)]
            with patch.object(module, "urlopen", fake_urlopen), patch.object(sys, "argv", argv):
                self.assertEqual(module.main(), 0)
            self.assertEqual(len(requested_urls), 1)
            self.assertIn("/git/ref/heads%2Fmain", requested_urls[0])
            self.assertNotIn("/commits/", requested_urls[0])
            self.assertIn("b" * 40, output.read_text())
            self.assertIn("TRUE", output.read_text())

    def test_source_only_closure_builder_is_offline_and_complete(self) -> None:
        result = self.run_script("build_source_only_closure.py")
        self.assertEqual(result.returncode, 0, result.stderr)
        matrix = ROOT / "reports/SOURCE_ONLY_CLOSURE_MATRIX.tsv"
        with matrix.open(newline="") as handle:
            rows = list(csv.DictReader(handle, delimiter="\t"))
        self.assertEqual(len(rows), 19)
        self.assertTrue(all(row["review_state"] == "CANDIDATE_SOURCE_ONLY" for row in rows))
        self.assertTrue(any(row["closure_status"] == "INTERNAL_ACTION_REQUIRED" for row in rows))
        self.assertTrue(any(row["file_inventory"] == "NO_FILE_INVENTORY_DISPOSITION" for row in rows))
        self.assertTrue(all(row["closure_status"] != "INTERNAL_ACTION_REQUIRED" for row in rows if row["file_inventory"] == "NO_FILE_INVENTORY_DISPOSITION"))
        self.assertTrue(all(row["blocker_class"] for row in rows))


if __name__ == "__main__":
    unittest.main()
