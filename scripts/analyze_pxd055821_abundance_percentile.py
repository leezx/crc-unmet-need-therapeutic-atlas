#!/usr/bin/env python3
"""Module D follow-up: where do ERBB2/TACSTD2's DIA-NN signal values rank
within PXD055821's own matrix?

Context (Next-handoff item 3e(a)): `ERBB2` and `TACSTD2` show a real,
unreconciled split between `PXD055821` mass-spec (frequent nonzero
detection: 56/60 and 43/60 specimens respectively) and HPA cancer-tissue
IHC (mostly `Low`/`Not detected`: TE038, TE041). This script does not
resolve that split and does not attempt to explain it biologically.

**This is an assay-internal signal-rank descriptor, not a calibrated
cross-protein abundance percentile** (round 1 review of PR #86). This
repository's own Module D contract, already locked by PR #82/TE032-041,
states DIA-NN gene-group intensity is in "arbitrary DIA-NN intensity
units, not directly comparable across genes" -- and that holds within
one matrix just as much as across matrices/cohorts. Protein-specific MS
response (differing tryptic-peptide count, ionization efficiency,
digestion/sequence properties, protein-inference/gene-group aggregation,
and DIA detectability, all per-protein) means a lower raw DIA-NN
intensity for one gene than another does NOT establish that the first
gene's protein is biologically less abundant than the second's. This
script therefore does NOT claim ERBB2/TACSTD2 are "modest-abundance" or
sit in a "lower half of the abundance range" in any biological sense --
only that their own nonzero DIA-NN signal values rank there among this
one matrix's ~9,263 gene-group columns, on this matrix's own,
uncalibrated signal scale. It also does NOT characterize DIA-NN's
nonzero-value detection rule as a "very permissive" or generically
low assay-detection threshold -- "detected = nonzero, non-missing
intensity" is this repository's own operational definition (see
`extract_pxd055821_protein_abundance.py`'s `summarize_detection()`),
not an independently established property of DIA-NN's actual limit of
detection, so it cannot be used to explain why IHC scores lower.

What this script *does* add, computed directly from the same
already-downloaded `PXD055821` matrix (no new data source, no new
claim about biological abundance): each of the five `A_CLINICAL`
targets' own same-matrix DIA-NN signal-intensity percentile -- where
its detection fraction and median detected intensity rank among every
other gene-group column in this one run. This is useful only as an
assay-internal descriptive statistic (e.g. "is this gene's signal near
the lower/sparse end of this assay-output distribution, or not" --
"sparse" describes rank position, not a claim about measurement noise,
which this script has no model for) -- not as
evidence toward, or against, any biological explanation for the
ERBB2/TACSTD2 MS-vs-IHC split. The cohort-composition question (whether
HPA's cancer_data.tsv cohort is liver-metastasis-specific like
PXD055821's Sydney cohort) remains a separate, still-open candidate
factor, addressed in `analysis_contracts/erbb2_tacstd2_ms_ihc_discrepancy.md`,
not by this script.

Usage: python3 scripts/analyze_pxd055821_abundance_percentile.py
"""
import bisect
import csv
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from extract_pxd055821_protein_abundance import resolve_file, summarize_detection

REPO_ROOT = Path(__file__).resolve().parents[1]
A_CLINICAL_TARGETS = ["CEACAM5", "ERBB2", "F3", "NECTIN4", "TACSTD2"]


def load_all_gene_stats(path):
    """Returns {gene: (n_detected, n_total, frac_detected, median_or_None)}
    for every gene row in the matrix, using the same detection definition
    as extract_pxd055821_protein_abundance.py's summarize_detection()."""
    stats = {}
    with open(path, newline="") as f:
        reader = csv.reader(f, delimiter="\t")
        header = next(reader)
        for row in reader:
            gene = row[0]
            values = row[1:]
            n_detected, n_total, frac, s = summarize_detection(values)
            median = s[0] if s else None
            stats[gene] = (n_detected, n_total, frac, median)
    return stats


def percentile_rank(sorted_values, value):
    """Fraction of sorted_values strictly less than value, as a percentile
    (0-100). Standard "percentile of rank" definition, not interpolated."""
    idx = bisect.bisect_left(sorted_values, value)
    return idx / len(sorted_values) * 100 if sorted_values else None


def main():
    path = resolve_file()
    all_stats = load_all_gene_stats(path)
    n_genes = len(all_stats)

    missing = [g for g in A_CLINICAL_TARGETS if g not in all_stats]
    if missing:
        print(f"ERROR: {missing} not found in the {n_genes}-gene matrix -- "
              f"refusing to report a partial/incomplete result set.", file=sys.stderr)
        sys.exit(1)

    fracs_all = sorted(v[2] for v in all_stats.values() if v[2] is not None)
    medians_all = sorted(v[3] for v in all_stats.values() if v[3] is not None)

    out_path = REPO_ROOT / "modules" / "module_d_protein_and_endpoint" / "results" / "pxd055821_abundance_percentile.tsv"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    print(f"Matrix: {n_genes} genes x 60 specimens (PXD055821 Sydney cohort).\n")
    print(f"{'gene':<10}{'n_detected/60':<16}{'frac_detected':<16}{'frac_signal_rank_pct':<22}"
          f"{'median_intensity':<20}{'median_signal_rank_pct':<22}")
    for gene in A_CLINICAL_TARGETS:
        n_det, n_tot, frac, median = all_stats[gene]
        frac_pct = percentile_rank(fracs_all, frac) if frac is not None else None
        med_pct = percentile_rank(medians_all, median) if median is not None else None
        rows.append({
            "gene": gene,
            "n_detected": n_det,
            "n_total": n_tot,
            "frac_detected": f"{frac:.4f}" if frac is not None else "NA",
            "frac_detected_signal_rank_percentile_among_9263_genes": f"{frac_pct:.1f}" if frac_pct is not None else "NA",
            "median_intensity_arbitrary_units": f"{median:.4g}" if median is not None else "NA",
            "median_intensity_signal_rank_percentile_among_genes_with_nonzero_median": f"{med_pct:.1f}" if med_pct is not None else "NA",
        })
        print(f"{gene:<10}{f'{n_det}/{n_tot}':<16}{frac:<16.3f}{frac_pct:<22.1f}"
              f"{median:<20.4g}{med_pct:<22.1f}")

    with open(out_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), delimiter="\t")
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print(f"\nWrote {len(rows)} rows to {out_path}")
    print(f"\nThese are same-matrix, assay-internal DIA-NN signal-rank percentiles on this "
          f"matrix's own uncalibrated intensity scale -- NOT a calibrated cross-protein "
          f"biological-abundance ranking, NOT a cross-dataset or cross-target ADC-suitability "
          f"ranking, and NOT a resolution (or biological explanation) of the ERBB2/TACSTD2 "
          f"MS-vs-IHC split (see this script's own docstring for exactly what it does and "
          f"does not establish).")


if __name__ == "__main__":
    main()
