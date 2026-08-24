#!/usr/bin/env python3
"""Regression tests for annotate_gse225857_tumor_cells.py's parsing, cell-ID
join, bucket logic, and metadata pre-flight validation. No real GEO data
needed -- synthetic gzip fixtures built in a temp directory, matching the
real files' exact format (quoted TSV, "." vs "-" cell-ID mismatch, Tu0N/
F0N/E0N cluster labels, predicted.doublet/doublet columns).

Extended after PR #81 round 1 review caught that validate_metadata()'s
three checks (cluster completeness, exact Tu01-Tu11 set, deposited-
doublet-filtering claim) were previously only asserted in the docstring,
not actually verified in code -- this file now exercises each check's
failure mode with a synthetic fixture built to trip it, using
contextlib.redirect_stderr + SystemExit to test the fail-closed sys.exit(1)
paths without spawning a subprocess.

Usage: python3 scripts/test_annotate_gse225857_tumor_cells.py
"""
import contextlib
import gzip
import io
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from annotate_gse225857_tumor_cells import (
    dequote, bucket, load_metadata, read_counts_header, find_gene_row, validate_metadata,
    EXPECTED_PATIENTS, EXPECTED_ORGANS,
)

failures = []


def check(label, cond):
    if not cond:
        failures.append(label)
        print(f"FAIL: {label}")
    else:
        print(f"ok: {label}")


def expect_exit(label, fn):
    """Runs fn() and checks it calls sys.exit(1) (validate_metadata's
    fail-closed path), swallowing the printed error output."""
    buf = io.StringIO()
    try:
        with contextlib.redirect_stderr(buf):
            fn()
        check(label, False)  # fn() returned normally -- should have exited
    except SystemExit as e:
        check(label, e.code == 1)


# --- dequote ---
check('dequote strips wrapping double quotes', dequote('"s0107_SampleTag06-1"') == "s0107_SampleTag06-1")
check('dequote leaves unquoted text alone', dequote("CEACAM5") == "CEACAM5")
check('dequote strips surrounding whitespace too', dequote('  "F3"  ') == "F3")

# --- bucket ---
check("bucket: exactly at RNA_no boundary (0.05) is NOT RNA_no (strict <)", bucket(0.05) == "RNA_low")
check("bucket: just under 0.05 is RNA_no", bucket(0.0499) == "RNA_no")
check("bucket: exactly at RNA_high boundary (0.50) is NOT RNA_high (strict >)", bucket(0.50) == "RNA_low")
check("bucket: just over 0.50 is RNA_high", bucket(0.5001) == "RNA_high")
check("bucket: None fraction -> NA", bucket(None) == "NA")


def write_meta_gz(path, rows, cluster_col="cluster"):
    """rows: list of (cell_id, patient, organ, cluster, predicted_doublet, doublet)."""
    with gzip.open(path, "wt") as f:
        f.write(f'""\t"patients"\t"organs"\t"{cluster_col}"\t"predicted.doublet"\t"doublet"\n')
        for cell_id, patient, organ, cluster, pd, d in rows:
            f.write(f'"{cell_id}"\t"{patient}"\t"{organ}"\t"{cluster}"\t"{pd}"\t"{d}"\n')


def write_counts_gz(path, cell_ids, gene_rows):
    """gene_rows: dict of gene_symbol -> list[int] (same length as cell_ids)."""
    with gzip.open(path, "wt") as f:
        header_ids = [cid.replace("-", ".") for cid in cell_ids]
        f.write('""\t' + "\t".join(f'"{h}"' for h in header_ids) + "\n")
        for gene, values in gene_rows.items():
            f.write(f'"{gene}"\t' + "\t".join(str(v) for v in values) + "\n")


