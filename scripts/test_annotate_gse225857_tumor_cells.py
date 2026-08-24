#!/usr/bin/env python3
"""Regression tests for annotate_gse225857_tumor_cells.py's parsing, cell-ID
join, and bucket logic. No real GEO data needed -- synthetic gzip fixtures
built in a temp directory, matching the real files' exact format (quoted
TSV, "." vs "-" cell-ID mismatch, Tu0N/F0N/E0N cluster labels).

Usage: python3 scripts/test_annotate_gse225857_tumor_cells.py
"""
import gzip
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from annotate_gse225857_tumor_cells import dequote, bucket, load_metadata, read_counts_header, find_gene_row

failures = []


def check(label, cond):
    if not cond:
        failures.append(label)
        print(f"FAIL: {label}")
    else:
        print(f"ok: {label}")


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

# --- end-to-end on a tiny synthetic dataset ---
with tempfile.TemporaryDirectory() as tmp:
    tmp = Path(tmp)
    meta_path = tmp / "meta.txt.gz"
    counts_path = tmp / "counts.txt.gz"

    # 4 synthetic cells: 2 tumor (Tu01/Tu02), 1 fibroblast (F01), 1 endothelial (E01).
    # Metadata row names use "-"; counts header uses "." at the same position,
    # matching the real files' R write.table artifact.
    meta_rows = [
        ("cellA-1", "pX", "CCT", "Tu01_AREG"),
        ("cellA-2", "pX", "LCT", "Tu02_DEFA5"),
        ("cellA-3", "pX", "CCT", "F01_fibroblast_PRELP"),
        ("cellA-4", "pY", "LCT", "E01_endothelial_SELP"),
    ]
    with gzip.open(meta_path, "wt") as f:
        f.write('""\t"patients"\t"organs"\t"cluster"\n')
        for cell_id, patient, organ, cluster in meta_rows:
            f.write(f'"{cell_id}"\t"{patient}"\t"{organ}"\t"{cluster}"\n')

    # Target gene "TESTGENE" positive in cellA-1 and cellA-3, zero elsewhere.
    with gzip.open(counts_path, "wt") as f:
        header_ids = [cid.replace("-", ".") for cid, _, _, _ in meta_rows]
        f.write('""\t' + "\t".join(f'"{h}"' for h in header_ids) + "\n")
        f.write('"OTHERGENE"\t0\t0\t0\t0\n')
        f.write('"TESTGENE"\t3\t0\t5\t0\n')

    meta = load_metadata(meta_path)
    check("load_metadata reads all 4 rows in file order", len(meta) == 4)
    check("load_metadata parses cluster column", meta[0][3] == "Tu01_AREG")
    check("load_metadata parses organ column", meta[1][2] == "LCT")
    check("load_metadata parses patient column", meta[3][1] == "pY")

    counts_ids = read_counts_header(counts_path)
    check("read_counts_header normalizes '.' back to '-'", counts_ids[0] == "cellA-1")
    check("read_counts_header preserves order", counts_ids == [r[0] for r in meta])

    gene_row = find_gene_row(counts_path, "TESTGENE")
    check("find_gene_row locates the correct row by exact symbol match", gene_row == [3, 0, 5, 0])
    check("find_gene_row returns None for a gene not present", find_gene_row(counts_path, "NOPE") is None)
    check("find_gene_row does not match a substring of another gene's name",
          find_gene_row(counts_path, "OTHER") is None)

    # Tumor-cell filter: only cellA-1 (Tu01) and cellA-2 (Tu02) should count as tumor.
    tumor_cell_ids = {cid for cid, patient, organ, cluster in meta if cluster.startswith("Tu")}
    check("exactly 2 of 4 synthetic cells are tumor-cluster cells", len(tumor_cell_ids) == 2)
    check("fibroblast (cellA-3) and endothelial (cellA-4) cells are excluded from the tumor set",
          "cellA-3" not in tumor_cell_ids and "cellA-4" not in tumor_cell_ids)
    check("tumor-cluster cells are exactly cellA-1 and cellA-2",
          tumor_cell_ids == {"cellA-1", "cellA-2"})

    # Full pipeline sanity: among the 2 tumor cells, TESTGENE is positive in
    # cellA-1 (count=3) and zero in cellA-2 (count=0) -> 1/2 = 0.5 -> RNA_low
    # (0.50 is the strict-> boundary for RNA_high, not inclusive).
    tumor_counts = [count for (cid, *_), count in zip(meta, gene_row) if cid in tumor_cell_ids]
    frac = sum(1 for c in tumor_counts if c > 0) / len(tumor_counts)
    check("TESTGENE detection fraction among tumor cells is exactly 0.5", frac == 0.5)
    check("0.5 buckets to RNA_low, not RNA_high (strict > boundary)", bucket(frac) == "RNA_low")

if failures:
    print(f"\n{len(failures)} test(s) FAILED: {failures}")
    sys.exit(1)
print("\nAll parsing, join, and bucket regression tests passed.")
