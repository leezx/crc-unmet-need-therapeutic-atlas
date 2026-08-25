#!/usr/bin/env python3
"""Module D: MCRC_liver_metastasis_PDO_2026 multiplex-IHC protein
expression for one target.

MCRC_liver_metastasis_PDO_2026 (Kryeziu, Sveen, Lothe et al. 2026,
"Patient-derived organoids from metastatic colorectal cancer mirror
tumor heterogeneity and predict patient survival and drug sensitivity",
Mendeley Data v3, doi:10.17632/hr94h42xdc.3; publication PMC13293968) is
a living biobank of 213 CRC liver-metastasis (CRLM) patient-derived
organoids (PDOs) from 102 patients. Its Data S3.xlsx is a small
(114.6 KB), source-provided *processed* multiplex-fluorescent-IHC
(mIHC) table -- not a raw measurement: one row per PDO x protein-marker
x staining-round, with a continuous `mean_express_PDO` value (mean
relative fluorescence intensity per PDO image, already normalized to
total cellular content by the source authors -- not a raw pixel count
and not a High/Medium/Low/Not-detected category).

Per the source publication's own methods text (independently fetched
and confirmed 2026-08-25, PR #84 round 1 review): "Fluorescence-based
multiplex immunohistochemistry and digital image analyses were used to
analyze in situ expression of fourteen proteins in 136 PDOs and two
corresponding tumor tissue samples from 67 patients." Only `ERBB2` (of
this repository's five `A_CLINICAL` targets) is among those fourteen
markers.

*** IMPORTANT CAVEAT, not a formality -- and precisely worded, not
upgraded past what the source publication actually says: the source
publication's own methods text states, verbatim: "KRT7 and ERBB2 were
excluded from analysis due to no or very low expression levels,
respectively." Per that "respectively": `KRT7` was excluded for NO
expression; `ERBB2` was excluded for VERY LOW expression -- a real
distinction this script's own EXCLUDED_MARKERS dict preserves (round 1
review of PR #84 caught an earlier version collapsing both markers to
the same "no or very low" string, erasing "respectively").

The 136 per-PDO `ERBB2` values are still present in Data S3.xlsx and are
what this script reports (unmodified). **This repository does not claim
those values represent unreliable measurements, a failed reagent, or
assay noise** -- the source publication says only that the measured
expression was very low, not that the assay/antibody malfunctioned.
**This repository cannot determine, from what the source publication
states, whether this reflects genuinely low ERBB2 protein abundance in
these PDOs, limited sensitivity/performance of this specific multiplex
assay configuration (polyclonal antibody, catalog A0485), or both** --
and does not resolve that ambiguity by guessing. (Elsewhere in the same
publication, a *different* ERBB2 antibody clone, single-plex DAB IHC,
clone CB11, was used for a single-patient case-report figure -- Pt137,
a patient later found to have ERBB2-amplified, heterogeneously
expressed tumors -- but that one patient's result does not establish
that the cohort-wide multiplex signal was a reagent artifact rather
than real biology or assay-sensitivity limits, or some mix of both.)
`ERBB2` was excluded only from downstream analyses of this specific
multiplex protein-expression panel -- the same publication does go on
to analyze `ERBB2` amplification, single-plex `ERBB2` IHC, and
anti-`ERBB2` treatment response elsewhere, so "excluded from every
downstream analysis in their own paper" would overclaim.

Because a numeric value greater than zero is not evidence of
biologically "detected" `ERBB2` protein (the source publication states
no assay-detection threshold, and these are the very values the source
authors themselves judged too low to trust), this script does NOT
report a "detected/undetected" fraction. It reports how many of the 136
`ERBB2` rows carry a positive numeric `mean_express_PDO` value --
`summarize_values()`, not "summarize_detection()" -- and leaves any
detection/prevalence claim unmade. `evidence_directness` for the
resulting evidence row is `UNCALIBRATED_PROXY` (same tier as this
repository's other Module D IHC/MS sources), but the claim/notes text
must always carry the source-exclusion caveat verbatim, framed exactly
as the source publication frames it -- never as "reagent failure" or
"assay noise," which this repository cannot establish.

PDO-to-patient mapping: the source publication states the fourteen-
protein mIHC panel covers "136 PDOs ... from 67 patients" as its own
stated denominator; this script uses that publication-stated patient
count rather than re-deriving one from parsing PDO_id strings (some
PDO_id values carry decimal suffixes, e.g. "Pt54.2", whose meaning --
distinct patient vs. a second lesion/re-resection from the same patient
-- is not resolved in the fetched text and is not guessed at here).
This script's own per-marker patient-level breakdown is therefore not
computed; only the PDO (organoid)-level value summary is reported.

Usage: python3 scripts/extract_pdo_erbb2_mihc.py --gene ERBB2
"""
import argparse
import csv
import hashlib
import statistics
import sys
from pathlib import Path

import openpyxl

REPO_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = (
    REPO_ROOT / "modules" / "module_d_protein_and_endpoint"
    / "data_lock" / "raw" / "MCRC_liver_metastasis_PDO_2026"
)
XLSX_FILE = "Data S3.xlsx"
SHEET_NAME = "Data_Set_3_Proteins_mIHC"
PANEL_MARKERS = {
    "ABCB1", "ABCG2", "CDH1", "CDX2", "CFTR", "ERBB2", "HSF1", "KI67",
    "KRT20", "KRT7", "RCC2", "RIPK1", "TP53", "UGT1A",
}
# Per the source publication's own "respectively" -- KRT7 and ERBB2 were
# excluded for two DIFFERENT reasons, not the same one. Do not collapse
# these back into one shared string (round 1 review of PR #84).
EXCLUDED_MARKERS = {
    "KRT7": "no expression",
    "ERBB2": "very low expression levels",
}


