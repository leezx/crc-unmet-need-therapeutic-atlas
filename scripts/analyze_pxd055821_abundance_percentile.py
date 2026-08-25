#!/usr/bin/env python3
"""Module D follow-up: where do ERBB2/TACSTD2 sit in PXD055821's own
whole-matrix abundance distribution?

Context (Next-handoff item 3e(a)): `ERBB2` and `TACSTD2` show a real,
unreconciled split between `PXD055821` mass-spec (frequent nonzero
detection: 56/60 and 43/60 specimens respectively) and HPA cancer-tissue
IHC (mostly `Low`/`Not detected`: TE038, TE041). This script does not
resolve that split -- it cannot determine, from data alone, whether the
gap reflects cohort-composition differences (PXD055821 is CRC-liver-
metastasis-specific; HPA's cancer_data.tsv cohort is a generic, not
liver-metastasis-specific, colorectal-cancer cohort -- confirmed by
independently fetching HPA's own pathology pages 2026-08-25, which do
not state whether HPA's colorectal-cancer IHC cohort is primary,
metastatic, or mixed, and do not identify which of ERBB2's four listed
antibodies (HPA001383/CAB000043/CAB020416/CAB062555) generated the
colorectal-cancer-category staining specifically), a genuine difference
in assay sensitivity between whole-tissue DIA-NN mass-spec (a
continuous-intensity method whose practical detection floor is well
below what produces visible IHC staining) and HPA's categorical IHC
scoring, or some mix of both.

What this script *can* add, computed directly from the same
already-downloaded `PXD055821` DIA-NN matrix used by
`extract_pxd055821_protein_abundance.py` (no new data source): where
each of the five `A_CLINICAL` targets' own median detected-intensity and
detection-fraction fall relative to every other gene measured in this
same 60-specimen matrix. This is a same-matrix relative-abundance
percentile, not a cross-target ranking of ADC suitability and not a
claim about any other dataset. A target sitting in this matrix's lower
half of the abundance distribution -- while still frequently "detected"
by nonzero-intensity DIA-NN -- is one concrete, checkable partial factor
consistent with (not proof of) the idea that whole-tissue MS's very
permissive "any nonzero signal" detection threshold can register
lower-abundance proteins that a categorical IHC staining call would not
score above `Low`/`Not detected`. This does not rule out the cohort-
composition explanation above, and this script does not attempt to
adjudicate between the two.

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

    fracs_all = sorted(v[2] for v in all_stats.values() if v[2] is not None)
    medians_all = sorted(v[3] for v in all_stats.values() if v[3] is not None)

    out_path = REPO_ROOT / "modules" / "module_d_protein_and_endpoint" / "results" / "pxd055821_abundance_percentile.tsv"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    print(f"Matrix: {n_genes} genes x 60 specimens (PXD055821 Sydney cohort).\n")
    print(f"{'gene':<10}{'n_detected/60':<16}{'frac_detected':<16}{'frac_percentile':<18}"
          f"{'median_intensity':<20}{'median_percentile':<18}")
    for gene in A_CLINICAL_TARGETS:
        if gene not in all_stats:
            print(f"{gene}: NOT FOUND in matrix", file=sys.stderr)
            continue
        n_det, n_tot, frac, median = all_stats[gene]
        frac_pct = percentile_rank(fracs_all, frac) if frac is not None else None
        med_pct = percentile_rank(medians_all, median) if median is not None else None
        rows.append({
            "gene": gene,
            "n_detected": n_det,
            "n_total": n_tot,
            "frac_detected": f"{frac:.4f}" if frac is not None else "NA",
            "frac_detected_percentile_among_9263_genes": f"{frac_pct:.1f}" if frac_pct is not None else "NA",
            "median_intensity": f"{median:.4g}" if median is not None else "NA",
            "median_intensity_percentile_among_genes_with_nonzero_median": f"{med_pct:.1f}" if med_pct is not None else "NA",
        })
        print(f"{gene:<10}{f'{n_det}/{n_tot}':<16}{frac:<16.3f}{frac_pct:<18.1f}"
              f"{median:<20.4g}{med_pct:<18.1f}")

    with open(out_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), delimiter="\t")
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print(f"\nWrote {len(rows)} rows to {out_path}")
    print(f"\nAll percentiles are same-matrix relative-abundance ranks among this matrix's "
          f"{n_genes} genes -- not a cross-dataset or cross-target ADC-suitability ranking, "
          f"and not a resolution of the ERBB2/TACSTD2 MS-vs-IHC split (see this script's own "
          f"docstring for what it does and does not establish).")


if __name__ == "__main__":
    main()
