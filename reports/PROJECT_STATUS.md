# CRC Unmet-Need Therapeutic Atlas — project status

更新时间：2026-08-11

## 项目目标

建立 registry-first 的 CRC Unmet-Need Therapeutic Atlas，为 advanced/metastatic CRC 的 ADC 和 therapeutic target discovery 提供可追溯证据来源。仓库不保存具体生物数据，只保存来源、索引、下载方式、元数据契约、审查结果和更新机制。

## 当前阶段

**Phase 1 — dataset discovery and provenance materialization**

当前仍处于候选数据集来源核验阶段。任何候选只有在来源、临床上下文、processed 文件、license/access 和审计门禁完成后，才可在单独 PR 中讨论 `APPROVED`；目前没有候选达到该状态。

## 当前规模

- 独立 GitHub 仓库：[leezx/crc-unmet-need-therapeutic-atlas](https://github.com/leezx/crc-unmet-need-therapeutic-atlas)
- 候选数据集：19 个，全部为 `CANDIDATE`
- 优先级：10 个 `P0_DOWNLOAD`、5 个 `P1_DOWNLOAD`、4 个 `REFERENCE_ONLY`
- source manifests：11 个
- file-level inventories：5 个（GSE159216、GSE178318、GSE224235、GSE226997、PXD038149）
- sample maps：3 个（GSE178318、GSE224235、GSE226997）
- GitHub PR：#1–#29 全部已合并；最新主分支 merge commit 为 `7baa199`
- GSE178318 admission-gate reconciliation 由公开 PR #30 提出；该 PR 用于对齐已完成的 sample-level treatment metadata 与 P0 matrix，当前待审核

## 已完成能力

1. 建立独立 registry、dataset README、source manifest、file inventory 和 sample metadata schema。
2. 建立 `CANDIDATE`、`P0_DOWNLOAD`、`P1_DOWNLOAD`、`REFERENCE_ONLY` 等 admission 语义和 Phase 1 review checklist。
3. 固化 processed-first policy：不默认下载 FASTQ/BAM/CEL/raw archive，不在仓库存储 biological matrices。
4. 建立 registry validator、landing-page scanner、offline checksum capture 工具和稳定输出检查。
5. 建立 GitHub supplementary repository 的 fixed-commit Trees API metadata inventory；不读取 blob、不 clone、不执行、不下载。
6. 建立 weekly metadata scan、pinned-target drift checker、update candidate report 和人工复核清单；上游变化不自动修改 pinned SHA。
7. 保存 Chrome ChatGPT 的 CRC 临床适应症地图反馈和每个 PR 的审核/修复记录。
8. 完成 GSE117548 固定 commit 的 144 个 blob / 1,242,162,377 bytes 分层 inventory。
9. 完成 GSE226997 的 4 个 sample-level supplementary 文件索引和 GSE159216 的 171 patients / 283 samples、283 CHP / 283 CEL 文件级聚合索引。

## 当前门禁与限制

- 没有开始批量下载，也没有生成 biological matrices。
- checksum 只能对用户或外部 staging 流程明确放入指定目录的文件离线计算；当前未对生物文件计算 checksum。
- P0 候选尚未全部完成原始论文、治疗史、分子注释、processed availability、license/access 和下载路径核验。
- PXD038149 的 `SamplesDescription.xlsx` 仍处于 metadata gate；没有下载或解析外部 workbook。
- 2026 CRLM PDO biobank 的原始 accession 尚未定位完成。
- knowledge/review layer 尚未建立，临床适应症地图尚未与 dataset evidence 形成正式关系表。
- `DATA/registry/datasets.tsv` 中候选仍不能解释为已批准的 discovery cohort。

## 下一步顺序

1. 继续完成 P0 候选的 source/file-level provenance，优先处理 PXD038149、DepMap_26Q1、HPA_normal_tissue 和 CRLM PDO biobank。
2. 在明确 staged 文件出现后，运行离线 checksum capture；未 staging 时不下载、不计算。
3. 完成每个 P0 候选的 Phase 1 checklist，再通过单独 PR 讨论是否提升为 `APPROVED`。
4. 定位并核验 2026 CRLM PDO biobank 原始 accession、license 和 processed download path。
5. 另开 knowledge/review layer PR，把 CRC 临床适应症地图与 dataset evidence、证据等级和 data gaps 对接。

## 权威项目记录

- [README.md](../README.md)：仓库目标、范围和 repository map
- [DATASET_REVIEW.md](DATASET_REVIEW.md)：Phase 1 候选、数据缺口和 stop condition
- [PHASE1_REVIEW_CHECKLIST.md](PHASE1_REVIEW_CHECKLIST.md)：逐候选 admission gate
- [PR_HISTORY.md](PR_HISTORY.md)：PR、网页版 ChatGPT 审核和合并记录
- [CHATGPT_CRC_CLINICAL_INDICATION_MAP_FEEDBACK.md](CHATGPT_CRC_CLINICAL_INDICATION_MAP_FEEDBACK.md)：外部审核反馈归档
- [updates/REVIEW_CHECKLIST.md](updates/REVIEW_CHECKLIST.md)：上游 pinned-target 漂移后的人工复核流程
- [P2_SAMPLE_METADATA.md](P2_SAMPLE_METADATA.md)：GSE178318 sample-level treatment/pairing reconciliation
