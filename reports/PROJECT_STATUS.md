# CRC Unmet-Need Therapeutic Atlas — project status

更新时间：2026-08-10

## 项目目标

建立一个 registry-first 的 CRC Unmet-Need Therapeutic Atlas，为 advanced/metastatic CRC 的 ADC 和 therapeutic target discovery 提供可追溯证据来源。仓库不保存具体生物数据，只保存来源、索引、下载方式、元数据契约、审查结果和更新机制。

## 已完成

1. 读取并落实 `Asset-Generation-OS-architecture.md#CRC Unmet-Need Therapeutic Atlas` 的 scope。
2. 建立独立 GitHub 仓库：`leezx/crc-unmet-need-therapeutic-atlas`。
3. 建立 Phase 1 registry，收录 14 个候选资源：GEO、DepMap、PRIDE、PDO/organoid、Perturb-seq、HPA 和 GTEx。
4. 定义 dataset registry、sample metadata、source manifest 三类 TSV schema。
5. 为已开始 source verification 的种子数据集建立 dataset README 和 manifest。
6. 固化 processed-first policy，禁止默认下载 FASTQ/BAM 等大体积 raw data。
7. 加入 `scripts/validate_registry.py` 和 `scripts/scan_sources.py`。
8. 加入每周 GitHub Action：只做 landing-page metadata scan，并通过 draft PR 供人工审核。
9. 加入 Phase 1 review checklist 和 Phase 1 stop condition：review 批准前不开始 bulk download。
10. 已从 Chrome ChatGPT 对话读取并保存 CRC 临床适应症地图反馈。

## 实施方式

- 先从架构文档提取临床 territory、数据层、admission gate、metadata model 和 download policy。
- 将数据集登记与数据下载分离，候选数据先进入 `CANDIDATE` 状态。
- 对每个未来数据集保留 accession、source URL、download method、license、publication DOI、checksum 和 access status。
- 使用 dependency-free Python 脚本做 schema/目录/状态校验和来源页面探测。
- 使用 GitHub Actions 定期扫描；状态变化通过 draft PR 进入人工 review。
- GitHub 工作流采用功能分支 + draft PR，不自动 merge、不自动批准 P0 下载。

## 当前 GitHub 状态

