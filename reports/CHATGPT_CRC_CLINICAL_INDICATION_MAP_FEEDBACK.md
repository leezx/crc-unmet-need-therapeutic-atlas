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

## PR #5 treatment reconciliation review

复审对象：[PR #5](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/5)，reviewed head：`cca8f1c8197f25571c4bf4c691ee5dba5d2e8a98`。

结论：**APPROVE**。网页版 ChatGPT 检查了实际 diff、`sample_map.tsv` schema 修改和 CI；PR `mergeable: true`，`Validate registry` 为 `completed / success`。

审核确认原论文 [PMC8421363](https://pmc.ncbi.nlm.nih.gov/articles/PMC8421363/) 明确支持：COL15、COL17、COL18 为术前化疗患者，其余患者 treatment-naïve；COL15 为 3 cycles CAPEOX，COL17 为 4 cycles CAPEOX，COL18 为 8 cycles FOLFOX-Bev；三位患者约在末次化疗后 1 个月手术。将这些信息作为 patient-level context 下沉到 matched sample rows，未伪装成独立样本测量；肿瘤样本和 PBMC 的采集语境也未被混淆。

下一步：合并 PR #5；再进入 checksum capture 和其他 P0 数据集的 sample-level reconciliation。

## PR #6 checksum and GSE224235 sample review

复审对象：[PR #6](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/6)，reviewed head：`d8a6f7633af26928c427deaa0fa4f6379c81667f`。

结论：**APPROVE**。网页版 ChatGPT 检查了实际 diff、`capture_checksums.py`、GSE224235 的 17-row `sample_map.tsv` 和 CI；PR `mergeable: true`，`Validate registry` 为 `completed / success`。

审核确认 checksum 工具只从显式 `--data-root` 读取本地文件，缺失文件输出 `MISSING`，没有 HTTP client、下载逻辑或自动写回 registry。GSE224235 的 17 个 accession 组成 8 个 primary/liver matched pairs 加 1 个 primary-only sample；`SURGICAL_RESECTION_CONTEXT` 仅表示 specimen context，regimen 和 treatment timing 保持 `UNKNOWN`。

下一步：合并 PR #6；checksum 只有在外部数据被明确 staged 后才执行，继续保持仓库不存生物数据。

## PR #7 PXD038149 PRIDE provenance review

复审对象：[PR #7](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/7)，reviewed head：`fc5cd950d1c73b0325bf48b44169172c3af36f66`。

结论：**APPROVE**。网页版 ChatGPT 检查了实际 diff、PXD038149 的 `file_inventory.tsv`、`source_manifest.tsv`、README 和 CI；PR `mergeable: true`，`Validate registry` workflow 为 `completed / success`，没有真正 blocker。

审核确认：PRIDE API 返回的 51 个文件中，44 个 RAW 文件明确留在默认范围之外；7 个非 raw 文件逐项登记了精确 FTP URL、API 返回的字节大小和原始类别 `OTHER / SEARCH / PEAK`，仓库内部映射为 `PROCESSED / SEARCH / PEAK`。`Quantitation*.xlsx`、sample metadata、search results、peak/library 文件被保留为可下载候选，但没有被夸大为统一 biological output。license 只记录为“CC0 according to PRIDE API”，PXD038149 仍为 `CANDIDATE`，没有声称已下载或已完成 checksum capture。

下一步：合并 PR #7；继续做 `SamplesDescription.xlsx` 的样本元数据解析和外部 staged 文件的 checksum capture，仍不默认下载 raw 数据。

## PR #8 PXD038149 sample-metadata gate review

复审对象：[PR #8](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/8)，reviewed head：`409d6ded96620b82be63403108aee1ced9a2771a`。

结论：**APPROVE**。网页版 ChatGPT 检查了实际 diff；PR 只改动报告/状态文件，`mergeable: true`，`Validate registry` workflow 为 `completed / success`，没有真正 blocker。

审核确认：`SamplesDescription.xlsx` 的 endpoint、PRIDE category `OTHER`、8,577 bytes 和 registry entry 只是 provenance 记录；只有显式 staged 的本地文件才能进入 checksum 和解析阶段，且继续复用 offline-only `capture_checksums.py`。解析契约要求保留原始标签、对不支持字段使用 `UNKNOWN`，不从 PDO/drug-response labels 推断 systemic treatment exposure；staged file 缺失或 sample identifier 歧义时停止并进入 review。没有 downloader、自动 PRIDE 访问、dataset status 升级或 biological data 提交路径。

下一步：合并 PR #8；若后续获得明确 staged workbook，再进入字段级 metadata review。

## PR #9 GSE117548 CRC PDO source expansion review

复审对象：[PR #9](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/9)，reviewed head：`a35a9b2580583fb85a1059c04bc5a2ba2a2d8b5c`。

结论：**APPROVE**。网页版 ChatGPT 检查了实际 diff、`datasets.tsv`、GSE117548 的 `source_manifest.tsv`、README 和 CI；PR `mergeable: true`，`Validate registry` workflow 为 `completed / success`，没有真正 blocker。

审核确认：GSE117548 被保守记录为 16 个 human CRC PDO、25 个样本、Affymetrix HG-U133_Plus_2 expression array，processed availability 仅限定在 GEO sample-table/Series Matrix 层面。115.3 MB `GSE117548_RAW.tar` 明确标为 raw CEL archive，不进入默认范围；EGA `EGAS00001003140` 标为 `CONTROLLED_ACCESS`，未假设已获批或已有具体文件；补充 GitHub repository 仅作为 provenance entry。研究中“>500 compounds”的表述保持为 study context，没有声称 image-level 或 compound-level response matrix 已可下载；DOI `10.1038/s41467-022-30722-9` 与三条来源保持一致，候选仍为 `P0_DOWNLOAD / CANDIDATE`。

下一步：合并 PR #9；随后对补充 GitHub repository 做 file-level provenance inventory，仍不下载 raw CEL 或受控访问数据。

## PR #10 GSE117548 supplementary repository inventory review

复审对象：[PR #10](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/10)，reviewed head：`942a1eb3c5c246c6630cff9922f6bfcee1028a03`。

结论：**APPROVE**。网页版 ChatGPT 检查了实际 diff、`supplementary_inventory.tsv`、`source_manifest.tsv`、README，以及固定 commit `1bfec50e1f8f8deb7bbaa40aa28315262dbb1c19` 的公开 GitHub API tree；PR `mergeable: true`，`Validate registry` workflow 为 `completed / success`，没有真正 blocker。

审核确认：所有 inventory URL 都锚定 full SHA，而非浮动 `master`；顶层目录和 Dockerfile、README.md、make_results.R 的路径/大小与 API 一致。分类边界保守：`data` 为 `POTENTIAL_DATA_AND_CODE`，`tables` 为 `POTENTIAL_DERIVED_DATA`，`models` 为 model artifacts，figures 不作为 biological matrix，code/notebooks 仅作为分析代码。没有把 repository tree 当作已验证 biological asset、自动下载源或可直接分析的数据包。

下一步：合并 PR #10；后续如需继续，只对 `data/models/tables` 做更细的 API 文件级目录核验，仍不下载内容。

### PR #11 initial review correction

网页版 ChatGPT 首轮对 head `6811d52bb7c4b4457d78b01305f9c4c7b6ef91c9` 给出 **REQUEST_CHANGES**：分层计数为 143、字节合计为 1,242,156,229，但 aggregate 写成 144、1,242,162,377。核对固定 commit API tree 后确认遗漏的是根层 `data/.DS_Store`（6,148 bytes），因此新增 `data/root_metadata`，没有改动 biological-data 边界。

### PR #11 final review

修复对象：[PR #11](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/11)，reviewed head：`54a3a499b7d860cb0a1d8de7545fc434d4e69de5`。

结论：**APPROVE**。网页版 ChatGPT 确认 blobs 加和为 144，字节加和为 1,242,162,377；README、`asset_layer_summary.tsv` 和 `source_manifest.tsv` 一致，CI 为 `completed / success`。`data/raw` 仍为 `EXCLUDED_RAW`，`data/processed` 仍不进入本仓库下载范围，`data/.DS_Store` 为 `REPOSITORY_METADATA / NO_DOWNLOAD`，没有新的 blocker。
## PR #12 selected model/table file inventory review

复审对象：[PR #12](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/12)，reviewed head：196606d。

结论：**APPROVE**。网页版 ChatGPT 最终确认唯一 blocker 为无；固定 commit 下 4 个 model-layer blob 和 1 个 table blob 的路径、Git blob SHA、字节大小与分类边界均可接受。Git blob SHA 被正确作为 provenance identifier，而非 MD5/SHA-256 checksum；model.hdf5 未执行，mutation table 未被当作已验证 clinical annotation。
## PR #13 GSE117548 processed-file inventory review

复审对象：[PR #13](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/13)，reviewed head：272b66d2fd48340f193022513d9df3c257a87fc4。

结论：**APPROVE**。网页版 ChatGPT 确认 processed_file_inventory.tsv 的 27 个 data/processed blob、路径、size 和 Git blob SHA 与固定 commit Git tree API 一致；27 行字节总量为 758,189,431，与 asset_layer_summary 对齐，CI 为 completed / success。

审核确认：expression、morphology 和 seq-derived mutation tables 均保持 REVIEW_REQUIRED；README/notes 明确 content not read、not biological-data validated；mutation table 不是已验证 clinical annotation。Git blob SHA 仅作为 repository object identity/provenance，没有被当作 MD5/SHA-256 checksum。
## PR #14 GSE117548 external-file inventory review

复审对象：[PR #14](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/14)，reviewed head：26597fd7972f07c18b59a721c70651c3fe2c9271。

结论：**APPROVE**。网页版 ChatGPT 确认 11 个 data/external blob 的路径、Git blob SHA 和大小与固定 commit Git tree API 一致，字节合计 115,992，与 asset-layer summary 一致。3 个 DS_Store 和 README 为 metadata/documentation；外部 XLSX、5 个 pathway TXT 和外部 signature workbook 分别为 REVIEW_REQUIRED。

审核确认：这些 external assets 未被当作 GSE117548-derived biological data，notes 明确 content not read；不存在把 pathway signatures、外部 workbook 或 repository presence 误升级为 biological validation 的问题。CI 当时为 in_progress，但不是代码/数据 blocker，最终结论为 APPROVE。

## PR #15 fixed-commit GitHub tree scanner review

初审对象：[PR #15](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/15)，初始 reviewed head：`8f5059f`。

结论：**REQUEST_CHANGES**。网页版 ChatGPT 指出唯一 blocker：`--commit` 未限制为完整 commit SHA，仍可传入 `master`、tag 或其他 ref，破坏 fixed-commit provenance 语义。

修复对象：reviewed head `e03089eea70627c7db51e8521ce139911be0d41d`。

复审结论：**APPROVE**。修复新增 `re.fullmatch(r"[0-9a-fA-F]{40}", args.commit)`，并将 help 文案改为 `Full 40-character commit SHA`；`master` 回归测试被拒绝，固定 commit 的 `data/external` 回归测试仍得到 11 files/115,992 bytes。网页版 ChatGPT 确认工具只访问 Git Trees API metadata，不读取 blob 内容、不 clone、不执行、不下载 repository files，truncated tree 仍硬失败，CI 为 completed / success；没有新的网络、安全或维护 blocker。
PR #16 初审：**REQUEST_CHANGES**，唯一 blocker 是 wrapper 未拒绝重复 `target_id` 或 `output_name`，可能使后一个 TSV 静默覆盖前一个结果。

PR #16 修复对象：reviewed head `47846b469f9c2c5a87502512c189eb775f0bcfe0`。

最终复审：**APPROVE**。网页版 ChatGPT 确认重复字段现在在逐 target 循环、网络扫描、`subprocess.run()` 和 TSV 写入之前触发 `SystemExit`；40 位 commit SHA、Trees API-only、artifact 和 no-download 边界未改变。当前 head 无 PR-triggered workflow run/status，但该 workflow 仅支持 schedule/manual dispatch，不构成代码 blocker。

## PR #17 scanner regression-test review

初审对象：[PR #17](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/17)，初始 reviewed head：`ba93d992`。

结论：**REQUEST_CHANGES**。网页版 ChatGPT 发现 `scan_github_targets.py` 在重复配置校验前创建 output 目录，且测试的目录断言位于临时目录清理之后，未真正验证“任何输出前失败”。

修复对象：reviewed head `4a1186a31330a63977eaa9ad62f9742dfda88bc6`。

最终复审：**APPROVE**。`output_dir.mkdir` 已移到全部配置、唯一性和文件名校验之后；断言已移入 `TemporaryDirectory` 作用域。网页版 ChatGPT 确认修复消除了 blocker；测试保持离线，不下载或访问生物数据。

## PR #18 pinned-target drift checker review

初审对象：[PR #18](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/18)，reviewed head：`0fc304a`。

结论：**REQUEST_CHANGES**。网页版 ChatGPT 发现 `/commits/{ref}` 响应可能包含 `files[].patch`，违反 metadata-only 边界。

修复对象：reviewed head `b910ea7`。

最终复审：**APPROVE**。脚本已改用 `/git/ref/heads/{tracking_ref}`，只读取 `object.sha`，并保留仅向 `api.github.com` 发送的 Bearer token；不读取 blob、不下载 patch、不自动修改 pinned commit。CI 通过。

## PR #19 tracked update-report review

复审对象：[PR #19](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/19)，reviewed head：`26edd5e`。

结论：**APPROVE**。网页版 ChatGPT 确认 tracked report 只保存 Git ref metadata；weekly workflow 在 report 变化时通过 draft PR 进入人工审核，不自动修改 pinned SHA，不读取 blob/patch、clone、执行或下载生物数据。

## PR #20 drift-checker regression-test review

初审对象：[PR #20](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/20)，初始 reviewed head：`2627269`。

结论：**REQUEST_CHANGES**。网页版 ChatGPT 指出回归测试只检查第一个请求，且 fake `object.sha` 与 pinned SHA 相同，不能证明测试真正使用了 Git ref 返回的最新 SHA，也不能充分防止退回 `/commits/` endpoint。

修复对象：reviewed head `67a6f04`。

最终复审结论：**APPROVE**。网页版 ChatGPT 确认测试现在要求恰好一次请求、明确禁止 `/commits/`，并用不同的 `bbbb...` latest SHA 驱动 `update_available=TRUE`；本地 3 项测试通过，未发现新的 metadata-only、网络或 provenance blocker。

## PR #21 pinned-target update review checklist

复审对象：[PR #21](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/21)。

结论：**APPROVE**。网页版 ChatGPT 检查了实际 diff 和现有 metadata-only 设计，确认 checklist 要求在 `update_available=TRUE` 时进行固定 commit tree/inventory reconciliation，并要求单独 PR 才能更新 pinned SHA；没有自动改 pin、blob 读取、下载、clone、执行上游代码或将上游变化当作生物学验证的问题。验证记录为 3 项 unittest、registry validation 与 `git diff --check` 全部通过。

## PR #22 GSE226997 source metadata review

初审对象：[PR #22](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/22)，reviewed head：`6c4db77`。

结论：**REQUEST_CHANGES**。网页版 ChatGPT 指出未下载的 raw archive 在 `source_manifest.tsv` 中错误填写了 `download_date=2026-08-11`，与 deferred/no-download 语义矛盾。

修复对象：reviewed head `1d1c421`，将 raw archive 的 `download_date` 改为 `NA`，并明确 `no download performed`。

最终复审结论：**APPROVE**。网页版 ChatGPT 确认唯一 blocker 已解决，没有新的 provenance、treatment-context 或 no-download blocker。

## PR #23 GSE226997 file-level metadata review

初审对象：[PR #23](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/23)，reviewed head：`7a60950`。

结论：**REQUEST_CHANGES**。网页版 ChatGPT 发现 4 个 sample-level supplementary URL 指向 series 目录并返回 404；应使用各自 GEO sample supplementary 路径。

修复对象：reviewed head `a70d5ce`。4 个 URL 已改为 sample-level 路径，并通过 HTTP HEAD 元数据检查。

最终复审结论：**APPROVE**。网页版 ChatGPT 确认 URL blocker 已解决，文件名/大小与官方 filelist 元数据、`NOT_RECORDED` checksum、`NA` download_date 和 no-download 边界一致，没有新的 blocker。

## PR #24 GSE159216 provenance review

初审对象：[PR #24](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/24)，reviewed head：`ce4fda2`。

结论：**REQUEST_CHANGES**。网页版 ChatGPT 发现 GSE159216 的 `priority=P1_DOWNLOAD` 与 comparator-only、`REFERENCE_ONLY` 和 no-download 语义矛盾；修复为 `REFERENCE_ONLY` 后，复审又发现 `n_patients` 错填为 283，官方 GEO 为 171 名患者、283 个样本。

最终修复对象：reviewed head `f789cf0`，修正为 `n_patients=171`、`n_samples=283`。

最终复审结论：**APPROVE**。网页版 ChatGPT 确认 priority、患者/样本计数、文件分类和 no-download 边界一致，没有新的 blocker。

## PR #25 project status reconciliation review

初审对象：[PR #25](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/25)，reviewed head：`7178051`。

结论：**REQUEST_CHANGES**。网页版 ChatGPT 指出 `reports/PROJECT_STATUS.md` 错误写着“当前没有开放 PR”，但 PR #25 本身处于 OPEN / DRAFT。

修复对象：reviewed head `1b4fc99`，将当前 PR 状态明确记录为 OPEN / DRAFT，并保留待复审后合并的状态。

最终复审结论：**APPROVE**。网页版 ChatGPT 确认唯一 blocker 已解决，没有新的 blocker。

## PR #33 source-only evidence objects review

初审对象：[PR #33](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/33)，reviewed head：`b9bd08d`。

结论：**REQUEST_CHANGES**。网页版 ChatGPT 指出 `schemas/evidence.tsv` 中 EV003 的 Mendeley v3 `source_uri` 使用了无效的点号路径 `https://data.mendeley.com/datasets/hr94h42xdc.3`，官方路径应为 `https://data.mendeley.com/datasets/hr94h42xdc/3`。

修复对象：reviewed head `72b31d3`，已修正 EV003.source_uri；未改变 evidence 内容边界或下载政策。

第二轮复核对象：归档 head `3bc1a11`。

结论：**REQUEST_CHANGES**。网页版 ChatGPT 指出 EV008 的 `structured_value` 把“16 个 CRC PDO”错误写成了“16 patients”；来源只支持“16 个 CRC PDO、25 个样本”。

当前修复：已将 EV008.structured_value 改为 `16 CRC PDOs; 25 samples`，等待最新 head 的最终网页复核。

第三轮复核对象：修复 head `e3e1223`。

结论：**REQUEST_CHANGES**。网页版 ChatGPT 指出 EV001/EV002 的 supporting-text 路径缺少 `reports/` 前缀；已确认对应文件实际位于 `reports/P2_SAMPLE_METADATA.md` 和 `reports/P6_PXD038149_SAMPLE_METADATA_PLAN.md`。

当前修复：已将两个路径补全，等待最新 head 的最终网页复核。

最终复审对象：head `35a34df`。

结论：**APPROVE**。网页版 ChatGPT 确认 EV003 官方 v3 URL、EV008 PDO/sample 计数措辞、EV001/EV002 supporting-text 路径、evidence/link 外键和 source-only 状态边界均正确，无新的 blocker。

合并前归档复核对象：head `c0324f7`。

结论：**REQUEST_CHANGES**。网页版 ChatGPT 发现 PROJECT_STATUS 仍写“尚未形成 evidence object”，与本 PR 新增的 8 个 source-only evidence objects 矛盾。已改为明确区分 source-only evidence objects 与尚未形成的 biological/clinical conclusions。

后续复核对象：head `b97f5bd`。

结论：**REQUEST_CHANGES**。网页版 ChatGPT 发现 PROJECT_STATUS 的 file-level inventory 统计仍为 5 个，但仓库实际已有 7 个，遗漏 HPA_normal_tissue 与 MCRC_liver_metastasis_PDO_2026。已按实际仓库计数修正为 7 个。

后续复核：网页版 ChatGPT 指出状态行把 `35a34df` 的历史 APPROVE 错写成最新 head 已批准，忽略后续 `b97f5bd` 的 REQUEST_CHANGES。已改为明确记录历史批准 head 与当前待复核 head。

再次复核：网页版 ChatGPT 指出该状态行仍引用旧待复核 head `71afa13`，已更新为当前提交 `99c7722`。

最终指针复核：发现上述归档修正后又产生了 head `f60bf9a`，已将 PROJECT_STATUS 实际文件更新为该当前 head。

最终稳定性修复：移除会随每次审计提交失效的“当前 head”自引用，仅保留历史批准 head，并标记 PR #33 待最终复核。

## PR #32 source-only knowledge/review layer review

初审对象：[PR #32](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/32)，reviewed head：`2f2d619`。

结论：**REQUEST_CHANGES**。网页版 ChatGPT 指出 `PROJECT_STATUS.md` 仍错误写着 2026 CRLM PDO accession 尚未定位，而 registry 已记录 Mendeley accession `hr94h42xdc.3`。

修复对象：reviewed head `79cdc46`，更新 accession 状态并保留 sample-level clinical/treatment、checksum 和 third-party terms 缺口。

最终复审结论：**APPROVE**。网页版 ChatGPT 确认 blocker 已解决，没有新的 blocker。

## PR #31 PXD038149 sample-metadata gate review

审核对象：[PR #31](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/31)，reviewed head：`ec01bef`。

结论：**APPROVE**。网页版 ChatGPT 确认两个 PRIDE workbook 候选、显式 staging 前的停止条件、UNKNOWN 规则和 `P0_DOWNLOAD/CANDIDATE/HOLD` 边界一致，没有声称已解析或已批准。

## PR #30 GSE178318 admission-gate reconciliation review

审核对象：[PR #30](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/30)，reviewed head：`af49234`。

结论：**APPROVE**。网页版 ChatGPT 确认 sample-level treatment/pairing 记录支持将 treatment context 标为 `PASS`，同时保留 molecular annotation、PI-contact、checksum 和最终 admission blockers；dataset 仍为 `P0_DOWNLOAD/CANDIDATE`。

## PR #29 P0 Phase 1 admission matrix review

初审对象：[PR #29](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/29)，reviewed head：`8643557`。

结论：**REQUEST_CHANGES**。网页版 ChatGPT 指出 `MCRC_liver_metastasis_PDO_2026` 的 `license_access=PASS` 与同一行“third-party terms 尚待核验”矛盾。

修复对象：reviewed head `4b291c8`，将该门禁降为 `PARTIAL`。

最终复审结论：**APPROVE**。网页版 ChatGPT 确认门禁与 blocker 文本一致，没有新的 blocker。

## PR #28 CRLM PDO biobank repository review

审核对象：[PR #28](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/28)，reviewed head：`2dd9751`。

结论：**APPROVE**。网页版 ChatGPT 核验了论文 PMID `42208542`、Mendeley Data v3 accession `hr94h42xdc.3`、DOI、CC BY 4.0 和 Data S1–S5 文件边界，确认没有下载、checksum、候选批准或 raw-sequencing 越界声明。

## PR #27 HPA 25.1 file provenance review

审核对象：[PR #27](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/27)，reviewed head：`41da9cd`。

结论：**APPROVE**。网页版 ChatGPT 核验了 HPA v25.1、Ensembl v109、四个官方下载端点、CC BY 4.0 与第三方约束，并确认没有下载、checksum、therapeutic-window 或 `APPROVED` 越界声明。

## PR #26 DepMap 26Q1 release provenance review

初审对象：[PR #26](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/26)，reviewed head：`ee4276e`。

结论：**REQUEST_CHANGES**。网页版 ChatGPT 指出 `DATA/registry/DepMap_26Q1/source_manifest.tsv` 在明确未下载数据时填写了 `download_date=2026-08-11`，与 no-download 语义矛盾。

修复对象：reviewed head `cbfd7c8`，将 `download_date` 改为 `NA`，并明确记录 no download performed。

最终复审结论：**APPROVE**。网页版 ChatGPT 确认唯一 blocker 已解决，没有新的 blocker。
