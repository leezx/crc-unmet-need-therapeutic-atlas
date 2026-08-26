#!/usr/bin/env python3
"""Module D follow-up: does PXD055821's protein-group-level DIA-NN output
show any additional protein-group-level splitting or inference ambiguity
for the five A_CLINICAL targets, beyond the gene-group-level matrix
already used?

Context (Next-handoff item 3e(c)): this repository's Module D evidence
(TE032-TE036) is built from `220920_PN_CRC_LM_all_63_LM_DIANN.gg_matrix.tsv`
-- DIA-NN's gene-group-level intensity summary, one row per gene symbol.
DIA-NN separately outputs a protein-group-level matrix,
`220920_PN_CRC_LM_all_63_LM_DIANN.pg_matrix.tsv` (available from PRIDE,
same Sydney-cohort project, downloaded 2026-08-25 -- see
`DATA/registry/PXD055821/file_inventory.tsv`). Protein-group-level output
can differ from gene-group-level output when a gene maps to more than one
protein group within this DIA-NN output (additional group-level
splitting) or when a single protein group's peptides are shared across
more than one gene (multi-gene/multi-accession group ambiguity) -- in
either case, the gene-group summary would collapse information the
protein-group table keeps separate.

**What a clean result here does and does NOT establish (tightened round 1
review of PR #87, after an earlier version overclaimed this):** a target
mapping to exactly one single-accession protein group in this table means
only that this specific DIA-NN search/inference run found no additional
protein-group-level splitting or multi-gene/multi-accession ambiguity for
that target. It does NOT establish that the protein has no biological
isoforms or proteoforms -- an isoform not present in DIA-NN's search
database could not appear in this table regardless of protein-group vs.
gene-group granularity, and PTM-defined proteoforms are not separately
resolved by protein-group-level output either. This script never uses
the words "isoform" or "proteoform" to describe what it establishes; it
reports only "protein-group-level splitting/ambiguity in this DIA-NN
output" -- a narrower, actually-verified claim.

**Validation logic (tightened round 1 review of PR #87):** an earlier
version of this script only checked that a target appeared in exactly
one pg_matrix row and that row's values matched gg_matrix -- it never
checked whether that one row's own `Genes` field was shared with another
gene, or whether its `Protein.Group`/`Protein.Ids` fields carried more
than one accession (both are semicolon-delimited when DIA-NN considers
peptides ambiguous across proteins/genes). A row with
`Protein.Group=P00000;P00001` and `Genes=ERBB2;OTHER_GENE` would have
silently passed the old check. `validate_target()` below explicitly
requires: exactly one matching pg row; that row's `Genes` field splits to
exactly `[target]` (not shared with any other gene); its `Protein.Group`
field splits to exactly one accession; its `Protein.Ids` field also
splits to exactly one accession; and its 60 specimen values match
gg_matrix's row for that gene exactly (compared as the parsed string
values csv.reader returns -- not a byte-level file comparison, so this
script never claims "byte-identical", only "all N parsed value strings
match exactly"). Any one of these failing is reported as a failure for
that target, not silently passed through.

**Specimen-column alignment (tightened round 1 review of PR #87):** an
earlier version compared only value strings at matching list positions,
never checking that pg_matrix's and gg_matrix's specimen columns are
actually the same columns in the same order. This script now asserts the
two files' specimen header rows are identical (order included) before
comparing any values -- if a future re-run of either matrix reorders
columns, this fails closed instead of silently comparing mismatched
specimens.

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
PG_META_COLS = 5  # Protein.Group, Protein.Ids, Protein.Names, Genes, First.Protein.Description


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
    """Returns (specimen_header, {gene: [value strings]}) for the
    gene-group matrix."""
    with open(path, newline="") as f:
        reader = csv.reader(f, delimiter="\t")
        header = next(reader)
        specimen_header = header[1:]
        out = {}
        for row in reader:
            if row[0] in targets:
                out[row[0]] = row[1:]
    return specimen_header, out


def load_pg_rows(path, targets):
    """Returns (specimen_header, {gene: [(genes_list, protein_group_list,
    protein_ids_list, [value strings]), ...]}) -- a list per gene because
    a gene could in principle appear in more than one row, and each
    matching row's full Genes/Protein.Group/Protein.Ids splits are kept
    (not discarded) so callers can check for sharing/multi-accession
    ambiguity, not just row count."""
    out = {t: [] for t in targets}
    with open(path, newline="") as f:
        reader = csv.reader(f, delimiter="\t")
        header = next(reader)
        specimen_header = header[PG_META_COLS:]
        idx_genes = header.index("Genes")
        idx_pg = header.index("Protein.Group")
        idx_pids = header.index("Protein.Ids")
        for row in reader:
            genes_list = [g.strip() for g in row[idx_genes].split(";") if g.strip()]
            pg_list = [p.strip() for p in row[idx_pg].split(";") if p.strip()]
            pids_list = [p.strip() for p in row[idx_pids].split(";") if p.strip()]
            values = row[PG_META_COLS:]
            for t in targets:
                if t in genes_list:
                    out[t].append((genes_list, pg_list, pids_list, values))
    return specimen_header, out


def validate_target(gene, pg_matches, gg_values):
    """Pure function (no file I/O) so this logic is directly unit-testable.
    Returns (ok: bool, reason: str). Checks, in order: exactly one
    matching pg row; that row's Genes field is not shared with any other
    gene; its Protein.Group field is exactly one accession; its
    Protein.Ids field is exactly one accession; its 60 values match
    gg_values exactly (as parsed strings, not a byte-level comparison)."""
    if gg_values is None:
        return False, "missing from gg_matrix -- cannot compare"
    if len(pg_matches) != 1:
        return False, f"{len(pg_matches)} matching pg_matrix row(s), expected exactly 1"
    genes_list, pg_list, pids_list, pg_values = pg_matches[0]
    if genes_list != [gene]:
        return False, f"Genes field is shared: {genes_list} (not just {gene})"
    if len(pg_list) != 1:
        return False, f"Protein.Group has {len(pg_list)} accessions: {pg_list}"
    if len(pids_list) != 1:
        return False, f"Protein.Ids has {len(pids_list)} accessions: {pids_list}"
    if pg_values != gg_values:
        n_diff = sum(1 for a, b in zip(pg_values, gg_values) if a != b)
        return False, f"{n_diff}/{len(gg_values)} value strings differ from gg_matrix"
    return True, pg_list[0]


def main():
    gg_path = resolve_file(GG_MATRIX_FILE)
    pg_path = resolve_file(PG_MATRIX_FILE)

    gg_header, gg_rows = load_gg_rows(gg_path, A_CLINICAL_TARGETS)
    pg_header, pg_rows = load_pg_rows(pg_path, A_CLINICAL_TARGETS)

    if gg_header != pg_header:
        print("ERROR: gg_matrix and pg_matrix specimen columns are not identical "
              "(order included) -- refusing to compare target values across "
              "possibly-mismatched columns.", file=sys.stderr)
        sys.exit(1)
    if len(gg_header) != 60:
        print(f"ERROR: expected 60 specimen columns, found {len(gg_header)}.", file=sys.stderr)
        sys.exit(1)

    print(f"Specimen columns confirmed identical and in the same order across both "
          f"files ({len(gg_header)} columns).\n")
    print(f"{'gene':<10}{'n_pg_matches':<14}{'result':<12}{'protein_group_or_reason'}")
    any_failure = False
    for gene in A_CLINICAL_TARGETS:
        ok, detail = validate_target(gene, pg_rows.get(gene, []), gg_rows.get(gene))
        if not ok:
            any_failure = True
        print(f"{gene:<10}{len(pg_rows.get(gene, [])):<14}{'OK' if ok else 'FAIL':<12}{detail}")

    print()
    if any_failure:
        print("At least one target failed validation (shared Genes field, multi-accession "
              "Protein.Group/Protein.Ids, missing/duplicate pg_matrix row, or a value "
              "mismatch vs. gg_matrix) -- this needs investigation before treating the "
              "existing gg_matrix-based evidence rows as final for that target.", file=sys.stderr)
        sys.exit(1)
    print(f"No additional protein-group-level ambiguity is represented for these "
          f"{len(A_CLINICAL_TARGETS)} targets in this specific DIA-NN pg_matrix output "
          f"(no target's Genes field is shared with another gene; no target's "
          f"Protein.Group/Protein.Ids field carries more than one accession); all 60 "
          f"parsed value strings match the gg_matrix row already used in TE032-TE036 "
          f"exactly. This does not establish absence of biological isoforms/proteoforms "
          f"not separately represented by DIA-NN's own search/inference model.")


if __name__ == "__main__":
    main()
