#!/usr/bin/env python3
"""Module E: extract one target's normal-tissue evidence -- bulk RNA (HPA, GTEx)
and cell-type-resolved IHC (HPA) -- for schemas/target_evidence.tsv.

Source resolution, fixed after web-ChatGPT round-1 review of PR #73 caught two
provenance problems:

  1. HPA RNA + IHC data is NOT read from an external DATA/1.Databases/ location
     via a path_env_var (that was this script's first-pass design, and it also
     mislabeled the file "consensus" when it is actually HPA's own "RNA
     expression (HPA)" 40-tissue product, a different official product from
     "RNA expression (consensus)" (51 tissues) -- see
     https://www.proteinatlas.org/about/download). Both HPA files are already
     tracked, with SHA256, in this repository's own canonical
     DATA/registry/HPA_normal_tissue/source_manifest.tsv, physically present at
     archive/phase2_fetal_state_track_v1/phase2/03_data/raw/HPA_normal_tissue/
     (gitignored, downloaded 2026-08-11 during the pre-pivot phase2 track, never
     deleted). This script now reads that fixed repo-relative path directly and
     verifies each file's SHA256 against source_manifest.tsv before using it --
     hard fail on missing file or checksum mismatch, not a silent fallback.
  2. GTEx v11 median TPM has no local copy anywhere in this repository's own
     tree -- it genuinely is an external resource, reused from another project
     (see DATA/1.Databases/GTEx_v11_median_tpm/link.md on the machine that has
     it), resolved via config/external_sources.yaml's path_env_var, same
     fail-closed pattern as Module A. Its own registry entry,
     DATA/registry/GTEx_normal_tissue/source_manifest.tsv, is backfilled with
     the exact file/release/checksum this script actually used.

Usage:
  python3 scripts/extract_normal_tissue_rna.py --gene CEACAM5
      [--out-rna modules/module_e_normal_tissue_risk/results/tgt_ceacam5_normal_tissue_rna.tsv]
      [--out-ihc modules/module_e_normal_tissue_risk/results/tgt_ceacam5_normal_tissue_ihc.tsv]
"""
import argparse
import csv
import gzip
import hashlib
import io
import os
import re
import sys
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
HPA_RAW_DIR = (
    REPO_ROOT / "archive" / "phase2_fetal_state_track_v1" / "phase2"
    / "03_data" / "raw" / "HPA_normal_tissue"
)

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


def load_tsv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def resolve_hpa_files():
    """Fixed repo-relative path, checksum-verified against this repo's own
    canonical DATA/registry/HPA_normal_tissue/source_manifest.tsv -- not an
    env var, since this is this repository's own tracked (if gitignored) local
    cache, not an external cross-project resource."""
    manifest_path = REPO_ROOT / "DATA" / "registry" / "HPA_normal_tissue" / "source_manifest.tsv"
    if not manifest_path.is_file():
        print(f"ERROR: {manifest_path} not found.", file=sys.stderr)
        sys.exit(1)
    manifest = {r["file_name"]: r for r in load_tsv(manifest_path)}

    resolved = {}
    for fname in ("rna_tissue_hpa.tsv.zip", "normal_ihc_data.tsv.zip"):
        path = HPA_RAW_DIR / fname
        if not path.is_file():
            print(
                f"ERROR: {path} not found. DATA/registry/HPA_normal_tissue/source_manifest.tsv "
                f"records this file as downloaded 2026-08-11 to this repository's own gitignored "
                f"Phase 2 raw cache. If it has genuinely been removed from this machine, that is a "
                f"real state change -- update the calling module's data_lock to say "
                f"'historically downloaded, currently unavailable' rather than silently proceeding "
                f"without it.",
                file=sys.stderr,
            )
            sys.exit(1)
        expected = manifest.get(fname, {}).get("checksum", "").replace("sha256:", "")
        if not expected:
            print(f"ERROR: no checksum recorded for {fname} in {manifest_path}.", file=sys.stderr)
            sys.exit(1)
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != expected:
            print(
                f"ERROR: checksum mismatch for {path}: manifest says {expected}, file is {actual}. "
                f"Do not use a file that doesn't match its own canonical manifest record.",
                file=sys.stderr,
            )
            sys.exit(1)
        resolved[fname] = path
    return resolved


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
        if line.startswith("module_e_gtex_bulk_rna_reference:"):
            in_block = True
            continue
        if in_block and re.match(r"^\S", line) and not line.startswith("module_e_gtex_bulk_rna_reference:"):
            break
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
    if "gtex_v11_median_tpm" not in sources:
        print(
            f"ERROR: could not find a 'path_env_var' for source id 'gtex_v11_median_tpm' "
            f"under module_e_gtex_bulk_rna_reference in {path}.",
            file=sys.stderr,
        )
        sys.exit(1)
    return sources


def resolve_env_path(var_name):
    val = os.environ.get(var_name)
    if not val:
        print(
            f"ERROR: {var_name} is not set. This script resolves the GTEx reference only via "
            f"config/external_sources.yaml's path_env_var -- it will not fall back to any "
            f"example_local_path. Set {var_name} and re-run.",
            file=sys.stderr,
        )
        sys.exit(1)
    p = Path(val)
    if not p.is_dir():
        print(f"ERROR: {var_name}={val} is not a directory.", file=sys.stderr)
        sys.exit(1)
    return p


def extract_hpa_rna(zip_path, gene_symbol):
    rows = []
    with zipfile.ZipFile(zip_path) as z:
        with z.open("rna_tissue_hpa.tsv") as f:
            tr = io.TextIOWrapper(f, encoding="utf-8")
            reader = csv.DictReader(tr, delimiter="\t")
            for row in reader:
                if row["Gene name"] == gene_symbol:
                    rows.append(row)
    return rows


