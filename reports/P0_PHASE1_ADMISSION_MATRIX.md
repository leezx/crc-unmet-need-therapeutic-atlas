# P0 Phase 1 admission matrix

更新时间：2026-08-11

本表把“来源已核验”与“可以批准下载”分开。`PASS` 表示当前 metadata 证据足够；`PARTIAL` 表示有部分证据但仍有缺口；`BLOCKED` 表示该门禁阻止 Phase 1 admission；`NOT_REVIEWED` 表示尚未开始。`HOLD` 是当前唯一决策：本轮不把任何 P0 候选提升为 `APPROVED`。

逐字段矩阵见 [`P0_PHASE1_ADMISSION_MATRIX.tsv`](P0_PHASE1_ADMISSION_MATRIX.tsv)。权威 admission 条件仍见 [`PHASE1_REVIEW_CHECKLIST.md`](PHASE1_REVIEW_CHECKLIST.md)。

## 当前结论

- 10 个 P0 候选全部保持 `CANDIDATE`。
- 已达到 `PASS` 的候选仍可能因 treatment metadata、exact file inventory、license/access、checksum 或 update audit 缺口而保持 `HOLD`。
- `CRC_organoid_CRISPR_dependency` 尚未定位 repository accession，因此不进入下载计划。
- `HPA_normal_tissue` 只承担 normal-tissue safety reference 角色，不作为 malignant discovery cohort。
- `DepMap_26Q1` 的 release-level provenance 已建立，但 CRC subset file selection 仍受 portal verification gate 阻塞。

## Admission rule

只有在单独 reviewed PR 中，逐候选完成原始论文、临床上下文、processed-file inventory、license/access 和 reproducible download path 后，才可讨论 `APPROVED`。本矩阵本身不改变 registry status，也不触发下载。