- 默认分支：`main`
- 功能分支：`feat/registry-first-atlas`
- PR：[#1 Initial CRC Unmet-Need Therapeutic Atlas registry](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/1)
- PR 状态：`OPEN / DRAFT`
- 当前 PR 实际 diff：Phase 1 review checklist；初始 registry implementation 已在 `main`。
- 外部 ChatGPT 审核结论：`REQUEST_CHANGES`

## 当前限制

- 14 个候选资源尚未全部完成原始论文/仓库逐项 verification。
- 没有开始批量下载，也没有生成 biological matrices。
- 当前代码已将 `checked_at` 移出稳定 scan output，待外部复审。
- treatment-history schema 已补充 refractory/intolerance/current-line 等最小字段，待外部复审。
- validator 已允许 `CANDIDATE` 没有 dataset-specific directory，待外部复审。
- 网页版 ChatGPT 已复审 head `47cc25c` 并给出 `APPROVE`；随后加入普通 PR/push 的轻量 validation workflow。
- 最新 head `f9c7003` 已再次获得网页版 ChatGPT `APPROVE`；复审反馈认为 PR 可合并，且新增 CI workflow 没有引入 blocker。
- PR #1 已于 2026-08-10 合并，merge commit 为 `240473c`。
- 已开始 Phase 1 P0 source verification：首批核验 GSE178318、GSE224235、GSE226997、DepMap 26Q1、PXD038149、2026 CRLM PDO biobank 和 HPA。
- source verification PR #2 已建立；head `34ea67d` 已通过网页版 ChatGPT 最终复审（`APPROVE`），可合并。
- 开放式搜索又补充 4 个候选，registry 从 14 增至 18 个：CRLM-NMP-ATLAS、HTAN progressive plasticity、GSE159216 和 Zenodo CRC-LM scRNA。
- knowledge/review layer 尚未建立，仍作为后续 PR。
- PR #2 已合并为 `80a8506`；下一分支 `phase1/p1-provenance-inventory` 开始首批 processed-file inventory。
- 已完成 GSE178318 和 GSE224235 的第一批精确文件名、大小、下载 URL 和下载优先级记录；checksum 尚未捕获，未下载生物数据。
- PR #3 已获网页版 ChatGPT `APPROVE`，准备合并；下一步是 checksum capture 和 sample-level metadata review。
- 已开始 P2 sample metadata review：GSE178318 的 15 个 sample accession、6 个 patient group、primary/liver/PBMC 配对关系已建立轻量 sample map；原论文已解析出患者级 treatment context 和 regimen，但未将其误写成独立样本测量。
- PR #4 已获网页版 ChatGPT `APPROVE`，准备合并；sample map 未加入表达矩阵或 biological values。
- PR #5 已获网页版 ChatGPT `APPROVE`；原论文支持的 GSE178318 treatment context 已记录，准备合并。
- 已开始 P4 checksum/offline capture 机制和 GSE224235 sample map；17 个 GEO sample accession 已索引，治疗 regimen/timing 保留 `UNKNOWN`。
- PR #6 已获网页版 ChatGPT `APPROVE`，准备合并；checksum 工具仅处理外部已 staged 文件，不自动下载。
- 已完成 PXD038149 PRIDE API 文件级 provenance 核验：51 个文件中 44 个 raw、7 个非 raw；7 个 processed/metadata/search/peak 文件已登记，raw 仍不默认下载。
- PR #7 已由网页版 ChatGPT 对 reviewed head `fc5cd950d1c73b0325bf48b44169172c3af36f66` 审核为 `APPROVE`；审核确认 API 文件类别、FTP URL、字节大小、CC0 API 记录及 raw/processed 边界无 blocker，准备合并。
- PR #7 已于 2026-08-11 squash 合并，merge commit 为 `0b0a41a`；PXD038149 仍为 `CANDIDATE`。

## 下一步顺序

1. 审核并合并 P0 source verification PR。
2. 补齐已确认来源的 processed-file inventory、checksums、license 和下载路径。
3. 定位 2026 CRLM PDO biobank 的原始 accession。
4. 仅将完成 provenance materialization 的候选转为 `APPROVED`。
5. 另开 knowledge/review layer PR，将临床适应症地图与 dataset evidence 对接。

## 当前继续执行的门禁

- PR #7 合并后，下一阶段只解析 PXD038149 的 `SamplesDescription.xlsx` 元数据；不会把 sample description 解析等同于下载或 dataset approval。
- 任何 checksum 仅在数据被用户或外部 staging 流程明确放入指定目录后离线计算；扫描器不下载生物数据。
- 当前分支 `phase1/p6-pride-sample-metadata` 的下一门禁是为 `SamplesDescription.xlsx` 定义字段级解析和 provenance 记录，不下载文件、不提交样本值。
- PR #8 已由网页版 ChatGPT 对 reviewed head `409d6ded96620b82be63403108aee1ced9a2771a` 审核为 `APPROVE`，CI 通过，准备合并；后续只有明确 staged workbook 才进入字段级 metadata review。
- 公开来源扩展：根据官方 GEO GSE117548 页面及其关联论文新增 CRC PDO 表达/药物筛选候选；16 个 PDO、25 个样本、processed sample-table availability、115.3 MB raw CEL archive、补充 GitHub repository 和 EGA controlled-access study 已登记，image-level/compound-level response 文件仍未声称可用。
- PR #9 已由网页版 ChatGPT 对 reviewed head `a35a9b2580583fb85a1059c04bc5a2ba2a2d8b5c` 审核为 `APPROVE`，CI 通过，准备合并；下一门禁是补充 GitHub repository 的 file-level provenance inventory。
- 已完成 GSE117548 补充 GitHub repository 的只读目录快照：固定 master commit `1bfec50e`，登记顶层 code/data/figures/models/notebooks/references/reports/tables 及 Docker/README/脚本入口；未 clone、未下载、未计算 checksum，data/models/tables 保持待核验。
- PR #10 已由网页版 ChatGPT 对 reviewed head `942a1eb3c5c246c6630cff9922f6bfcee1028a03` 审核为 `APPROVE`，CI 通过，准备合并；后续若继续，仅对 data/models/tables 做更细 API 文件级核验。
- 已完成固定 commit 的资产层 API 汇总：data/models/tables 共 144 个 blob、1,242,162,377 bytes；其中 raw 100 个/482,753,226 bytes，processed 27 个/758,189,431 bytes，models 4 个，tables 1 个；仅记录 API 元数据，未读取或下载内容。
- PR #11 网页审核发现并定位汇总差异：根目录 data/.DS_Store 的 1 个 blob/6,148 bytes 被计入总量但此前未列层；已补为 data/root_metadata，使 144 blobs 与 1,242,162,377 bytes 的总计可加和复核。