def extract_hpa_ihc(zip_path, gene_symbol):
    rows = []
    with zipfile.ZipFile(zip_path) as z:
        with z.open("normal_ihc_data.tsv") as f:
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
        f.readline()
        f.readline()
        header = f.readline().rstrip("\n").split("\t")
        tissues = header[2:]
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if parts[1] == gene_symbol:
                rows.append({"ensembl_id": parts[0], "gene_symbol": parts[1],
                             "values": dict(zip(tissues, parts[2:]))})
    return rows, gct_path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gene", required=True, help="HGNC gene symbol, e.g. CEACAM5")
    ap.add_argument("--out-rna", default=None)
    ap.add_argument("--out-ihc", default=None)
    args = ap.parse_args()
    gene = args.gene.strip()

    hpa_files = resolve_hpa_files()
    env_vars = load_external_sources_config(REPO_ROOT / "config" / "external_sources.yaml")
    gtex_path = resolve_env_path(env_vars["gtex_v11_median_tpm"])

    hpa_rows = extract_hpa_rna(hpa_files["rna_tissue_hpa.tsv.zip"], gene)
    if not hpa_rows:
        print(f"ERROR: gene symbol '{gene}' not found in HPA RNA tissue (HPA) data.", file=sys.stderr)
        sys.exit(1)
    if len(hpa_rows) != 40:
        print(f"WARNING: expected 40 HPA tissue rows for '{gene}', got {len(hpa_rows)}.", file=sys.stderr)

    ihc_rows = extract_hpa_ihc(hpa_files["normal_ihc_data.tsv.zip"], gene)
    if not ihc_rows:
        print(f"ERROR: gene symbol '{gene}' not found in HPA normal IHC data.", file=sys.stderr)
        sys.exit(1)

    gtex_rows, gct_path = extract_gtex(gtex_path, gene)
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
    gtex_row = gtex_rows[0]

    # RNA output (HPA + GTEx)
    rna_out_rows = []
    for r in hpa_rows:
        rna_out_rows.append({
            "source": "HPA_RNA_tissue_HPA", "tissue": r["Tissue"],
            "key_compartment": KEY_COMPARTMENTS_HPA.get(r["Tissue"], ""),
            "value": r["nTPM"], "unit": "nTPM",
        })
    for tissue, val in gtex_row["values"].items():
        rna_out_rows.append({
            "source": "GTEx_v11_median_tpm", "tissue": tissue,
            "key_compartment": KEY_COMPARTMENTS_GTEX.get(tissue, ""),
            "value": val, "unit": "median_TPM",
        })
    rna_out_path = Path(args.out_rna) if args.out_rna else (
        REPO_ROOT / "modules" / "module_e_normal_tissue_risk" / "results"
        / f"tgt_{gene.lower()}_normal_tissue_rna.tsv"
    )
    rna_out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(rna_out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["source", "tissue", "key_compartment", "value", "unit"], delimiter="\t")
        w.writeheader()
        for row in sorted(rna_out_rows, key=lambda r: (r["source"], r["tissue"])):
            w.writerow(row)
    print(f"Wrote {len(rna_out_rows)} RNA rows ({len(hpa_rows)} HPA + {len(gtex_row['values'])} GTEx) to {rna_out_path}")

    # IHC output (HPA cell-type-resolved)
    ihc_out_path = Path(args.out_ihc) if args.out_ihc else (
        REPO_ROOT / "modules" / "module_e_normal_tissue_risk" / "results"
        / f"tgt_{gene.lower()}_normal_tissue_ihc.tsv"
    )
    with open(ihc_out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["Tissue", "IHC tissue name", "Cell type", "Level", "Reliability"], delimiter="\t")
        w.writeheader()
        for r in sorted(ihc_rows, key=lambda r: (r["Tissue"], r["Cell type"])):
            w.writerow({k: r[k] for k in ["Tissue", "IHC tissue name", "Cell type", "Level", "Reliability"]})
    print(f"Wrote {len(ihc_rows)} IHC rows to {ihc_out_path}")

    # Human-readable summaries
    print(f"\nKey-compartment RNA summary for {gene}:")
    for comp in ["colon", "small_intestine", "liver", "lung", "kidney", "heart", "skin", "bone_marrow"]:
        hpa_vals = [r["nTPM"] for r in hpa_rows if KEY_COMPARTMENTS_HPA.get(r["Tissue"]) == comp]
        gtex_vals = [gtex_row["values"][t] for t, c in KEY_COMPARTMENTS_GTEX.items() if c == comp and t in gtex_row["values"]]
        print(f"  {comp:16s} HPA nTPM={hpa_vals or 'NA'}  GTEx medianTPM={gtex_vals or 'NA (not in GTEx panel)'}")

    others = sorted(
        (r for r in hpa_rows if not KEY_COMPARTMENTS_HPA.get(r["Tissue"])),
        key=lambda r: float(r["nTPM"]), reverse=True,
    )[:5]
    print(f"\nTop 5 non-key-compartment HPA tissues by RNA nTPM:")
    for r in others:
        print(f"  {r['Tissue']:20s} nTPM={r['nTPM']}")

    high_medium = [r for r in ihc_rows if r["Level"] in ("High", "Medium")]
    print(f"\nHPA IHC cell types at High/Medium for {gene} ({len(high_medium)} of {len(ihc_rows)} rows):")
    for r in sorted(high_medium, key=lambda r: (r["Level"] != "High", r["Tissue"])):
        print(f"  {r['Level']:8s} {r['Tissue']:16s} {r['Cell type']}")


if __name__ == "__main__":
    main()
