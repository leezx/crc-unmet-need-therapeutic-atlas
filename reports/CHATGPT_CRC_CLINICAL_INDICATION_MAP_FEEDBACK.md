# ChatGPT feedback: CRC 临床适应症地图

来源：Chrome 中 ChatGPT 项目 `Biotech ideas` 的对话 [CRC临床适应症地图](https://chatgpt.com/g/g-p-68c041b4df6881918a83a55e2dd7ac70/c/6a7a21a5-9474-83ea-895e-859b789fbe7c)

读取时间：2026-08-10

## 反馈结论

针对当前 `crc-unmet-need-therapeutic-atlas` 仓库，反馈结论为：**REQUEST_CHANGES**。

反馈明确认为当前 scope 是正确的，但指出当前 PR 与实际 diff 不一致，并指出注册表校验器、临床治疗史字段、priority 语义和 weekly scan 时间戳存在问题。

## 反馈认可的设计

- 不是泛 CRC Atlas，而是面向 MSS/pMMR refractory mCRC、RAS-mutant non-G12C、post-systemic-therapy CRC 和 CRLM 的窄范围资源。
- 核心证据链是：patient population → malignant cell state → surface target → dependency/payload vulnerability → normal-tissue therapeutic window。
- registry-first、processed-first，原始数据默认不下载。
- 缺失的 MSI/MMR、RAS/BRAF/HER2、治疗史和样本配对信息保留为 `UNKNOWN`，不做静默推断。
- `Phase 1` 先做数据源发现和审查，不直接开始批量下载。
- knowledge/review layer（临床适应症、SOC、耐药、targets、modality competition）应作为后续 PR，不应扩大首个数据注册表 PR。

## 必须修正的问题

### 1. PR scope 与实际 diff 不一致

PR #1 的描述声称新增了 registry、schema、validator、scanner 和 workflow，但 GitHub 显示这些文件已经在 `main`；PR #1 实际只新增 `reports/PHASE1_REVIEW_CHECKLIST.md`。

决策：PR 标题和 body 必须与真实 diff 一致；初始实现已视为进入 `main`，PR #1 应被视为 Phase 1 审核清单补充。

### 2. `validate_registry.py` 对 `CANDIDATE` 的规则过严

当前 validator 要求所有 registry row 都有 `DATA/registry/<dataset_id>/` 目录，但候选数据集可以尚未完成 source verification。

建议规则：

- `CANDIDATE`：允许没有 dataset-specific directory / manifest；
- `APPROVED` 或 source-verified：必须有 directory + manifest；
- `APPROVED`：必须有可验证 source manifest；
- 实际运行 `python3 scripts/validate_registry.py` 必须返回 0。

### 3. treatment-history schema 仍需补充

建议在 `sample_metadata.tsv` 增加：

`n_prior_lines_metastatic`, `current_line`, `prior_regimens`, `last_regimen`, `progressed_on_last_regimen`, `refractory_status`, `intolerance_status`, `intolerant_to`

原因：exposure、line、progression/refractory 和 intolerance 是不同的 clinical states，不应混为一体。

### 4. priority 语义需要统一

当前 HPA 是 `clinical_relevance_score=0`，但被标为 `P0_DOWNLOAD`；这并不一定是错误，因为 HPA 是 ADC safety reference，但说明 P0 不能只解释为 clinical discovery priority。

最小修法：把 P0 定义改成“required for first decision cycle”，使 discovery dataset 和 required safety reference 都能合理进入 P0。

### 5. weekly scan 存在 timestamp noise

`checked_at` 每周变化，会导致 source 状态不变时也产生新的 JSON diff 和 draft PR。

建议：将 `checked_at` 放到不参与 diff 的日志，或 PR diff 只比较 `dataset_id/url/status/http_status` 等状态字段。`403/405` 应解释为 scanner limitation，不应直接判定 source invalid。

## 后续知识层建议

CRC 临床适应症地图建议形成独立 knowledge/review layer，而不是混入本仓库首个 registry PR。建议后续输出：

- `reviews.tsv`
- `01_clinical_treatment_landscape.md`
- `02_patient_territories.md`
- `03_resistance_mechanisms.md`
- `04_malignant_cell_states.md`
- `05_metastatic_biology.md`
- `06_target_landscape.md`
- `07_modality_landscape.md`
- `08_open_questions.md`
- `UNRESOLVED_THERAPEUTIC_PROBLEMS.tsv`

关键知识表应连接：patient territory、当前 SOC、SOC 失败原因、残余 biology、emerging solution 和 remaining gap，并最终与 multi-omics dataset evidence 对接。

## 当前处理决定

本次复审任务已开始执行上述五项代码修复；每次修改仍需通过本地校验并由网页版 ChatGPT 复审。

## 修复后复审结果

复审对象：PR #1，head `47cc25c7995ed997105fd33f9a1a478075a0265f`。

结论：**APPROVE**。复审确认五项 blocker 均已解决：candidate/approved validator 语义、treatment-history schema、P0 定义、weekly scan timestamp noise，以及 PR scope/body 一致性。

非阻断建议：

- `HEAD` 被 GEO/PRIDE/publisher 拒绝时，未来可增加 GET fallback，或区分 `HEAD_BLOCKED` 与 `SOURCE_INVALID`；当前 scanner 只记录状态，不自动拒绝来源，因此不阻断 Phase 1。
- 增加普通 push/PR 的轻量 GitHub Actions validation workflow，以便每个代码 PR 都有 CI 证据；本次随后已加入 `.github/workflows/validate.yml`。

复审建议下一步：合并 registry infrastructure 后，逐个完成 P0 candidate 的论文、accession、patient composition、treatment annotation 和 processed-data availability verification，再将候选转为 `APPROVED`。knowledge/review layer 应另开 PR。

## 最终快速复审

最新 head：`f9c7003`。

结论：**APPROVE**。新增的 `validate.yml` 在 `pull_request` 和 `push main` 上运行 registry validator，并使用连续两次 offline scan + `cmp` 验证稳定输出；复审确认没有新的 blocker。ChatGPT 反馈显示该 workflow 已完成并成功，PR 可合并。

## PR #2 source-verification review

复审对象：[PR #2](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/2)，最新 head：`34ea67d04f3a4bad07a97b5a7bb423087e49e610`。

结论：**APPROVE**。网页版 ChatGPT 检查了公开 PR 的实际 diff、GitHub CI、registry、relationship schema、README 修订和 source manifest；PR `mergeable: true`，`Validate registry` workflow 为 `completed / success`。

本轮确认已解决的四项问题：

- `Zenodo_CRC_LM_scRNA` 通过 `DATA/registry/relationships.tsv` 明确作为 `CRLM_NMP_ATLAS` 的 `ALIAS_OR_SOURCE_MIRROR`，并执行 `COUNT_CANONICAL_ONLY`，避免重复证据计数。
- `CRLM_NMP_ATLAS.n_samples` 改为 `UNKNOWN`；`75,104` 只作为 CELLxGENE cell count 记录。
- `GSE224235.target_discovery_value` 从 `3` 降为 `2`，并限定为 matched primary–CRLM context comparator；GeoMx availability 仍标为未确认。
- HTAN 的 treatment annotation 改为 `SURGICAL_RESECTION_CONTEXT`，并明确 systemic treatment exposure unknown。

下一步：可合并 PR #2；合并后继续做 processed-file inventory、checksum、license/access 和下载路径的逐项 provenance materialization。仍不下载生物数据，也不把 alias 作为独立 cohort。后续 knowledge/review layer 另开 PR。

### Audit-only head confirmation

最新审计提交 `b4d2b47` 仅修改三份 reports 文件，没有改变 registry、relationships、schema、source manifests 或代码。网页版 ChatGPT 快速确认结果仍为 **APPROVE**，没有新的 blocker；当时 GitHub `Validate registry` 仍在运行，但不影响技术结论。

## PR #3 processed-file provenance review

复审对象：[PR #3](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/3)，reviewed head：`56ba66c7adcacba3d8c6d6af0951c11ae59eb9df`。

结论：**APPROVE**。网页版 ChatGPT 检查了实际 diff、两个 `file_inventory.tsv`、schema、validator 和 CI；PR `mergeable: true`，`Validate registry` 为 `completed / success`，没有真正 blocker。

审核确认：

- GSE178318 的三个 processed 文件及 GEO 官方下载 endpoint、大小和 priority 记录正确，未把 SRA raw 数据混入当前范围。
- GSE224235 正确区分 sample-table processed evidence 与 170 KB raw archive，没有声称 GeoMx ROI matrix 已确认公开。
- checksum 尚未记录，且没有候选被提前升级为 `APPROVED`，符合 provenance gate。

下一步：合并 PR #3；随后进入 checksum capture 和 sample-level metadata review，仍不默认下载 raw data。

## PR #4 sample metadata review

复审对象：[PR #4](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/4)，reviewed head：`69ccbff3d2f157cb90bc3b83fa77954afa85102e`。

结论：**APPROVE**。网页版 ChatGPT 检查了实际 diff、`sample_map.tsv`、schema、validator 和 GitHub CI；PR `mergeable: true`，`Validate registry` 为 `completed / success`，没有真正 blocker。

审核确认：15 个 GEO sample accession 已完整收录，并按 COL07、COL12、COL15、COL16、COL17、COL18 六组组织；primary CRC、liver metastasis、PBMC 配对关系内部一致。所有 sample-level treatment context 保持 `UNKNOWN`，没有把 series-level “preoperative chemotherapy”误下沉为逐样本暴露或时间点。该 PR 不含表达矩阵或其他生物数据，也没有将 sample metadata completeness 等同于 dataset approval。

下一步：合并 PR #4；继续 checksum capture 和逐样本 metadata reconciliation。
