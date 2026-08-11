# CRC Unmet-Need Therapeutic Atlas — project status

更新时间：2026-08-11

## 项目目标

建立 registry-first 的 CRC Unmet-Need Therapeutic Atlas，为 advanced/metastatic CRC 的 ADC 和 therapeutic target discovery 提供可追溯证据来源。仓库不保存具体生物数据，只保存来源、索引、下载方式、元数据契约、审查结果和更新机制。

## 当前阶段

**Phase 1 — dataset discovery and provenance materialization**

当前仍处于候选数据集来源核验阶段。任何候选只有在来源、临床上下文、processed 文件、license/access 和审计门禁完成后，才可在单独 PR 中讨论 `APPROVED`；目前没有候选达到该状态。

## 量化进度

| 维度 | 当前进度 | 本轮变化 | 判定标准 | 当前阻塞 |
|---|---:|---:|---|---|
| 工程 / provenance 基础设施 | **90/90** | 85/90 → 90/90（+5） | 19 个候选 closure matrix、13 个候选的结构化 source/no-file-inventory/scope disposition、1 个 configured update target 的 metadata scan/disposition、CI freshness check、source-only 边界审计和 5 个 P0 gate crosswalk 已完成 | DepMap exact headers、HPA final scope/files/terms、CRLM row-level metadata 仍未完成；这些属于后续 dataset review，不再是内部 closure 缺口 |
| source-only completion endpoint | **100% COMPLETE** | final closure PR #53 已合并；内部 closure artifacts、update disposition、validator 和 no-data audit 均满足 | `closure_matrix_is_complete`、`every_update_target_has_scan_disposition`、`final_closure_pr_is_merged`、`validator_tests_and_no_data_audit_pass` 全部满足 | 无 source-only 内部 blocker；后续仅是独立 dataset review 或未来科学/临床 overlay |
| 科学 / 临床可用性 | **0/10** | 0/10 → 0/10（+0） | 本阶段不下载或分析数据；科学 readiness 只在未来独立分析阶段计分 | 当前没有 biological matrix、target ranking、therapeutic-window 或 clinical conclusion |
| 总体项目进度 | **90/100（90%）** | 90/100 → 90/100（source-only endpoint 已关闭；科学 overlay 不计入本阶段） | 固定 100 分制：source-only engineering/provenance 90 分 + scientific/clinical readiness 10 分；当前总分为 90 + 0 | source-only 阶段完成；科学/临床 overlay 仍按当前范围为 0/10 |

评分明细（工程/provenance 90/90）：registry/admission architecture 10/10；source/index layer 15/15；validator/tests 10/10；update/scan system 10/10；PR/review audit 10/10；P0 gate design 10/10；exact dataset provenance materialization 15/15；closure/handoff 10/10。科学/临床可用性 0/10，因为本阶段不进行 biological analysis，也没有 candidate approval 或 clinical conclusion。本轮完成 final closure 状态同步；分项严格合计 90/90。90/90 加权基础设施评分与 source-only completion endpoint 现在均已闭环；科学/临床 overlay 仍为 0/10。

## 当前规模

