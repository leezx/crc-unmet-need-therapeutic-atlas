#!/usr/bin/env python3
"""Regression tests for build_target_seed_universe.py's indication-string distillation.

No external sources needed -- pure unit tests on split_indications() / distill_cancer_types().
Added after web-ChatGPT review of PR #72 round 1 caught: (1) a negative-context indication
string ("... Excluding ... Colorectal Cancer") was being counted as CRC precedent by naive
substring match, (2) split(";") shredded a cytogenetic-notation label into garbage fragments,
(3) the CRC-priority cap wasn't actually capping total shown terms.

Usage: python3 scripts/test_build_target_seed_universe.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_target_seed_universe import distill_cancer_types, split_indications

failures = []


def check(label, cond):
    if not cond:
        failures.append(label)
        print(f"FAIL: {label}")
    else:
        print(f"ok: {label}")


# 1. A real positive CRC term is surfaced.
result = distill_cancer_types(["Colorectal Cancer; Breast Cancer"])
check("positive CRC term surfaced", "Colorectal Cancer" in result)

# 2. An explicit-exclusion term is never counted as positive precedent.
result = distill_cancer_types([
    "Part 2: HER2 Expressing/Amplified Solid Tumors Excluding Breast, Gastric, Colorectal Cancer"
])
check(
    "negative-context 'Excluding ... Colorectal Cancer' not shown as precedent",
    "Colorectal Cancer" not in result or "Excluding" in result,
)
# Stricter: the raw exclusion phrase should not appear re-labeled as a bare positive term.
check(
    "negative-context term does not appear as a bare 'Colorectal Cancer' entry",
    not any(t.strip() == "Colorectal Cancer" for t in result.split(";")),
)

# 3. A cytogenetic-notation label with internal semicolons/parens is not shredded.
raw = "Precursor B-Cell Lymphoblastic Leukemia-Lymphoma with t(9;22)(q34.1;q11.2); Breast Cancer"
terms = split_indications(raw)
check(
    "cytogenetic label kept intact, not split inside parens",
    any("t(9;22)(q34.1;q11.2)" in t for t in terms),
)
check("no garbage fragment like '22)(q34.1' produced", not any(t.strip().startswith("22)") for t in terms))

# 4. cap is a true total cap, including CRC-priority terms.
many_crc = "; ".join(f"Colorectal Cancer Variant {i}" for i in range(12))
result = distill_cancer_types([many_crc], cap=8)
shown = [t for t in result.split(" (+")[0].split(";") if t.strip()]
check(f"cap=8 enforced even when all terms are CRC-relevant (got {len(shown)})", len(shown) <= 8)
check("truncation note present when capped", "more distinct root terms" in result)

if failures:
    print(f"\n{len(failures)} test(s) FAILED: {failures}")
    sys.exit(1)
print("\nAll distillation regression tests passed.")