# 11 Tu clusters (one cell each, to satisfy the exact-Tu01-Tu11 check) plus
# one fibroblast and one endothelial cell, all QC-clean (predicted.doublet=
# False, doublet=singlet), matching a real metadata file's expected shape.
# Patients/organs are spread across the real EXPECTED_PATIENTS/EXPECTED_ORGANS
# sets (not placeholder IDs) so this fixture is a genuine positive case for
# the patient-set/organ-set checks too, not just the cluster/doublet ones.
REAL_PATIENTS = sorted(EXPECTED_PATIENTS)  # s0107, s0115, s0813, s0920, s1231
REAL_ORGANS = sorted(EXPECTED_ORGANS)  # CCT, LCT
FULL_TUMOR_SET_ROWS = [
    (f"cellTu{i:02d}-1", REAL_PATIENTS[i % len(REAL_PATIENTS)], REAL_ORGANS[i % len(REAL_ORGANS)],
     f"Tu{i:02d}_MARKER{i}", "False", "singlet")
    for i in range(1, 12)
] + [
    ("cellF-1", REAL_PATIENTS[0], REAL_ORGANS[0], "F01_fibroblast_PRELP", "False", "singlet"),
    ("cellE-1", REAL_PATIENTS[1], REAL_ORGANS[1], "E01_endothelial_SELP", "False", "singlet"),
]
assert {r[1] for r in FULL_TUMOR_SET_ROWS} == EXPECTED_PATIENTS, "fixture must cover every expected patient"
assert {r[2] for r in FULL_TUMOR_SET_ROWS} == EXPECTED_ORGANS, "fixture must cover every expected organ"