- 独立 GitHub 仓库：[leezx/crc-unmet-need-therapeutic-atlas](https://github.com/leezx/crc-unmet-need-therapeutic-atlas)
- 候选数据集：19 个，全部为 `CANDIDATE`
- 优先级：10 个 `P0_DOWNLOAD`、5 个 `P1_DOWNLOAD`、4 个 `REFERENCE_ONLY`
- source manifests：11 个
- file-level inventories：8 个（GSE159216、GSE178318、GSE224235、GSE226997、HPA_normal_tissue、MCRC_liver_metastasis_PDO_2026、PXD038149、CRLM_NMP_ATLAS）
- sample maps：3 个（GSE178318、GSE224235、GSE226997）
- GitHub PR：#1–#49 全部已合并；最新主分支 merge commit 为 `2688cd5`
- PR #33 已合并 source-only evidence objects：EV003 URL、EV008 计数措辞、EV001/EV002 supporting-text 路径、source-only 状态措辞和 inventory 统计均已完成审核修正

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
10. 建立 source-only final audit：受追踪文件后缀、raw/processed/data 路径、文件大小和核心控制文件均由脚本检查，并在 CI 中强制保持稳定。
11. 为 DepMap、HTAN、Zenodo mirror、GSE117548、四个 GEO reference subseries 和 GTEx 建立结构化 no-file-inventory disposition，避免把受控的 source-only 不主张误判为内部遗漏。

## 当前门禁与限制

- 没有开始批量下载，也没有生成 biological matrices。
- checksum 只能对用户或外部 staging 流程明确放入指定目录的文件离线计算；当前未对生物文件计算 checksum。
- P0 候选尚未全部完成原始论文、治疗史、分子注释、processed availability、license/access 和下载路径核验。
- PXD038149 的 `SamplesDescription.xlsx` 仍处于 metadata gate；没有下载或解析外部 workbook。
- 2026 CRLM PDO biobank 的 processed-data accession `hr94h42xdc.3` 已定位；sample-level clinical/treatment reconciliation、checksums 和 third-party terms 仍未完成。
- knowledge/review layer 目前已建立 source-only ontology/link skeleton 和 8 个 source-only evidence objects；尚未形成 target claim、biological/clinical evidence conclusion 或临床适应症结论。
- `DATA/registry/datasets.tsv` 中候选仍不能解释为已批准的 discovery cohort。

## 下一步顺序

1. 按 `reports/P0_NEXT_GATE_PLAN.tsv` 并行推进 DepMap exact-file/header、HPA file-level terms 和 CRLM-NMP row-level metadata 门禁；三个 source-only contract 已建立。
2. 在明确 staged 文件出现后，运行离线 checksum capture；未 staging 时不下载、不计算。
3. 完成每个 P0 候选的 Phase 1 checklist，再通过单独 PR 讨论是否提升为 `APPROVED`。
4. 定位并核验 2026 CRLM PDO biobank 原始 accession、license 和 processed download path。
5. 在现有 knowledge/review layer 上继续人工复核 source-only evidence objects，把 CRC 临床适应症地图与 dataset evidence、证据等级和 data gaps 对接；任何 biological/clinical conclusion 仍需单独审核。

## 权威项目记录

- [README.md](../README.md)：仓库目标、范围和 repository map
- [DATASET_REVIEW.md](DATASET_REVIEW.md)：Phase 1 候选、数据缺口和 stop condition
- [PHASE1_REVIEW_CHECKLIST.md](PHASE1_REVIEW_CHECKLIST.md)：逐候选 admission gate
- [PR_HISTORY.md](PR_HISTORY.md)：PR、网页版 ChatGPT 审核和合并记录
- [CHATGPT_CRC_CLINICAL_INDICATION_MAP_FEEDBACK.md](CHATGPT_CRC_CLINICAL_INDICATION_MAP_FEEDBACK.md)：外部审核反馈归档
- [updates/REVIEW_CHECKLIST.md](updates/REVIEW_CHECKLIST.md)：上游 pinned-target 漂移后的人工复核流程
- [P2_SAMPLE_METADATA.md](P2_SAMPLE_METADATA.md)：GSE178318 sample-level treatment/pairing reconciliation
- [PXD038149_SAMPLE_METADATA_GATE.tsv](PXD038149_SAMPLE_METADATA_GATE.tsv)：PXD038149 workbook staging and sample-metadata gate
- [P0_NEXT_GATE_PLAN.tsv](P0_NEXT_GATE_PLAN.tsv)：批量 P0 下一阶段 provenance 门禁
- [SOURCE_ONLY_FINAL_AUDIT.tsv](SOURCE_ONLY_FINAL_AUDIT.tsv)：无生物数据边界审计结果
- `DATA/registry/*/no_file_inventory_disposition.tsv`：显式不主张 file-level inventory 的 source-only 处置
