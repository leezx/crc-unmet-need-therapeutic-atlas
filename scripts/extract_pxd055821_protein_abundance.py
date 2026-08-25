#!/usr/bin/env python3
"""Module D: PXD055821 tumor-tissue protein abundance for one target.

PXD055821 (152 CRC-LM specimens / 111 patients total, 3 proteomic
phenotypes, Mol Cell Proteomics 2025, DOI 10.1016/J.MCPRO.2025.101026) is
a Proteome Discoverer/DIA-NN mixed-search project. Most of its raw data
is either multi-GB .raw files or multi-GB .pdResult/.msf Proteome
Discoverer result files -- neither has a search engine available in this
environment and neither is reproduced or reprocessed here.

One DIA-NN output file is a small (3.48 MB), already-processed,
gene-symbol-indexed protein abundance matrix:
`220920_PN_CRC_LM_all_63_LM_DIANN.gg_matrix.tsv`. Its 60 columns
correspond to the publication's own "Sydney cohort" -- **60 CRC-LM
specimens collected from 51 patients**, independently confirmed by
fetching the publication's own full text (PMC12335997): "The third
cohort was from the tumor bank of the Kolling Institute, Royal North
Shore Hospital in Sydney, Australia and comprised 60 specimens
collected from 51 patients... samples of the third cohort were
processed and measured [by DIA-NN] at the Kolling Institute in
Australia." Some patients contributed more than one specimen (60 != 51)
-- the exact per-patient breakdown is not stated in the publication text
fetched here and is not resolved further. These are pathologist-selected
tumor-enriched regions, not raw whole-tissue sections. The filename says
"all_63_LM" but the matrix content has exactly 60 columns -- consistent
with the publication's stated Sydney-cohort size of 60 specimens
(independently confirmed in round-1 review of PR #82), so the "63" in
the filename is very likely stale/mismatched naming from an earlier
draft of the run, not an unexplained data-content gap; the reason for
the stale filename itself remains unresolved. This script reads that
file only; it does not touch the raw .raw/.pdResult/.msf files, which
remain unprocessed and are not claimed to contribute to this evidence.

**Columns are specimens, not independent patients** -- some of the 51
patients contributed more than one specimen/column (exact breakdown not
resolved). Column-to-patient mapping has not been reconstructed here
(the header only carries the original DIA-NN run file paths, e.g.
"H:\\Paula\\CRC_LM\\...\\220624_CRCLM_PN_S24.mzML", not patient IDs), so
every "n/60" figure this script reports is a specimen-level detection
fraction, not a patient-level prevalence and not "60 independent
patients" (round-1 review of PR #82 caught this exact overclaim).

Detection is defined as a genuinely nonzero, non-missing intensity value
-- a blank cell (missing) and a literal "0" value are both treated as
NOT detected, matching this script's own claim text ("detected =
nonzero intensity"). Round-1 review of PR #82 also caught that an
earlier version of this script's summarize_detection() only excluded
blank cells, silently counting a literal "0" as detected -- inconsistent
with its own claim text, though it happened not to change any of the
five targets' actual reported numbers (no observed value for any of
them is exactly zero).

This is whole-tissue (not malignant-cell-specific) mass-spec protein
abundance -- per this repository's own Module D contract
(modules/module_d_protein_and_endpoint/README.md), it does NOT
establish malignant-cell-specific membrane/surface density on its own.
evidence_directness stays UNCALIBRATED_PROXY.

Usage: python3 scripts/extract_pxd055821_protein_abundance.py --gene CEACAM5
"""
import argparse
import csv
import hashlib
import statistics
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = (
    REPO_ROOT / "modules" / "module_d_protein_and_endpoint"
    / "data_lock" / "raw" / "PXD055821"
)
MATRIX_FILE = "220920_PN_CRC_LM_all_63_LM_DIANN.gg_matrix.tsv"


