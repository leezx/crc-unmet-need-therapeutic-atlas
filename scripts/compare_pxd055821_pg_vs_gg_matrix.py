#!/usr/bin/env python3
"""Module D follow-up: does PXD055821's protein-group-level DIA-NN output
add anything beyond the gene-group-level matrix already used for the
five A_CLINICAL targets?

Context (Next-handoff item 3e(c)): this repository's Module D evidence
(TE032-TE036) is built from `220920_PN_CRC_LM_all_63_LM_DIANN.gg_matrix.tsv`
-- DIA-NN's gene-group-level intensity summary, one row per gene symbol.
DIA-NN separately outputs a protein-group-level matrix,
`220920_PN_CRC_LM_all_63_LM_DIANN.pg_matrix.tsv` (available from PRIDE,
same Sydney-cohort project, not previously downloaded -- see
`DATA/registry/PXD055821/file_inventory.tsv`). Protein-group-level output
can differ from gene-group-level output when a gene maps to more than one
protein group (isoform/proteoform-level splitting) or when a single
protein group's peptides are shared across more than one gene (protein-
inference ambiguity) -- in either case, the gene-group summary would
collapse information the protein-group table keeps separate.

This script checks, for the five A_CLINICAL targets only (this
repository's actual evidence scope; it does not attempt to resess DIA-NN's
protein inference for the other ~9,250 genes in the matrix): whether each
target maps to exactly one protein group in the pg_matrix, and whether
that protein group's 60 specimen values match the gg_matrix row already
used, exactly.

This is a confirmatory check, not a new evidence source in its own
right -- if the two matrices agree (which they do, verified 2026-08-25:
each of the five targets maps to exactly one single-UniProt-accession
protein group, no other gene sharing it, and all 60 specimen values are
byte-identical to the gg_matrix), it means there is no protein-inference
ambiguity for these five targets specifically to worry about, and no
correction to TE032-TE036's already-recorded values is needed. It does
NOT mean DIA-NN's protein inference is unambiguous for the rest of the
9,263-gene matrix (not checked here), and it does NOT add any new
numeric evidence -- if this script ever finds a disagreement for a
future target, that would need investigation before use, not silent
preference for either file.

Usage: python3 scripts/compare_pxd055821_pg_vs_gg_matrix.py
"""
import csv
import hashlib
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
GG_MATRIX_FILE = "220920_PN_CRC_LM_all_63_LM_DIANN.gg_matrix.tsv"
PG_MATRIX_FILE = "220920_PN_CRC_LM_all_63_LM_DIANN.pg_matrix.tsv"
RAW_DIR = (
    REPO_ROOT / "modules" / "module_d_protein_and_endpoint"
    / "data_lock" / "raw" / "PXD055821"
)
A_CLINICAL_TARGETS = ["CEACAM5", "ERBB2", "F3", "NECTIN4", "TACSTD2"]


def sha256(path):
    d = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            d.update(chunk)
    return d.hexdigest()


def resolve_file(file_name):
    inventory_path = REPO_ROOT / "DATA" / "registry" / "PXD055821" / "file_inventory.tsv"
    if not inventory_path.is_file():
        print(f"ERROR: {inventory_path} not found.", file=sys.stderr)
        sys.exit(1)
    with open(inventory_path, newline="") as f:
        inventory = {r["file_name"]: r for r in csv.DictReader(f, delimiter="\t")}
    path = RAW_DIR / file_name
    if not path.is_file():
        print(f"ERROR: {path} not found.", file=sys.stderr)
        sys.exit(1)
    expected = inventory.get(file_name, {}).get("checksum", "").replace("sha256:", "")
    if not expected:
        print(f"ERROR: no checksum recorded for {file_name} in {inventory_path}.", file=sys.stderr)
        sys.exit(1)
    actual = sha256(path)
    if actual != expected:
        print(f"ERROR: checksum mismatch for {path}: inventory says {expected}, file is {actual}.", file=sys.stderr)
        sys.exit(1)
    return path


def load_gg_rows(path, targets):
    """Returns {gene: [60 raw value strings]} for the gene-group matrix."""
    out = {}
    with open(path, newline="") as f:
        reader = csv.reader(f, delimiter="\t")
        next(reader)  # header
        for row in reader:
            if row[0] in targets:
                out[row[0]] = row[1:]
    return out


def load_pg_rows(path, targets):
    """Returns {gene: [(protein_group, protein_ids, [60 raw value strings])]}
    -- a list per gene because a gene could in principle map to more than
    one protein group (checked, not assumed away)."""
    out = {t: [] for t in targets}
    with open(path, newline="") as f:
        reader = csv.reader(f, delimiter="\t")
        header = next(reader)
        idx_genes = header.index("Genes")
        idx_pg = header.index("Protein.Group")
        idx_pids = header.index("Protein.Ids")
        n_meta_cols = 5  # Protein.Group, Protein.Ids, Protein.Names, Genes, First.Protein.Description
        for row in reader:
            genes_field = row[idx_genes]
            genes_list = [g.strip() for g in genes_field.split(";") if g.strip()]
            for t in targets:
                if t in genes_list:
                    out[t].append((row[idx_pg], row[idx_pids], row[n_meta_cols:]))
    return out


def main():
    gg_path = resolve_file(GG_MATRIX_FILE)
    pg_path = resolve_file(PG_MATRIX_FILE)

    gg_rows = load_gg_rows(gg_path, A_CLINICAL_TARGETS)
    pg_rows = load_pg_rows(pg_path, A_CLINICAL_TARGETS)

    print(f"{'gene':<10}{'n_protein_groups':<18}{'protein_group':<16}{'values_match_gg':<18}")
    any_mismatch = False
    for gene in A_CLINICAL_TARGETS:
        groups = pg_rows.get(gene, [])
        gg_values = gg_rows.get(gene)
        if gg_values is None:
            print(f"{gene}: MISSING from gg_matrix -- cannot compare.", file=sys.stderr)
            any_mismatch = True
            continue
        if len(groups) != 1:
            print(f"{gene:<10}{len(groups):<18}{'AMBIGUOUS' if groups else 'NONE':<16}{'N/A':<18}")
            any_mismatch = True
            continue
        pg_id, protein_ids, pg_values = groups[0]
        match = pg_values == gg_values
        if not match:
            any_mismatch = True
        print(f"{gene:<10}{len(groups):<18}{pg_id:<16}{str(match):<18}")

    print()
    if any_mismatch:
        print("At least one target has an ambiguous protein-group mapping or a "
              "value mismatch between pg_matrix and gg_matrix -- this needs "
              "investigation before treating the existing gg_matrix-based "
              "evidence rows as final for that target.", file=sys.stderr)
        sys.exit(1)
    print(f"All {len(A_CLINICAL_TARGETS)} A_CLINICAL targets map to exactly one "
          f"single-protein protein-group in pg_matrix, and all 60 specimen "
          f"values are byte-identical to the gg_matrix row already used in "
          f"TE032-TE036. No protein-inference ambiguity for these five "
          f"targets; no correction needed to existing evidence.")


if __name__ == "__main__":
    main()
