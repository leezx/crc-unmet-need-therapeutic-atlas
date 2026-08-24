#!/usr/bin/env python3
"""Module B: GSE225857 non-immune (tumor) prevalence screen for one target.

Per PR #79's reviewer-specified next step, taken after confirming (this
script's --verify-only mode, and PR #80/#81's review): (1) cell IDs in
GSM7058755_non_immune_counts.txt.gz join 1:1, in the same row order, to
GSM7058755_non_immune_meta.txt.gz's row names after normalizing the
counts header's "." back to "-" (an R syntactic-name artifact -- write.table
substitutes "." for "-" in column names by default); (2) all five
A_CLINICAL targets (CEACAM5, ERBB2, F3, NECTIN4, TACSTD2) are present in
the gene index under their canonical symbols, no alias needed (unlike
GSE178318, which required PVRL4 for NECTIN4); (3) the metadata's own
`cluster` column already carries real author-provided cell-type labels
(11 distinct `Tu01`-`Tu11` tumor clusters, exactly matching the source
publication's stated "11 tumor cell clusters"; Wang et al., Sci Adv 2023,
PMID 37327339), 100% populated across all 41,892 cells, with
predicted.doublet=False / doublet=singlet already true for every cell
(this is the paper's own deposited, already-QC'd/doublet-filtered release
-- no additional QC filtering is applied here, unlike GSE178318's raw,
unfiltered barcode deposit).

This is a materially stronger starting point than GSE178318's screen:
tumor-cell identity here is the source publication's own validated
cluster call (11/11 tumor clusters present, cell counts consistent with
the paper), not a single-gene EPCAM proxy invented because no author
annotation existed. It is still an RNA detection-fraction read, not a
protein/surface-density measurement -- evidence_directness stays
UNCALIBRATED_PROXY, same measurement_layer convention as GSE178318's
TE004/TE005.

File format note: GSM7058755_non_immune_counts.txt.gz is a dense,
gene-by-cell TSV (17,515 gene rows x 41,892 cell columns, quoted
strings), not GSE178318's sparse Matrix Market format. This script reads
the header once, then streams line-by-line looking only for the one row
whose first field matches --gene (an O(n_genes) scan, not a full-matrix
load -- the file is never materialized in memory as a matrix).

Every patient in this dataset is uniformly CHEMOTHERAPY_AND_OR_RT_PREOPERATIVE
(GSE225857's own registry-level treatment_annotation) -- no treated/
treatment-naive split is needed, unlike GSE178318. Organs in this file
are CC (primary colorectal cancer) and LC (liver metastasis), both
under indication_id=mcrc_preop_chemotherapy_crlm (its anatomy field is
explicitly PRIMARY_AND_LIVER_METASTASIS).

Usage: python3 scripts/annotate_gse225857_tumor_cells.py --gene CEACAM5
"""
import argparse
import csv
import gzip
import hashlib
import sys
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = (
    REPO_ROOT / "modules" / "module_b_mcrc_target_prevalence"
    / "data_lock" / "raw" / "GSE225857"
)
META_FILE = "GSM7058755_non_immune_meta.txt.gz"
COUNTS_FILE = "GSM7058755_non_immune_counts.txt.gz"

TUMOR_CLUSTER_PREFIX = "Tu"
ORGAN_LABELS = {"CCT": "CC_primary", "LCT": "LC_liver_metastasis"}

RNA_NO_MAX = 0.05
RNA_HIGH_MIN = 0.50


def sha256(path):
    d = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            d.update(chunk)
    return d.hexdigest()


def resolve_files():
    inventory_path = REPO_ROOT / "DATA" / "registry" / "GSE225857" / "file_inventory.tsv"
    if not inventory_path.is_file():
        print(f"ERROR: {inventory_path} not found.", file=sys.stderr)
        sys.exit(1)
    with open(inventory_path, newline="") as f:
        inventory = {r["file_name"]: r for r in csv.DictReader(f, delimiter="\t")}
    files = {}
    for fname in (META_FILE, COUNTS_FILE):
        path = RAW_DIR / fname
        if not path.is_file():
            print(f"ERROR: {path} not found.", file=sys.stderr)
            sys.exit(1)
        expected = inventory.get(fname, {}).get("checksum", "").replace("sha256:", "")
        if not expected:
            print(f"ERROR: no checksum recorded for {fname} in {inventory_path}.", file=sys.stderr)
            sys.exit(1)
        actual = sha256(path)
        if actual != expected:
            print(f"ERROR: checksum mismatch for {path}: inventory says {expected}, file is {actual}.", file=sys.stderr)
            sys.exit(1)
        files[fname] = path
    return files


def dequote(s):
    return s.strip().strip('"')


def load_metadata(path):
    """Returns an ordered list of (cell_id, patient, organ, cluster) — the
    same row order as the file itself, which this script's own join
    verification (below) proves is identical to the counts file's column
    order."""
    rows = []
    with gzip.open(path, "rt", newline="") as f:
        reader = csv.reader(f, delimiter="\t")
        header = [dequote(h) for h in next(reader)]
        idx = {name: i for i, name in enumerate(header)}
        for name in ("patients", "organs", "cluster"):
            if name not in idx:
                print(f"ERROR: expected column '{name}' not found in {path} header: {header}", file=sys.stderr)
                sys.exit(1)
        for row in reader:
            cell_id = dequote(row[0])
            patient = dequote(row[idx["patients"]])
            organ = dequote(row[idx["organs"]])
            cluster = dequote(row[idx["cluster"]])
            rows.append((cell_id, patient, organ, cluster))
    return rows


