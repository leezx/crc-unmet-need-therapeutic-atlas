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
- knowledge/review layer 尚未建立，仍作为后续 PR。

## 下一步顺序

1. 合并 PR #1。
2. 逐个核对 P0 candidate 的论文、accession、patient composition、treatment annotation 和 processed-data availability。
3. 仅将完成 provenance materialization 的候选转为 `APPROVED`。
4. 另开 knowledge/review layer PR，将临床适应症地图与 dataset evidence 对接。