def sha256(path):
    d = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            d.update(chunk)
    return d.hexdigest()


def summarize_detection(values):
    """A blank/whitespace-only string is missing (DIA-NN's own convention
    in this matrix); a genuinely nonzero parsed value is detected; a
    literal "0" is NOT detected -- matches this script's own claim text
    ("detected = nonzero intensity"). Returns (n_detected, n_total,
    fraction_detected, (median, min, max) or None -- computed over
    detected values only)."""
    detected = [f for f in (float(v) for v in values if v.strip()) if f != 0]
    n_detected = len(detected)
    n_total = len(values)
    frac = n_detected / n_total if n_total else None
    stats = (statistics.median(detected), min(detected), max(detected)) if detected else None
    return n_detected, n_total, frac, stats


def resolve_file():
    inventory_path = REPO_ROOT / "DATA" / "registry" / "PXD055821" / "file_inventory.tsv"
    if not inventory_path.is_file():
        print(f"ERROR: {inventory_path} not found.", file=sys.stderr)
        sys.exit(1)
    with open(inventory_path, newline="") as f:
        inventory = {r["file_name"]: r for r in csv.DictReader(f, delimiter="\t")}
    path = RAW_DIR / MATRIX_FILE
    if not path.is_file():
        print(f"ERROR: {path} not found.", file=sys.stderr)
        sys.exit(1)
    expected = inventory.get(MATRIX_FILE, {}).get("checksum", "").replace("sha256:", "")
    if not expected:
        print(f"ERROR: no checksum recorded for {MATRIX_FILE} in {inventory_path}.", file=sys.stderr)
        sys.exit(1)
    actual = sha256(path)
    if actual != expected:
        print(f"ERROR: checksum mismatch for {path}: inventory says {expected}, file is {actual}.", file=sys.stderr)
        sys.exit(1)
    return path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gene", required=True)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    gene = args.gene.strip()

    path = resolve_file()
    with open(path, newline="") as f:
        reader = csv.reader(f, delimiter="\t")
        header = next(reader)
        n_specimens = len(header) - 1
        target_row = None
        n_rows = 0
        for row in reader:
            n_rows += 1
            if row[0] == gene:
                target_row = row
    print(f"Matrix: {n_rows} genes x {n_specimens} specimen columns (Sydney cohort, "
          f"60 CRC-LM specimens from 51 patients).", file=sys.stderr)

    if target_row is None:
        print(f"ERROR: gene '{gene}' not found in {path.name} (checked exact-match on column 1, "
              f"{n_rows} gene rows scanned).", file=sys.stderr)
        sys.exit(1)

    values = target_row[1:]
    n_detected, _n_total, frac_detected, stats = summarize_detection(values)

    out_rows = []
    for sample_path, v in zip(header[1:], values):
        out_rows.append({"specimen_run_path": sample_path, "value": v if v.strip() else "NA"})

    out_path = Path(args.out) if args.out else (
        REPO_ROOT / "modules" / "module_d_protein_and_endpoint" / "results"
        / f"tgt_{gene.lower()}_pxd055821_protein_abundance.tsv"
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["specimen_run_path", "value"], delimiter="\t")
        w.writeheader()
        for r in out_rows:
            w.writerow(r)

    print(f"\nWrote {len(out_rows)} specimen rows to {out_path}")
    if stats:
        median, lo, hi = stats
        print(f"\n{gene} protein abundance (DIA-NN gene-group intensity, arbitrary units) across "
              f"{n_specimens} specimens (Sydney cohort, 51 patients, some contributing >1 specimen -- "
              f"column-to-patient mapping not reconstructed here): detected in "
              f"{n_detected}/{n_specimens} specimens ({frac_detected:.1%}); "
              f"median={median:.4g}, min={lo:.4g}, max={hi:.4g}.")
    else:
        print(f"\n{gene}: detected in 0/{n_specimens} specimens.")


if __name__ == "__main__":
    main()
