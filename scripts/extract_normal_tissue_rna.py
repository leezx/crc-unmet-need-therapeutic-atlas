#!/usr/bin/env python3
"""Module E: extract one target's bulk-RNA normal-tissue expression from the two
sources declared under config/external_sources.yaml's
module_e_normal_tissue_bulk_rna_reference (HPA RNA tissue consensus, GTEx v11
median TPM). Resolves each source only via its path_env_var (fails closed if
unset, exactly like scripts/build_target_seed_universe.py) -- never reads
example_local_path.

This is a read-only extraction against already-fetched, checksum-verified local
copies of official public bulk-RNA resources -- it does not download anything.
Output is a per-tissue TSV meant to back one or more schemas/target_evidence.tsv
rows for Module E; it is NOT itself an evidence_directness=DIRECT claim -- see
modules/module_e_normal_tissue_risk/README.md's "Cannot prove" section. Bulk
tissue RNA cannot distinguish an accessible cell-surface-positive population
from background/stromal/rare-cell expression, so this script's output is
UNCALIBRATED_PROXY input, not a protein/IHC/cell-type-resolved result.

Usage: python3 scripts/extract_normal_tissue_rna.py --gene CEACAM5
       [--out modules/module_e_normal_tissue_risk/results/tgt_ceacam5_normal_tissue_rna.tsv]
"""
import argparse
import csv
import gzip
import io
import os
import re
import sys
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

# Module E README's explicit "key compartment" list, per source's own tissue naming.
KEY_COMPARTMENTS_HPA = {
    "colon": "colon", "rectum": "rectum", "small intestine": "small_intestine",
    "liver": "liver", "lung": "lung", "kidney": "kidney",
    "heart muscle": "heart", "skin": "skin", "bone marrow": "bone_marrow",
}
KEY_COMPARTMENTS_GTEX = {
    "Colon_Sigmoid": "colon", "Colon_Transverse": "colon",
    "Small_Intestine_Terminal_Ileum": "small_intestine",
    "Liver": "liver", "Lung": "lung",
    "Kidney_Cortex": "kidney", "Kidney_Medulla": "kidney",
    "Heart_Atrial_Appendage": "heart", "Heart_Left_Ventricle": "heart",
    "Skin_Not_Sun_Exposed_Suprapubic": "skin", "Skin_Sun_Exposed_Lower_leg": "skin",
    # GTEx v11's adult donor panel has no bone marrow tissue -- a real, source-level
    # coverage gap, not a script bug. Left unmapped deliberately.
}


def load_external_sources_config(path):
    """Same narrow id:/path_env_var: extraction as build_target_seed_universe.py --
    intentionally not a general YAML parser (scripts/ stays dependency-free)."""
    if not path.is_file():
        print(f"ERROR: {path} not found.", file=sys.stderr)
        sys.exit(1)
    sources = {}
    current_id = None
    in_block = False
    for line in path.read_text().splitlines():
        if line.startswith("module_e_normal_tissue_bulk_rna_reference:"):
            in_block = True
            continue
        if in_block and re.match(r"^\S", line) and not line.startswith("module_e_normal_tissue_bulk_rna_reference:"):
            break  # left the block (next top-level key)
        if not in_block:
            continue
        m_id = re.match(r"\s*-\s*id:\s*(\S+)", line)
        if m_id:
            current_id = m_id.group(1)
            continue
        m_var = re.match(r"\s*path_env_var:\s*(\S+)", line)
        if m_var and current_id:
            sources[current_id] = m_var.group(1)
            current_id = None
    for expected in ("hpa_rna_tissue_consensus", "gtex_v11_median_tpm"):
        if expected not in sources:
            print(
                f"ERROR: could not find a 'path_env_var' for source id '{expected}' "
                f"under module_e_normal_tissue_bulk_rna_reference in {path}.",
                file=sys.stderr,
            )
            sys.exit(1)
    return sources


def resolve_env_path(var_name):
    val = os.environ.get(var_name)
    if not val:
        print(
            f"ERROR: {var_name} is not set. This script resolves Module E's bulk-RNA "
            f"reference sources only via config/external_sources.yaml's path_env_var -- "
            f"it will not fall back to any example_local_path. Set {var_name} and re-run.",
            file=sys.stderr,
        )
        sys.exit(1)
    p = Path(val)
    if not p.is_dir():
        print(f"ERROR: {var_name}={val} is not a directory.", file=sys.stderr)
        sys.exit(1)
    return p


def extract_hpa(hpa_path, gene_symbol):
    zip_path = hpa_path / "raw" / "rna_tissue_hpa.tsv.zip"
    if not zip_path.is_file():
        print(f"ERROR: {zip_path} not found.", file=sys.stderr)
        sys.exit(1)
    rows = []
    with zipfile.ZipFile(zip_path) as z:
        with z.open("rna_tissue_hpa.tsv") as f:
            tr = io.TextIOWrapper(f, encoding="utf-8")
            reader = csv.DictReader(tr, delimiter="\t")
            for row in reader:
                if row["Gene name"] == gene_symbol:
                    rows.append(row)
    return rows


