# Human Protein Atlas normal-tissue reference

Official portal: https://www.proteinatlas.org/

Current release: Human Protein Atlas version 25.1, based on Ensembl version 109. Official downloadable endpoints are indexed in `file_inventory.tsv`: `proteinatlas.tsv.zip`, `proteinatlas.json.gz`, `proteinatlas.xml.gz`, and `cell.svg`. The XML endpoint is the comprehensive versioned atlas export described by HPA; TSV/JSON are corresponding tabular/API-oriented exports, while `cell.svg` is a schematic asset.

Relevant reference layers for therapeutic-window review include normal-tissue protein expression, consensus/HPA/GTEx/FANTOM RNA expression, single-cell type RNA expression, blood-protein resources, and subcellular localization. The registry records these as source scope only; it does not claim that any target has an ADC therapeutic window.

License: the current HPA licence page states CC BY 4.0 for copyrightable HPA database content, with possible third-party constraints. Cite the HPA website and the relevant primary publication/data URL for any later use.

`minimum_organ_reference.tsv` proposes a 10-organ source-level reference set for the first therapeutic-window review: liver, kidney, heart muscle, lung, bone marrow, spleen, colon, small intestine, pancreas and skin. The set is a coverage contract, not a biological result or a clinical safety conclusion; each row remains `PROPOSED_SOURCE_ONLY` until human review confirms the scope.

The selection is anchored to HPA v25.1 tissue names and tissue groups exposed on the official tissue-data page. It covers clearance organs, cardiac/respiratory/hematologic safety, immune-reticuloendothelial tissues, CRC lineage/GI context, pancreas and barrier tissue. It is intentionally minimum and may be expanded for target-specific liabilities.

Current gate: no HPA file was downloaded and no checksum was captured. File sizes, exact release archive hashes, third-party terms and human review of the proposed minimum organ subset remain blocked before any approval discussion.
