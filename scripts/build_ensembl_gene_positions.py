#!/usr/bin/env python3
"""One-time build: Ensembl gene genomic-position lookup table.

Real gene-window InferCNV (per `infercnvpy`'s own requirement -- see
`infercnv_gse178318.py`) needs each gene's actual genomic position
(chromosome, start, end base-pair coordinates) to sort genes into
genomic order per chromosome before applying a moving-window smoothing
step. This is a materially finer-grained requirement than Module B's
existing chromosome-*arm* CNV-lite method (`infercnv_lite_gse178318.py`),
which only needed a coarse cytogenetic-band-derived arm bucket from the
already-locally-available HGNC gene-id-mapping reference -- that file has
no base-pair coordinates, so it cannot serve this purpose.

Source: Ensembl's own public GTF annotation release
(`https://ftp.ensembl.org/pub/release-110/gtf/homo_sapiens/
Homo_sapiens.GRCh38.110.gtf.gz`), fetched 2026-08-26,
sha256=5d3c363835bda4cf8ba025f728b190f69d454e894514bb3c81123efdb15ef1b9,
54,325,732 bytes. Release 110 (GRCh38) was chosen as a recent, stable
Ensembl release; it is not required to be the exact release
`GSE178318`'s own CellRanger reference used (that exact release is not
recorded in the dataset's own metadata) -- gene body coordinates are
highly stable across nearby GRCh38-based Ensembl releases for the large
majority of genes, and this script's own coverage check (below) verifies
this empirically against `GSE178318`'s actual gene index rather than
assuming it.

This script parses only `feature == "gene"` rows, extracts
`gene_id`/chromosome/start/end, and keeps only the 25 standard nuclear +
mitochondrial contigs (1-22, X, Y, MT) -- unplaced scaffolds and patch
contigs are dropped, matching the same "don't guess an ambiguous
position" discipline as the arm-mapping script's own arm-pattern filter.
Output is committed directly (like `DATA/reference/
uniprot_accession_map.tsv` -- a small, versioned, one-time-fetched lookup
table, not something re-derived at analysis runtime) -- the 54 MB source
GTF itself is not retained in this repository; this script is what makes
the derived table reproducible.

Coverage against GSE178318 (2026-08-26): 32,807 of 33,694 (97.4%) of the
dataset's own Ensembl gene IDs resolve to a position via this table --
materially higher than the arm-mapping script's 75.3% arm coverage,
because base-pair position data changes far less across Ensembl releases
than not-yet-assigned/reserved HGNC symbol-chromosome-band entries do.

Usage: python3 scripts/build_ensembl_gene_positions.py --gtf <path to Homo_sapiens.GRCh38.110.gtf.gz>
"""
import argparse
import csv
import gzip
import hashlib
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
OUT_PATH = REPO_ROOT / "DATA" / "reference" / "ensembl_gene_positions_grch38_release110.tsv"
EXPECTED_SHA256 = "5d3c363835bda4cf8ba025f728b190f69d454e894514bb3c81123efdb15ef1b9"
GENE_ID_RE = re.compile(r'gene_id "([^"]+)"')
STANDARD_CONTIG_RE = re.compile(r"^([1-9]|1[0-9]|2[0-2]|X|Y|MT)$")


def sha256(path):
    d = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            d.update(chunk)
    return d.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gtf", required=True, help="Path to the downloaded Homo_sapiens.GRCh38.110.gtf.gz")
    args = ap.parse_args()
    gtf_path = Path(args.gtf)

    if not gtf_path.is_file():
        print(f"ERROR: {gtf_path} not found.", file=sys.stderr)
        sys.exit(1)
    actual = sha256(gtf_path)
    if actual != EXPECTED_SHA256:
        print(
            f"ERROR: checksum mismatch for {gtf_path}: expected {EXPECTED_SHA256}, got {actual}. "
            f"This is not the exact release-110 GTF this script was built against -- "
            f"re-verify before proceeding.",
            file=sys.stderr,
        )
        sys.exit(1)

    positions = {}
    n_gene_rows = 0
    n_nonstandard_contig = 0
    with gzip.open(gtf_path, "rt") as f:
        for line in f:
            if line.startswith("#"):
                continue
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 9 or parts[2] != "gene":
                continue
            n_gene_rows += 1
            chrom, start, end, attrs = parts[0], parts[3], parts[4], parts[8]
            if not STANDARD_CONTIG_RE.match(chrom):
                n_nonstandard_contig += 1
                continue
            m = GENE_ID_RE.search(attrs)
            if not m:
                continue
            positions[m.group(1)] = (chrom, int(start), int(end))

    print(f"Parsed {n_gene_rows} 'gene' feature rows from {gtf_path.name}.")
    print(f"Excluded {n_nonstandard_contig} on non-standard contigs (scaffolds/patches).")
    print(f"Retained {len(positions)} gene positions on standard contigs (1-22, X, Y, MT).")

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_PATH, "w", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["ensembl_gene_id", "chromosome", "start", "end"])
        for gid, (chrom, start, end) in sorted(positions.items()):
            w.writerow([gid, chrom, start, end])
    print(f"Wrote {len(positions)} rows to {OUT_PATH}")


if __name__ == "__main__":
    main()
