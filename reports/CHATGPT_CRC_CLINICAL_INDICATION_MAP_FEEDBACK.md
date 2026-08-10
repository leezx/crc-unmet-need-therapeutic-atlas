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

本次只保存反馈与项目记录，不直接执行上述五项代码修复；这些修复应作为下一次明确的 PR 修改任务。
