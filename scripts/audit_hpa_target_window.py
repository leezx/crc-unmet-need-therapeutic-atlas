#!/usr/bin/env python3
"""Audit normal-tissue RNA/protein coverage for exploratory CRC state markers."""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
from collections import defaultdict
from pathlib import Path

TARGETS = ["TACSTD2", "L1CAM", "EMP1", "SOX2", "CHGA", "KRT5"]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rna", type=Path, default=Path("phase2/03_data/raw/HPA_normal_tissue/rna_tissue_hpa.tsv.zip"))
    parser.add_argument("--ihc", type=Path, default=Path("phase2/03_data/raw/HPA_normal_tissue/normal_ihc_data.tsv.zip"))
    parser.add_argument("--output", type=Path, default=Path("phase2/06_results/HPA_normal_tissue/target_window_audit.json"))
    args = parser.parse_args()
    rna = defaultdict(list)
    proc = subprocess.Popen(["unzip", "-p", str(args.rna)], stdout=subprocess.PIPE, text=True)
    assert proc.stdout is not None
    for row in csv.DictReader(proc.stdout, delimiter="\t"):
        if row["Gene name"] in TARGETS:
            rna[row["Gene name"]].append({"tissue": row["Tissue"], "nTPM": float(row["nTPM"])})
    if proc.wait() != 0:
        raise RuntimeError(f"Failed to stream RNA archive: {args.rna}")
    missing_rna = sorted(set(TARGETS) - set(rna))
    if missing_rna:
        raise RuntimeError(f"RNA archive is missing target genes: {', '.join(missing_rna)}")
    ihc = defaultdict(list)
    proc = subprocess.Popen(["unzip", "-p", str(args.ihc)], stdout=subprocess.PIPE, text=True)
    assert proc.stdout is not None
    for row in csv.DictReader(proc.stdout, delimiter="\t"):
        if row["Gene name"] in TARGETS:
            ihc[row["Gene name"]].append({"tissue": row["Tissue"], "cell_type": row["Cell type"], "level": row["Level"], "reliability": row["Reliability"]})
    if proc.wait() != 0:
        raise RuntimeError(f"Failed to stream IHC archive: {args.ihc}")
    missing_ihc = sorted(set(TARGETS) - set(ihc))
    result = {}
    for gene in TARGETS:
        values, protein = rna[gene], ihc[gene]
        result[gene] = {
            "rna_tissue_count": len(values),
            "rna_max_nTPM": max((row["nTPM"] for row in values), default=None),
            "rna_tissues_nTPM_ge_1": sorted(row["tissue"] for row in values if row["nTPM"] >= 1),
            "ihc_record_count": len(protein),
            "ihc_detected_or_higher": sorted({row["tissue"] for row in protein if row["level"] != "Not detected"}),
            "ihc_levels": sorted({row["level"] for row in protein}),
        }
    output = {"dataset": "HPA_normal_tissue_v25.1", "targets": TARGETS, "genes": result, "rna_targets_present": sorted(rna), "ihc_targets_present": sorted(ihc), "ihc_targets_without_records": missing_ihc, "interpretation_boundary": "Normal-tissue RNA/protein coverage audit only; no therapeutic window, safety claim, target approval or clinical recommendation."}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
