# P2 sample metadata review — GSE178318

Date: 2026-08-11

The official GEO series page lists 15 samples from six labelled patient groups: COL07, COL12, COL15, COL16, COL17 and COL18. The sample map records the matched primary CRC, liver-metastasis and PBMC relationships without inferring treatment exposure.

The original publication resolves patient-level treatment context: COL15, COL17 and COL18 received preoperative chemotherapy, while COL07, COL12 and COL16 were treatment-naïve. The reported regimens were three CAPEOX cycles for COL15, four CAPEOX cycles for COL17 and eight FOLFOX-bevacizumab cycles for COL18; surgery occurred about one month after the final chemotherapy cycle. This context is propagated to matched samples as patient-level metadata, not as independent sample measurements.

PBMC rows are marked `PRE_SURGERY_BLOOD`; exact chemotherapy-to-blood collection timing is not inferred beyond the publication's collection context.

The map is an index only. It does not contain expression values or biological data.
