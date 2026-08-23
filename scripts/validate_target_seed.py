#!/usr/bin/env python3
"""Validate DATA/registry/ADC_TARGET_SEED_UNIVERSE.tsv against schemas/target_seed.tsv.

Checks: header matches the schema exactly, target_id/target_symbol are unique,
target_id follows the tgt_<lowercase symbol> convention, derisking_tier and
repurposing_status are in their controlled vocabularies, and the admission-gate
default rule from ADC_ATLAS_DATASET_CONTRACT.md holds (A_CLINICAL/B_PRECLINICAL_ADC
default to ACTIVE; C_ANTIBODY_OR_BIOLOGY_ONLY defaults to FUTURE unless a note
explains an exception).
"""
import csv
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = REPO_ROOT / "schemas" / "target_seed.tsv"
DATA_PATH = REPO_ROOT / "DATA" / "registry" / "ADC_TARGET_SEED_UNIVERSE.tsv"

DERISKING_TIERS = {"A_CLINICAL", "B_PRECLINICAL_ADC", "C_ANTIBODY_OR_BIOLOGY_ONLY"}
REPURPOSING_STATUSES = {"ACTIVE", "FUTURE", "EXCLUDED"}
DEFAULT_ACTIVE_TIERS = {"A_CLINICAL", "B_PRECLINICAL_ADC"}


def fail(msg):
    print(f"FAIL: {msg}", file=sys.stderr)
    sys.exit(1)


def main():
    if not SCHEMA_PATH.is_file():
        fail(f"schema not found: {SCHEMA_PATH}")
    if not DATA_PATH.is_file():
        fail(f"data file not found: {DATA_PATH}")

    schema_header = SCHEMA_PATH.read_text().splitlines()[0].split("\t")

    with open(DATA_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        if reader.fieldnames != schema_header:
            fail(
                "header mismatch\n"
                f"  schema: {schema_header}\n"
                f"  data:   {reader.fieldnames}"
            )
        rows = list(reader)

    if not rows:
        fail("no data rows (header-only file) -- run scripts/build_target_seed_universe.py")

    seen_ids = set()
    seen_symbols = set()
    errors = []

    for i, row in enumerate(rows, start=2):  # 1-indexed + header row
        tid = row["target_id"]
        sym = row["target_symbol"]
        if tid in seen_ids:
            errors.append(f"line {i}: duplicate target_id {tid}")
        seen_ids.add(tid)
        if sym in seen_symbols:
            errors.append(f"line {i}: duplicate target_symbol {sym}")
        seen_symbols.add(sym)

        expected_id = f"tgt_{sym.lower()}"
        if tid != expected_id:
            errors.append(f"line {i}: target_id {tid!r} does not follow tgt_<lowercase symbol> convention (expected {expected_id!r})")

        tier = row["derisking_tier"]
        if tier not in DERISKING_TIERS:
            errors.append(f"line {i}: derisking_tier {tier!r} not in {DERISKING_TIERS}")

        status = row["repurposing_status"]
        if status not in REPURPOSING_STATUSES:
            errors.append(f"line {i}: repurposing_status {status!r} not in {REPURPOSING_STATUSES}")

        if tier in DEFAULT_ACTIVE_TIERS and status not in ("ACTIVE",):
            errors.append(
                f"line {i}: target_id {tid} has derisking_tier={tier} (defaults to ACTIVE per "
                f"ADC_ATLAS_DATASET_CONTRACT.md) but repurposing_status={status} -- if this is a "
                f"deliberate override, document why in notes"
            )
        if tier == "C_ANTIBODY_OR_BIOLOGY_ONLY" and status == "ACTIVE":
            errors.append(
                f"line {i}: target_id {tid} has derisking_tier=C_ANTIBODY_OR_BIOLOGY_ONLY, which "
                f"defaults to FUTURE, but repurposing_status=ACTIVE -- this needs an explicit "
                f"justification note (an internalizing antibody alone is not ADC derisking)"
            )

        for field in schema_header:
            if row[field].strip() == "":
                errors.append(f"line {i}: empty field {field!r} for target_id={tid} -- use UNKNOWN, not blank")

    if errors:
        for e in errors:
            print(f"FAIL: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Target seed validation passed: {len(rows)} targets, {len(seen_symbols)} unique symbols")


if __name__ == "__main__":
    main()