def read_counts_header(path):
    with gzip.open(path, "rt", newline="") as f:
        header_line = f.readline().rstrip("\n\r")
    fields = header_line.split("\t")
    # fields[0] is the blank row-label header column; fields[1:] are cell IDs.
    # R's write.table substitutes "." for "-" when making syntactic column
    # names -- normalize back to match the metadata file's row names.
    return [dequote(c).replace(".", "-") for c in fields[1:]]


def find_gene_row(path, gene):
    with gzip.open(path, "rt", newline="") as f:
        f.readline()  # header, already read separately
        for line in f:
            tab = line.find("\t")
            if tab == -1:
                continue
            row_gene = dequote(line[:tab])
            if row_gene == gene:
                values = line.rstrip("\n\r").split("\t")[1:]
                return [int(float(v)) for v in values]
    return None


def bucket(frac):
    if frac is None:
        return "NA"
    if frac < RNA_NO_MAX:
        return "RNA_no"
    if frac > RNA_HIGH_MIN:
        return "RNA_high"
    return "RNA_low"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gene", required=True)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    gene = args.gene.strip()

    files = resolve_files()
    meta_rows = load_metadata(files[META_FILE])
    print(f"Loaded {len(meta_rows)} metadata rows.", file=sys.stderr)

    counts_cell_ids = read_counts_header(files[COUNTS_FILE])
    if len(counts_cell_ids) != len(meta_rows):
        print(f"ERROR: counts file has {len(counts_cell_ids)} cell columns, "
              f"metadata has {len(meta_rows)} rows.", file=sys.stderr)
        sys.exit(1)
    meta_cell_ids = [r[0] for r in meta_rows]
    if counts_cell_ids != meta_cell_ids:
        mismatches = sum(1 for a, b in zip(counts_cell_ids, meta_cell_ids) if a != b)
        print(f"ERROR: counts-file cell-ID order does not match metadata row order "
              f"({mismatches} positional mismatches). Cannot assume positional join.", file=sys.stderr)
        sys.exit(1)
    print(f"Verified: {len(counts_cell_ids)}/{len(counts_cell_ids)} cell IDs join 1:1 "
          f"in identical order between counts and metadata.", file=sys.stderr)

    print(f"Scanning {files[COUNTS_FILE]} for gene row '{gene}'...", file=sys.stderr)
    target_counts = find_gene_row(files[COUNTS_FILE], gene)
    if target_counts is None:
        print(f"ERROR: target gene '{gene}' not found in gene index.", file=sys.stderr)
        sys.exit(1)
    if len(target_counts) != len(meta_rows):
        print(f"ERROR: gene row for '{gene}' has {len(target_counts)} values, "
              f"expected {len(meta_rows)}.", file=sys.stderr)
        sys.exit(1)
    print(f"Found '{gene}' row; {sum(1 for c in target_counts if c > 0)} of "
          f"{len(target_counts)} cells (all clusters) have nonzero counts.", file=sys.stderr)

    per_group = defaultdict(lambda: {"n_tumor_cells": 0, "n_positive": 0})
    n_tumor_total = 0
    for (cell_id, patient, organ, cluster), count in zip(meta_rows, target_counts):
        if not cluster.startswith(TUMOR_CLUSTER_PREFIX):
            continue
        n_tumor_total += 1
        key = (patient, organ)
        per_group[key]["n_tumor_cells"] += 1
        if count > 0:
            per_group[key]["n_positive"] += 1

    print(f"Tumor-cluster cells (all {TUMOR_CLUSTER_PREFIX}0N labels): {n_tumor_total} of {len(meta_rows)}.", file=sys.stderr)

    out_rows = []
    for (patient, organ), s in sorted(per_group.items()):
        frac = (s["n_positive"] / s["n_tumor_cells"]) if s["n_tumor_cells"] else None
        out_rows.append({
            "patient_id": patient,
            "organ_code": organ,
            "organ_label": ORGAN_LABELS.get(organ, organ),
            "n_tumor_cells": s["n_tumor_cells"],
            f"{gene}_positive_cells": s["n_positive"],
            f"{gene}_positive_fraction_in_tumor_cells": round(frac, 4) if frac is not None else "NA",
            f"{gene}_bucket": bucket(frac),
        })

    out_path = Path(args.out) if args.out else (
        REPO_ROOT / "modules" / "module_b_mcrc_target_prevalence" / "results"
        / f"tgt_{gene.lower()}_gse225857_tumor_cell_prevalence.tsv"
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(out_rows[0].keys())
    with open(out_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t")
        w.writeheader()
        for r in out_rows:
            w.writerow(r)

    print(f"\nWrote {len(out_rows)} patient x organ rows to {out_path}")
    print(f"\nPer-patient x organ summary for {gene} (GSE225857 non-immune tumor-cell screen, "
          f"author-defined Tu0N clusters, all patients preoperative-chemo/RT-treated):")
    for r in out_rows:
        print(f"  {r['patient_id']:8s} {r['organ_label']:20s} n_tumor={r['n_tumor_cells']:5d}  "
              f"{gene}+_frac={r[f'{gene}_positive_fraction_in_tumor_cells']}  bucket={r[f'{gene}_bucket']}")


if __name__ == "__main__":
    main()
