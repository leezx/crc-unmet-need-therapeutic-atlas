#!/usr/bin/env python3
"""Regression tests for extract_hpa_cancer_ihc.py's row-loading and
cancer-type lookup. No real HPA download needed -- a tiny synthetic
cancer_data.tsv.zip fixture matching the real file's exact format
(Gene, Gene name, Cancer, High, Medium, Low, Not detected).

Usage: python3 scripts/test_extract_hpa_cancer_ihc.py
"""
import sys
import tempfile
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from extract_hpa_cancer_ihc import load_rows, TARGET_CANCER

failures = []


def check(label, cond):
    if not cond:
        failures.append(label)
        print(f"FAIL: {label}")
    else:
        print(f"ok: {label}")


check("TARGET_CANCER is the exact HPA category string", TARGET_CANCER == "colorectal cancer")

with tempfile.TemporaryDirectory() as tmp:
    zip_path = Path(tmp) / "cancer_data.tsv.zip"
    content = (
        "Gene\tGene name\tCancer\tHigh\tMedium\tLow\tNot detected\n"
        "ENSG00000105388\tCEACAM5\tbreast cancer\t0\t0\t0\t11\n"
        "ENSG00000105388\tCEACAM5\tcolorectal cancer\t6\t4\t0\t0\n"
        "ENSG00000105388\tCEACAM5\tstomach cancer\t6\t2\t2\t1\n"
        "ENSG00000141736\tERBB2\tcolorectal cancer\t0\t3\t2\t6\n"
    )
    with zipfile.ZipFile(zip_path, "w") as z:
        z.writestr("cancer_data.tsv", content)

    ceacam5_rows = load_rows(zip_path, "CEACAM5")
    check("load_rows returns all 3 CEACAM5 rows (all cancer types), not just colorectal",
          len(ceacam5_rows) == 3)
    check("load_rows does not accidentally match a different gene (ERBB2 excluded from CEACAM5 rows)",
          all(r["Gene name"] == "CEACAM5" for r in ceacam5_rows))

    crc_row = next(r for r in ceacam5_rows if r["Cancer"] == TARGET_CANCER)
    check("colorectal cancer row for CEACAM5 has the expected High/Medium/Low/NotDetected values",
          (crc_row["High"], crc_row["Medium"], crc_row["Low"], crc_row["Not detected"]) == ("6", "4", "0", "0"))

    erbb2_rows = load_rows(zip_path, "ERBB2")
    check("load_rows returns exactly 1 ERBB2 row (only colorectal cancer present in this fixture)",
          len(erbb2_rows) == 1)

    missing_rows = load_rows(zip_path, "NOTAGENE")
    check("load_rows returns an empty list for a gene symbol not in the file", missing_rows == [])

if failures:
    print(f"\n{len(failures)} test(s) FAILED: {failures}")
    sys.exit(1)
print("\nAll row-loading and cancer-type lookup regression tests passed.")