def extract_gtex(gtex_path, gene_symbol):
    candidates = list((gtex_path / "raw").glob("*.gct.gz"))
    if not candidates:
        print(f"ERROR: no .gct.gz file found in {gtex_path / 'raw'}.", file=sys.stderr)
        sys.exit(1)
    gct_path = candidates[0]
    rows = []
    with gzip.open(gct_path, "rt") as f:
        f.readline()  # version line
        f.readline()  # dims line
        header = f.readline().rstrip("\n").split("\t")
        tissues = header[2:]
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if parts[1] == gene_symbol:
                rows.append({"ensembl_id": parts[0], "gene_symbol": parts[1],
                             "values": dict(zip(tissues, parts[2:]))})
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gene", required=True, help="HGNC gene symbol, e.g. CEACAM5")
    ap.add_argument("--out", default=None, help="output TSV path")
    args = ap.parse_args()
    gene = args.gene.strip()

    env_vars = load_external_sources_config(REPO_ROOT / "config" / "external_sources.yaml")
    hpa_path = resolve_env_path(env_vars["hpa_rna_tissue_consensus"])
    gtex_path = resolve_env_path(env_vars["gtex_v11_median_tpm"])

    hpa_rows = extract_hpa(hpa_path, gene)
    if not hpa_rows:
        print(f"ERROR: gene symbol '{gene}' not found in HPA RNA tissue consensus (40 tissues expected per gene).", file=sys.stderr)
        sys.exit(1)
    if len(hpa_rows) != 40:
        print(
            f"WARNING: expected 40 HPA tissue rows for '{gene}', got {len(hpa_rows)} -- "
            f"gene symbol may not be canonical or the source format has changed.",
            file=sys.stderr,
        )

    gtex_rows = extract_gtex(gtex_path, gene)
    if not gtex_rows:
        print(f"ERROR: gene symbol '{gene}' not found in GTEx v11 median TPM.", file=sys.stderr)
        sys.exit(1)
    if len(gtex_rows) > 1:
        print(
            f"NOTE: {len(gtex_rows)} Ensembl IDs matched gene symbol '{gene}' in GTEx "
            f"(possible PAR/paralog duplication) -- all rows recorded, not merged silently: "
            f"{[r['ensembl_id'] for r in gtex_rows]}",
            file=sys.stderr,
        )
    gtex_row = gtex_rows[0]  # use the first (see NOTE above if >1)

    out_rows = []
    for r in hpa_rows:
        out_rows.append({
            "source": "HPA_RNA_tissue_consensus", "tissue": r["Tissue"],
            "key_compartment": KEY_COMPARTMENTS_HPA.get(r["Tissue"], ""),
            "value": r["nTPM"], "unit": "nTPM",
        })
    for tissue, val in gtex_row["values"].items():
        out_rows.append({
            "source": "GTEx_v11_median_tpm", "tissue": tissue,
            "key_compartment": KEY_COMPARTMENTS_GTEX.get(tissue, ""),
            "value": val, "unit": "median_TPM",
        })

    out_path = Path(args.out) if args.out else (
        REPO_ROOT / "modules" / "module_e_normal_tissue_risk" / "results"
        / f"tgt_{gene.lower()}_normal_tissue_rna.tsv"
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["source", "tissue", "key_compartment", "value", "unit"], delimiter="\t")
        w.writeheader()
        for row in sorted(out_rows, key=lambda r: (r["source"], r["tissue"])):
            w.writerow(row)

    print(f"Wrote {len(out_rows)} rows ({len(hpa_rows)} HPA + {len(gtex_row['values'])} GTEx) to {out_path}")

    # Human-readable key-compartment summary to stdout, for the analysis contract.
    print(f"\nKey-compartment summary for {gene}:")
    for comp in ["colon", "small_intestine", "liver", "lung", "kidney", "heart", "skin", "bone_marrow"]:
        hpa_vals = [r["nTPM"] for r in hpa_rows if KEY_COMPARTMENTS_HPA.get(r["Tissue"]) == comp]
        gtex_vals = [gtex_row["values"][t] for t, c in KEY_COMPARTMENTS_GTEX.items() if c == comp and t in gtex_row["values"]]
        print(f"  {comp:16s} HPA nTPM={hpa_vals or 'NA'}  GTEx medianTPM={gtex_vals or 'NA (not in GTEx panel)'}")

    # Top-5 non-key tissues by HPA nTPM, to avoid tunnel vision on only the
    # module README's named compartments.
    others = sorted(
        (r for r in hpa_rows if not KEY_COMPARTMENTS_HPA.get(r["Tissue"])),
        key=lambda r: float(r["nTPM"]), reverse=True,
    )[:5]
    print(f"\nTop 5 non-key-compartment HPA tissues by nTPM (checking for surprises):")
    for r in others:
        print(f"  {r['Tissue']:20s} nTPM={r['nTPM']}")


if __name__ == "__main__":
    main()