# --- end-to-end on a tiny synthetic dataset ---
with tempfile.TemporaryDirectory() as tmp:
    tmp = Path(tmp)
    meta_path = tmp / "meta.txt.gz"
    counts_path = tmp / "counts.txt.gz"

    # 4 synthetic cells: 2 tumor (Tu01/Tu02), 1 fibroblast (F01), 1 endothelial (E01).
    # Metadata row names use "-"; counts header uses "." at the same position,
    # matching the real files' R write.table artifact.
    meta_rows = [
        ("cellA-1", "pX", "CCT", "Tu01_AREG", "False", "singlet"),
        ("cellA-2", "pX", "LCT", "Tu02_DEFA5", "False", "singlet"),
        ("cellA-3", "pX", "CCT", "F01_fibroblast_PRELP", "False", "singlet"),
        ("cellA-4", "pY", "LCT", "E01_endothelial_SELP", "False", "singlet"),
    ]
    write_meta_gz(meta_path, meta_rows)
    write_counts_gz(counts_path, [r[0] for r in meta_rows],
                     {"OTHERGENE": [0, 0, 0, 0], "TESTGENE": [3, 0, 5, 0]})

    meta = load_metadata(meta_path)
    check("load_metadata reads all 4 rows in file order", len(meta) == 4)
    check("load_metadata parses cluster column", meta[0][3] == "Tu01_AREG")
    check("load_metadata parses organ column", meta[1][2] == "LCT")
    check("load_metadata parses patient column", meta[3][1] == "pY")
    check("load_metadata parses predicted.doublet column", meta[0][4] == "False")
    check("load_metadata parses doublet column", meta[0][5] == "singlet")

    counts_ids = read_counts_header(counts_path)
    check("read_counts_header normalizes '.' back to '-'", counts_ids[0] == "cellA-1")
    check("read_counts_header preserves order", counts_ids == [r[0] for r in meta])

    gene_row = find_gene_row(counts_path, "TESTGENE")
    check("find_gene_row locates the correct row by exact symbol match", gene_row == [3, 0, 5, 0])
    check("find_gene_row returns None for a gene not present", find_gene_row(counts_path, "NOPE") is None)
    check("find_gene_row does not match a substring of another gene's name",
          find_gene_row(counts_path, "OTHER") is None)

    # Tumor-cell filter: only cellA-1 (Tu01) and cellA-2 (Tu02) should count as tumor.
    tumor_cell_ids = {row[0] for row in meta if row[3].startswith("Tu")}
    check("exactly 2 of 4 synthetic cells are tumor-cluster cells", len(tumor_cell_ids) == 2)
    check("fibroblast (cellA-3) and endothelial (cellA-4) cells are excluded from the tumor set",
          "cellA-3" not in tumor_cell_ids and "cellA-4" not in tumor_cell_ids)
    check("tumor-cluster cells are exactly cellA-1 and cellA-2",
          tumor_cell_ids == {"cellA-1", "cellA-2"})

    # Full pipeline sanity: among the 2 tumor cells, TESTGENE is positive in
    # cellA-1 (count=3) and zero in cellA-2 (count=0) -> 1/2 = 0.5 -> RNA_low
    # (0.50 is the strict-> boundary for RNA_high, not inclusive).
    tumor_counts = [count for row, count in zip(meta, gene_row) if row[0] in tumor_cell_ids]
    frac = sum(1 for c in tumor_counts if c > 0) / len(tumor_counts)
    check("TESTGENE detection fraction among tumor cells is exactly 0.5", frac == 0.5)
    check("0.5 buckets to RNA_low, not RNA_high (strict > boundary)", bucket(frac) == "RNA_low")

    # --- validate_metadata: this small 4-row fixture only has Tu01/Tu02 (not
    # the full Tu01-Tu11 set), so it must itself fail the exact-set check --
    # confirms the check is real, not a no-op.
    expect_exit("validate_metadata rejects a fixture missing most of Tu01-Tu11",
                lambda: validate_metadata(meta))

    # --- validate_metadata: full 13-row fixture (Tu01-Tu11 + F01 + E01, all
    # QC-clean) should pass cleanly.
    buf = io.StringIO()
    with contextlib.redirect_stderr(buf):
        validate_metadata(FULL_TUMOR_SET_ROWS)  # should not raise/exit
    check("validate_metadata passes on a complete, QC-clean Tu01-Tu11 fixture", True)

    # --- validate_metadata: empty cluster value on one row must fail closed.
    empty_cluster_rows = list(FULL_TUMOR_SET_ROWS)
    empty_cluster_rows[0] = (empty_cluster_rows[0][0], empty_cluster_rows[0][1],
                              empty_cluster_rows[0][2], "", "False", "singlet")
    expect_exit("validate_metadata rejects a fixture with one empty cluster value",
                lambda: validate_metadata(empty_cluster_rows))

    # --- validate_metadata: an unexpected extra tumor label (Tu12) must fail closed.
    extra_label_rows = list(FULL_TUMOR_SET_ROWS) + [
        ("cellTu12-1", REAL_PATIENTS[0], REAL_ORGANS[0], "Tu12_EXTRA", "False", "singlet")]
    expect_exit("validate_metadata rejects a fixture with an unexpected Tu12 label",
                lambda: validate_metadata(extra_label_rows))

    # --- validate_metadata: a predicted doublet (predicted.doublet=True) must fail closed.
    doublet_rows = list(FULL_TUMOR_SET_ROWS)
    doublet_rows[0] = (doublet_rows[0][0], doublet_rows[0][1], doublet_rows[0][2],
                        doublet_rows[0][3], "True", "doublet")
    expect_exit("validate_metadata rejects a fixture with a real predicted doublet",
                lambda: validate_metadata(doublet_rows))

    # --- validate_metadata: an unrecognized patient ID must fail closed (PR #81 round 2 review --
    # the round-1 fixture used placeholder pX/pY IDs that this check would not have caught).
    unknown_patient_rows = list(FULL_TUMOR_SET_ROWS)
    unknown_patient_rows[0] = ("cellUnknownPatient-1", "sUNKNOWN", unknown_patient_rows[0][2],
                                unknown_patient_rows[0][3], "False", "singlet")
    expect_exit("validate_metadata rejects a fixture with an unrecognized patient ID",
                lambda: validate_metadata(unknown_patient_rows))

    # --- validate_metadata: an unrecognized organ code must fail closed -- otherwise it would
    # silently fall through ORGAN_LABELS.get(organ, organ) in the main pipeline, uncaught.
    unknown_organ_rows = list(FULL_TUMOR_SET_ROWS)
    unknown_organ_rows[0] = ("cellUnknownOrgan-1", unknown_organ_rows[0][1], "PBT",
                              unknown_organ_rows[0][3], "False", "singlet")
    expect_exit("validate_metadata rejects a fixture with an unrecognized organ code",
                lambda: validate_metadata(unknown_organ_rows))

if failures:
    print(f"\n{len(failures)} test(s) FAILED: {failures}")
    sys.exit(1)
print("\nAll parsing, join, bucket, and metadata-validation regression tests passed.")