def sha256(path):
    d = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            d.update(chunk)
    return d.hexdigest()


def summarize_values(values):
    """A blank/missing cell is not a numeric value; any other parsed
    float, including 0, is a numeric value. Returns (n_nonzero, n_total,
    fraction_nonzero, (median, min, max) or None -- computed over the
    nonzero values only). This function does NOT claim nonzero implies
    biologically "detected" -- the source publication states no
    assay-detection threshold, so this script reports counts and
    summary statistics only, never a detection/prevalence claim."""
    parsed = [float(v) for v in values if v is not None and str(v).strip()]
    nonzero = [f for f in parsed if f != 0]
    n_nonzero = len(nonzero)
    n_total = len(values)
    frac = n_nonzero / n_total if n_total else None
    stats = (statistics.median(nonzero), min(nonzero), max(nonzero)) if nonzero else None
    return n_nonzero, n_total, frac, stats


def resolve_file():
    inventory_path = REPO_ROOT / "DATA" / "registry" / "MCRC_liver_metastasis_PDO_2026" / "file_inventory.tsv"
    if not inventory_path.is_file():
        print(f"ERROR: {inventory_path} not found.", file=sys.stderr)
        sys.exit(1)
    with open(inventory_path, newline="") as f:
        inventory = {r["file_name"]: r for r in csv.DictReader(f, delimiter="\t")}
    path = RAW_DIR / XLSX_FILE
    if not path.is_file():
        print(f"ERROR: {path} not found.", file=sys.stderr)
        sys.exit(1)
    expected = inventory.get(XLSX_FILE, {}).get("checksum", "").replace("sha256:", "")
    if not expected:
        print(f"ERROR: no checksum recorded for {XLSX_FILE} in {inventory_path}.", file=sys.stderr)
        sys.exit(1)
    actual = sha256(path)
    if actual != expected:
        print(f"ERROR: checksum mismatch for {path}: inventory says {expected}, file is {actual}.", file=sys.stderr)
        sys.exit(1)
    return path


def load_marker_rows(xlsx_path, marker):
    """Returns list of (PDO_id, mean_express_PDO) tuples for the given
    marker, one row per PDO x staining-round the marker was measured
    in (a PDO can appear more than once if a marker was re-stained;
    not deduplicated here -- reported as-is from the source file)."""
    wb = openpyxl.load_workbook(xlsx_path, data_only=True, read_only=True)
    ws = wb[SHEET_NAME]
    rows = list(ws.iter_rows(min_row=1, values_only=True))
    header = rows[0]
    idx = {name: i for i, name in enumerate(header)}
    out = []
    for row in rows[1:]:
        if row[idx["Prot_marker"]] == marker:
            out.append((row[idx["PDO_id"]], row[idx["mean_express_PDO"]]))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gene", required=True)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    gene = args.gene.strip()

    if gene not in PANEL_MARKERS:
        print(f"ERROR: '{gene}' is not among the panel's fourteen markers "
              f"({sorted(PANEL_MARKERS)}).", file=sys.stderr)
        sys.exit(1)

    path = resolve_file()
    marker_rows = load_marker_rows(path, gene)
    if not marker_rows:
        print(f"ERROR: marker '{gene}' has no rows in {path.name} despite being "
              f"a listed panel marker.", file=sys.stderr)
        sys.exit(1)

    values = [v for _pdo, v in marker_rows]
    n_nonzero, n_total, frac_nonzero, stats = summarize_values(values)
    distinct_pdos = sorted({pdo for pdo, _v in marker_rows})

    out_path = Path(args.out) if args.out else (
        REPO_ROOT / "modules" / "module_d_protein_and_endpoint" / "results"
        / f"tgt_{gene.lower()}_pdo_mihc.tsv"
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["PDO_id", "mean_express_PDO"], delimiter="\t")
        w.writeheader()
        for pdo, v in marker_rows:
            w.writerow({"PDO_id": pdo, "mean_express_PDO": v if v is not None else "NA"})

    print(f"\nWrote {len(marker_rows)} PDO rows to {out_path}")
    print(f"\n{gene}: {len(distinct_pdos)} distinct PDOs measured in the 14-marker mIHC panel.")
    if stats:
        median, lo, hi = stats
        print(f"{gene} mIHC mean_express_PDO (this study's own normalized relative fluorescence "
              f"intensity scale; source publication states no assay-detection threshold, so this "
              f"is a numeric-value summary, not a detection/prevalence claim): "
              f"{n_nonzero}/{n_total} rows ({frac_nonzero:.1%}) carry a positive numeric value; "
              f"median={median:.4g}, min={lo:.4g}, max={hi:.4g}.")
    else:
        print(f"{gene}: 0/{n_total} rows carry a positive numeric value.")

    if gene in EXCLUDED_MARKERS:
        print(f"\n*** CAVEAT: the source publication's own methods text states '{gene}' was "
              f"excluded from downstream analyses of this multiplex protein-expression panel "
              f"due to '{EXCLUDED_MARKERS[gene]}'. This repository cannot determine whether "
              f"that reflects genuinely low protein abundance, limited assay sensitivity, or "
              f"both -- these source-provided processed values are reported as-is, with no "
              f"detection/prevalence claim.", file=sys.stderr)


if __name__ == "__main__":
    main()
