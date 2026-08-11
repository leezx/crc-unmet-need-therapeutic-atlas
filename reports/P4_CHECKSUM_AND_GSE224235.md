# P4 checksum and GSE224235 sample index

Date: 2026-08-11

## Checksum capture

`scripts/capture_checksums.py` computes MD5 and SHA-256 only for files already staged in an external data root. It never calls a network endpoint and never writes biological files to this repository. Missing files are reported as `MISSING`; they are not downloaded or silently treated as verified.

Example after an explicitly approved external staging step:

```bash
python3 scripts/capture_checksums.py \
  --data-root /path/to/external/staged-data \
  --inventory DATA/registry/GSE178318/file_inventory.tsv \
  --output /path/to/external/checksum_capture.tsv
```

## GSE224235 sample map

The official GEO series page lists 17 samples: matched primary/liver pairs for patient labels 187278, 187252, 187269, 187256, 187284, 187286, 187254 and 187273, plus a primary-only 187265 sample. These are indexed in `DATA/registry/GSE224235/sample_map.tsv`.

The accession-level assay is NanoString nCounter PanCancer IO 360. `SURGICAL_RESECTION_CONTEXT` describes specimen context only; regimen and treatment timing remain `UNKNOWN`. The map does not claim that the broader study's GeoMx component is available under this accession.
