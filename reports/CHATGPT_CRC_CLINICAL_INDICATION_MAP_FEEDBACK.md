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

## PR #46 source-only completion framework 审核

初审 head `4d899bf`：**REQUEST_CHANGES**。网页版 ChatGPT 指出完成定义允许把首次 update scan 和 final closure PR 等内部步骤错误归类为 external blocker。

修复 head `9ab56c6`：`project_completion.yaml` 增加 mandatory `internal_requirements` 和明确的 `external_blocker_allowlist`；checklist 明确内部 validator/test、no-data audit、scan disposition 和 final closure PR 不可豁免。

最终复审结论：**APPROVE**。确认 source-only completion 与 dataset `APPROVED` 严格分离。

## PR #47 source-only closure matrix 审核

初审 head `e73c908`：**REQUEST_CHANGES**。网页版 ChatGPT 指出缺失 `source_manifest.tsv` / `file_inventory.tsv` 被自动归类为 `EXTERNAL_BLOCKED`，但创建仓库 provenance artifact 是内部工作，不能豁免。

修复 head `fb5003e`：矩阵新增 `blocker_class`，将缺失 artifact 标为 `INTERNAL_ACTION_REQUIRED / INTERNAL_ARTIFACT_GAP`；同时统一 source-only 90 分 + scientific 10 分评分模型。PR 描述中的旧 external blocker 表述随后修正。

最终复审结论：**APPROVE**。确认 19 行矩阵、离线生成器、CI freshness check、评分和内部/外部 blocker 边界一致。

## PR #48 update-target disposition 审核

初审 head `89e09c9`：**REQUEST_CHANGES**。网页版 ChatGPT 指出 `project_completion.yaml` 的 closure 权重与 PROJECT_STATUS 的 8/10 计分不一致。

修复 head `e89ae8e`：统一为 9 项 100 分模型；随后发现 source-only 100% endpoint 不应包含未来 scientific readiness，进一步修复 head `1d27a62`，将 source-only endpoint 定义为 90 分并将 scientific/clinical 作为独立 10 分 overlay。

最终复审结论：**APPROVE**。确认 metadata-only scan、无更新处置、评分模型和 source-only completion 边界一致。

## PR #49 source-only final boundary audit 审核

审核对象：PR #49；复用固定对话“PR审核与错误反馈”。

审核范围：受追踪文件后缀、raw/processed/data 路径、50 MiB 大文件门禁、核心 source-only 控制文件、CI 稳定输出和 75→80 进度更新。没有生物数据下载、分析、候选批准或临床结论。

初审结论：**REQUEST_CHANGES**。必需控制文件只用 `Path.exists()` 检查，未验证其仍属于 `git ls-files`；已修正为“存在且已追踪”双重门禁，防止未追踪重建文件被 CI 误接受。

第二次复审结论：**REQUEST_CHANGES**。PROJECT_STATUS 分项合计为 77/90，无法支持 80/100；已将本轮 +5 显式分配为 source/index +1、PR/review audit +2、closure/handoff +2，并在状态文件中写明依据与算术。

第三次复审结论：**REQUEST_CHANGES**。forbidden suffix denylist 漏掉 `.fq/.fq.gz`、`.cram`、`.vcf/.vcf.gz`、`.loom`、`.cel`、`.chp` 等生物文件；已补入 denylist，尚未改变任何数据范围。

第四次复审结论：**REQUEST_CHANGES**。`reports/SOURCE_ONLY_FINAL_AUDIT.tsv` 未列入 `REQUIRED`；已补入“存在且已追踪”的必需控制文件清单。

最终复审对象：head `cd9705c`。

最终结论：**APPROVE**。网页版 ChatGPT 确认审计报告自身已纳入 tracked-file 门禁，denylist、CI 稳定性、80/90 分项和 no-download/no-analysis/no-approval 边界一致。

## PR #50 explicit no-file-inventory dispositions 审核

审核范围：四个 source-manifest 候选的 tracked `no_file_inventory_disposition.tsv`、closure builder 对该处置的识别、80→85 进度算术，以及 no-download/no-analysis/no-approval 边界。继续复用固定对话“PR审核与错误反馈”。

初审结论：**REQUEST_CHANGES**。`read_disposition()` 未强制 `disposition_id` 非空；已补上 required-field 校验，当前四个 disposition 的 ID 均非空。

最终复审对象：head `239c4fb`。

最终结论：**APPROVE**。网页版 ChatGPT 确认结构化 disposition contract、blocker-class 映射、closure matrix、85/90 分项和 no-download/no-analysis/no-approval 边界一致。

## PR #51 known-source manifest completion 审核

审核范围：四个 GEO reference subseries 与 GTEx 的官方 source manifest、结构化 no-file-inventory disposition、90/90 provenance 算术，以及剩余两个未知来源候选的 blocker 保留。继续复用固定对话“PR审核与错误反馈”。

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

规划复核：网页版 ChatGPT 指出 PROJECT_STATUS 下一步仍要求另开 knowledge/review layer PR，但 PR #32/#33 已建立该层骨架；已改为在现有层上继续人工复核和证据对接。

合并结果：PR #33 已于 2026-08-11 squash-merge，merge commit 为 `c830dba`；source-only evidence objects 已进入 main，未引入 biological data 或临床结论。

## PR #34 状态同步审核

网页版 ChatGPT 审核 PR #34 head `b7f52d6`，结论：**APPROVE**。确认该 PR 只同步 PR #33 合并状态，没有修改 registry、evidence schemas、biological data 或 clinical/target conclusions。

## PR #35 PXD038149 provenance hygiene 审核

网页版 ChatGPT 审核 PR #35 head `3934be9`，结论：**APPROVE**。确认 download_date 已清空为 `NA`，7 个非 raw 文件索引与状态描述一致，PXD038149 仍为 P0_DOWNLOAD/CANDIDATE，workbook staging/parsing/checksum 仍 blocked，未下载或提交 biological data。

## PR #36 项目状态同步审核

网页版 ChatGPT 审核 PR #36 head `b95f1fc`，结论：**APPROVE**。确认主分支 PR/merge 统计更新为 #1–#35 / `29b0edf`，PXD038149 workbook gate 保留，且没有 registry、schema、数据或临床结论变更。

## PR #37 DepMap release evidence 审核

初审 head `37b6bb5`：**REQUEST_CHANGES**。EV009/IEL009 与已有 EV004/IEL004 重复同一 DepMap release-level evidence。

修正 head `5863b1d`：删除重复对象，直接增强 EV004/IEL004；网页版 ChatGPT 最终结论：**APPROVE**。source-only evidence 数量保持为 8，未新增 CRC subset 或 dependency claim。

## PR #38 HPA/CRLM 批量 provenance 审核

初审 head `add076e`：**REQUEST_CHANGES**。HPA `cell.svg` 被错误归类为 versioned endpoint。

修正 head `aed039c`：改为 3 个 v25.1 atlas exports + 1 个 static asset；网页版 ChatGPT 最终结论：**APPROVE**。CRLM no-download 语义和 status update 也通过审核。

## PR #39 P0 verification schema 审核

网页版 ChatGPT 审核 PR #39 head `615a223`，结论：**APPROVE**。确认后四行补齐 `publication_or_record` 字段，所有行与 10 列表头对齐，没有 biological 或 clinical content 变化。

## PR #40 P0 并行门禁计划审核

网页版 ChatGPT 审核 PR #40 head `caa6f74`，结论：**APPROVE**。确认 DepMap、HPA、CRLM-NMP 五个门禁均为 `BLOCKED / PLANNED_SOURCE_ONLY`，并保留明确的 stop conditions；没有下载、biological data 或 approval 越界。

## PR #32 source-only knowledge/review layer review

初审对象：[PR #32](https://github.com/leezx/crc-unmet-need-therapeutic-atlas/pull/32)，reviewed head：`2f2d619`。

结论：**REQUEST_CHANGES**。网页版 ChatGPT 指出 `PROJECT_STATUS.md` 仍错误写着 2026 CRLM PDO accession 尚未定位，而 registry 已记录 Mendeley accession `hr94h42xdc.3`。

修复对象：reviewed head `79cdc46`，更新 accession 状态并保留 sample-level clinical/treatment、checksum 和 third-party terms 缺口。

最终复审结论：**APPROVE**。网页版 ChatGPT 确认 blocker 已解决，没有新的 blocker。

## PR #41 CRLM-NMP 最新 Zenodo archive inventory 审核

初审 head `f5b803f`：**REQUEST_CHANGES**。网页版 ChatGPT 指出 `file_inventory.tsv` 的三个 `source_url` 仍是 Zenodo record page，不是逐文件官方下载 endpoint，与“下载路径”字段语义不一致。

修复 head `d81ec41`：将 `source_manifest.tsv` 和 `file_inventory.tsv` 的 `source_url` 改为 Zenodo API `/files/<name>/content` 直接下载路径，并把 record page 保留在 notes 作为核验入口。

最终复审结论：**APPROVE**。确认 DOI/version、逐文件 URL、source-record MD5、CC BY 4.0 和 no-download/no-inner-h5ad 边界一致；没有 biological data、sample count、candidate approval 或 clinical conclusion 越界。

## PR #42 量化项目进度审核

初审 head `8f7be81`：**REQUEST_CHANGES**。网页版 ChatGPT 指出 58% 及 56%→58% 缺少可复算的分母、权重和计分清单。

修复 head `a22f4aa`：在 `PROJECT_STATUS.md` 增加固定 100 分制：工程/provenance 58/80、科学/临床可用性 0/20、总体 58/100，并列出工程分项得分和计算式。

最终复审结论：**APPROVE**。确认评分可复算，且 0/20 科学/临床分数与当前没有 biological matrix、candidate approval、target ranking 或 clinical conclusion 的边界一致。

## PR #43 HPA minimum organ reference 审核

审核 head `87b3c24`：**APPROVE**。网页版 ChatGPT 核对了 HPA v25.1 tissue naming、10 个来源级器官/组织的覆盖逻辑、TSV 结构和 `PROPOSED_SOURCE_ONLY` 边界。

确认该 PR 没有下载 HPA 文件、checksum、biological data、therapeutic-window/toxicity 结论或 candidate approval；HPA-G1 仍保持 `BLOCKED / PLANNED_SOURCE_ONLY`，待人工确认器官集、文件级元数据和第三方条款。

## PR #44 HPA gate 后进度同步审核

审核 head `f986a66`：**APPROVE**。网页版 ChatGPT 确认 PR #43 合并提交 `83ac83d`、HPA 门禁进度和 58/100 → 60/100 的固定评分增量一致；没有 biological data、candidate approval、target ranking 或 clinical conclusion 变化。

## PR #45 P0 contracts batch 审核

初审 head `2719e02`：**REQUEST_CHANGES**。网页版 ChatGPT 指出 source-only contract 不能直接计入 exact dataset provenance，要求保留 exact provenance 5/15。

修复 head `55bd8c4`：增加 `P0_CONTRACT_CROSSWALK.tsv`，把 5 个 gate 的 artifact、source evidence、completed scope 和 remaining blocker 显式对齐；PROJECT_STATUS 改为固定评分 60/100 → 65/100（+5），其中 source/index +1、P0 gate design +4，exact provenance 不增加。

另一个文档 blocker：PR 描述残留 66/100，已改为 65/100。最终复审结论：**APPROVE**。确认三个 source-only contract、crosswalk、评分和 no-download/no-conclusion 边界一致。

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
## PR #51 known-source manifest completion — initial review

网页版 ChatGPT 在既有对话“PR审核与错误反馈”中审核 PR #51，结论：**REQUEST_CHANGES**。反馈指出：`90/90` 表示 source-only 端点已完成，但 closure matrix 仍有两个 `INTERNAL_ACTION_REQUIRED` 候选，且状态文档同时承认内部闭环未完成，完成度语义自相矛盾。

修复方向：明确区分 90 分加权工程/provenance scorecard 与 source-only completion endpoint；在配置和项目状态中保留 endpoint 为 `INCOMPLETE`，直到 `CRC_organoid_CRISPR_dependency` 与 `CRC_Perturb_seq` 的 source manifest 内部缺口完成。无数据下载、分析、候选批准或临床结论。

最终复审：最新 head `ed00c72`，网页版 ChatGPT 结论：**APPROVE**。确认配置、项目状态和归档记录已经一致区分加权 scorecard 与 completion endpoint；两个内部来源缺口仍被诚实保留为未完成状态。

## PR #52 remaining source identities review

网页版 ChatGPT 在既有对话“PR审核与错误反馈”中审核 PR #52 head `7ed27b7`，结论：**APPROVE**。确认 GSE263580/GSE263581/GSE263582 与 EGA EGAS50000000256 的来源和 accession 可追溯，Mus musculus 工程化类器官与 HT29/SW480 受控访问 Perturb-seq 的 scope 边界已明确，两个候选仍为 `INTERNAL_ACTION_REQUIRED`，没有下载、分析、候选批准或临床结论越界。

## PR #53 source-only final closure review

初审 head `f7e8b12`：**REQUEST_CHANGES**。网页版 ChatGPT 指出 `CRC_organoid_CRISPR_dependency` 已在 scope review 中决定为 reference-only，但 `datasets.tsv` 仍保留 `P0_DOWNLOAD`，与 scope decision 矛盾。

修正 head `202427d`：将该候选改为 `REFERENCE_ONLY`，并同步明确 Mus musculus 工程化类器官来源不等同于 patient-derived-human cohort。网页版 ChatGPT 最终复审结论：**APPROVE**。

## PR #54 source-only completion status review

初审 head `1138690`：**REQUEST_CHANGES**。网页版 ChatGPT 指出 closure matrix 仍有 `SOURCE_INDEXED_REVIEW_REQUIRED` 项，而 completion gate 没有明确这些 dataset-review handoff 是否阻断完成。

修正 head `e101ec5`：增加 `closure_matrix_completion_rule`，明确 19/19 source manifests 加上 file inventory/disposition、且无 `INTERNAL_ACTION_REQUIRED` 即满足 source-only closure；`SOURCE_INDEXED_REVIEW_REQUIRED` 不阻断该 endpoint。网页版 ChatGPT 最终复审结论：**APPROVE**。

## PR #55 source-only handoff documentation review

初审 head `57736ee`：**REQUEST_CHANGES**。优先级统计应为 9 个 `P0_DOWNLOAD`、5 个 `P1_DOWNLOAD`、5 个 `REFERENCE_ONLY`。

修正 head `f329e1f`：网页版 ChatGPT 继续指出 closure checklist 将“完整 file metadata”保留为未完成，与 no-file disposition 规则冲突。

最终修正 head `8dbeb7a`：将 checklist 改为“source-level metadata 或显式 no-file-inventory disposition”，网页版 ChatGPT 结论：**APPROVE**。

## PR #56 Phase 2 therapeutic state discovery plan review

网页版 ChatGPT 在既有对话“PR审核与错误反馈”中审核 PR #56 head `52bdabe`，结论：**APPROVE**。确认问题、novelty boundary、五图证据链和 data-lock v0 可执行，并明确 GSE263580–582 的 mouse reference-only、EGA controlled-access、患者级统计单位及无下载/无分析/无批准边界。

## PR #57 GSE178318 data-lock review

网页版 ChatGPT 在既有对话“PR审核与错误反馈”中审核 PR #57 head `bfe85e8`，结论：**APPROVE**。确认三个官方 processed 文件的 checksum、gzip/维度核验、Git ignored 原始数据边界和 no-analysis 语义一致；未产生 target approval 或临床结论。

## PR #58 Figure 1 analysis-contract review

初审 head：`5223464`，网页版 ChatGPT 结论：**REQUEST_CHANGES**。唯一 blocker 是契约声称使用 prespecified marker/program list，但未锁定 marker 集及版本。

修正 head：`31ad91a`，新增 `figure1_marker_set_v1.tsv`，锁定 epithelial identity、plasticity/non-canonical anchors 与 confounder genes，并规定版本在 QC 后不可变更、confounders 不进入 state score。网页版 ChatGPT 在同一对话中最终结论：**APPROVE**。

## PR #59 GSE178318 structural QC review

初审 head：`03a5231`，网页版 ChatGPT 结论：**REQUEST_CHANGES**。唯一 blocker 是 QC 脚本只报告 barcode/sample/marker reconciliation，没有在失败时退出。

修正 head：`c2c1346`，增加 unparseable barcode、unmapped sample key 和 missing marker 的 fail-closed checks；复审发现仍缺少 `set(sample_map) - set(cell_keys)` 的反向完整性检查。

最终修正 head：`6e13875`，增加双向 sample-key reconciliation；网页版 ChatGPT 在同一对话中最终结论：**APPROVE**。

## PR #60 cell-QC rules review

初审 head：`3fa0767`，网页版 ChatGPT 结论：**REQUEST_CHANGES**。唯一 blocker 是 `QC_SENSITIVE` 的“material change”没有可复现数值定义。

修正 head：`efc727e`，定义 retained-cell count >20%、matched pair 丢失 specimen 或 paired effect direction reversal 为 `QC_SENSITIVE`；网页版 ChatGPT 在同一对话中最终结论：**APPROVE**。

## PR #61 GSE178318 QC retention execution review

初审 head：`eb3aaf7`，网页版 ChatGPT 结论：**REQUEST_CHANGES**。唯一 blocker 是脚本未计算 paired effect direction，却将 retention-only 结果标为完整 `QC_STABLE`。

修正 head：`d1d83be`，将结果改为 `QC_RETENTION_STABLE` / `QC_RETENTION_SENSITIVE`，并明确方向门禁延后至患者级 state analysis。网页版 ChatGPT 在同一对话中最终结论：**APPROVE**。

## PR #62 patient-level state-score review

初审 head：`7c1639b`，网页版 ChatGPT 结论：**REQUEST_CHANGES**。唯一 blocker 是 contract 要求报告 cell-cycle/stress confounders，但脚本未计算或输出这 6 个基因。

修正 head：`55977b6`，增加 sample-level `cell_cycle_report` 与 `stress_report`，并明确不进入 state score 或 paired effect。网页版 ChatGPT 在同一对话中最终结论：**APPROVE**。

## PR #63 GSE224235 independent-validation audit

初审 head：`2cdbf49`，网页版 ChatGPT 结论：**REQUEST_CHANGES**。唯一 blocker 是 `PROJECT_STATUS.md` 仍声称没有对生物文件计算 checksum，与已完成的 Phase 2 checksum 记录冲突。

修正 head：`bfcdd89`，将语义改为仅其余未下载或未授权候选文件尚未计算 checksum。网页版 ChatGPT 在同一对话中最终结论：**APPROVE**。
## PR #64 HTAN replication audit review

初审 head：`fffe070`，网页版 ChatGPT 结论：**REQUEST_CHANGES**。唯一 blocker 是 HTAN 数据集来自 marker set 的来源研究，不能被称为 independent validation，也不能据此增加进度。

修正 head：`a30bbb1`，将 HTAN 结果、脚本边界、PR 描述统一改为 `source-cohort replication audit`，科学 readiness 保持 7/10。网页版 ChatGPT 最终轻量复核：**APPROVE**。

## PR #65 HPA normal-tissue target audit review

初审 head：`d32ade5`，网页版 ChatGPT 结论：**REQUEST_CHANGES**。唯一 blocker 是 HPA 解压返回码和目标缺失没有 fail-closed 处理，可能生成空的审计结果。

修正 head：`55fb4fd`，检查 RNA/IHC archive 返回码；RNA 缺少任一目标时失败；IHC 中官方无记录的目标显式写入 `ihc_targets_without_records`。网页版 ChatGPT 在同一对话最终结论：**APPROVE**。

## PR #67 / #68 CRLM external cohort review

PR #67 因复用旧 HTAN 分支 head `40b29c6` 而关闭，未合并；网页版 ChatGPT 已指出该 head 与声称的 CRLM 提交不一致。

PR #68 初审 head：`c24ad0a`，网页版 ChatGPT 结论：**REQUEST_CHANGES**。唯一 blocker 是 CRLM-versus-adjacent-liver 不等价于锁定的 primary CRC-versus-liver metastasis 对照，不能计为 independent validation 或升至 98/100。

修正 head：`87ba899`，PR 标题、描述、source manifest、脚本/报告和项目状态统一为 external cohort coverage/descriptive audit，进度保持 97/100。网页版 ChatGPT 最终结论：**APPROVE**。

## PR #70 ADC Target Repurposing Atlas pivot review (Modules B-F)

来源：Chrome 中 ChatGPT 项目 `Biotech ideas` 的对话 [CRC临床适应症地图](https://chatgpt.com/g/g-p-68c041b4df6881918a83a55e2dd7ac70/c/6a7a21a5-9474-83ea-895e-859b789fbe7c)（同一对话，即该 ADC Atlas 架构方向的原始来源）。四轮审核，逐轮记录如下；每次网页版 ChatGPT 尝试直接把 review 写回 PR #70 都被 GitHub 连接器的写权限拒绝（403），因此正式 review 记录只保存在这里。

初审 head：初始 pivot commit（未单独打 tag），网页版 ChatGPT 结论：**REQUEST_CHANGES**。五个 blocker：(1) target-first 只存在于 prose，Module A 只是硬编码 `/Volumes/...` 路径，没有 `ADC_TARGET_SEED_UNIVERSE.tsv` 的机器可读 I/O contract，`evidence.tsv`/`indication_evidence_links.tsv` 没有 `target_id`；(2) `module_classification.tsv` 和 canonical `datasets.tsv.priority` 是两套互相冲突的 execution control plane，且前者没有 schema/受控词表/validator；(3) `PROJECT_STATUS.md` 和 `knowledge/README.md` 仍把旧 Phase 2 状态写成当前状态；(4) `qc_gse178318.py`/`apply_gse178318_qc.py`/`audit_hpa_target_window.py` 仍默认读取旧 Fig1 marker panel，部分 module README 与 canonical registry status 矛盾；(5) `.gitignore` 删掉了旧 `phase2/03_data/raw` 等 ignore 规则。三条建议：`CSPA_PXD000589` 应移出 Module B、Module D 需要独立的 HPA cancer/CRC layer、PDO 14-marker mIHC 覆盖限制需要标注。

修正 head `c7dbdaf`（round 2）：新增 `ADC_TARGET_SEED_UNIVERSE.tsv`/`target_evidence.tsv` 契约雏形、`module_classification.tsv` 加受控词表校验器、`PROJECT_STATUS.md`/`knowledge/README.md` 重写为 target-first、三个残留脚本全部归档、`.gitignore` 恢复旧规则、三条建议全部处理。网页版 ChatGPT 复审：**REQUEST_CHANGES**（确认方向已经从架构层面转正，但给出 5 项更细的 contract 级问题：`target_evidence.tsv` 缺 `indication_id`/`evidence_directness`、Module C 把 clinical response association 和真正 persistence 混成一个 axis、Module B 措辞暗示 Module D calibration 可以把 RNA_high 升级成 surface-density、Module A 缺 admission tier、一批一致性问题）。

修正 head `9d47d1e`（round 3）：`target_evidence.tsv` 加 `indication_id`/`measurement_layer`/`evidence_directness`/`source_evidence_id`，明确 evidence.tsv（provenance）与 target_evidence.tsv（canonical interpreted output）两表分工；Module C 拆出 `clinical_endpoint_context` axis；`module_classification.tsv` 加 `activation_context` 受控字段；Module B 措辞改为"Module D calibration 永远不能单独把 RNA_high 升级为 surface-density"；`target_seed.tsv` 加 `derisking_tier`/`repurposing_status` admission gate；一致性问题清空。网页版 ChatGPT 复审：**REQUEST_CHANGES**（独立核对 GSE274551/GSE225857/GSE84267/PXD055821/PXD022613 等官方来源记录，候选集本身没有问题；但指出 GSE274551 等被错误标成 `persistence`——按官方 GEO 设计这是 refractory 组织里的单一时间点 baseline biopsy，不是配对 pre/post 测量；`B_PRECLINICAL_ADC` 的 admission 定义把"抗体+internalization"单独就算数，放得太松；`PROJECT_STATUS.md` 声称"B 和 E 是仅有的两个 CORE_ACTIVE/every_target module"与实际不符）。

最终修正 head `b00d7ec`（round 4）：`persistence` axis 彻底退役，拆成 `longitudinal_persistence`（仅 `GSE84267`，唯一真正配对 pre/post 设计）和 `refractory_or_treated_presence`（`GSE274551`/`GSE178318`/`GSE225857`/`GSE294385`，单一时间点、证明存在而非保留）；`B_PRECLINICAL_ADC` 收紧为要求真实 preclinical ADC construct evidence（target-specific in-vitro killing/in-vivo efficacy），单纯 antibody-internalization 落到 `C_ANTIBODY_OR_BIOLOGY_ONLY` → `FUTURE`；`PROJECT_STATUS.md` 措辞改为"intentionally selected minimum first-pass vertical slice"。网页版 ChatGPT 最终结论：**APPROVE**——确认三处全部到位，未发现新 blocker，明确"这个 PR 的任务是完成 Atlas 的战略 pivot 和执行契约，不是开始真正的数据分析"，可以 merge。

## PR #71 Phase 1 source verification for 13 pivot-added candidates

来源：同一对话 [CRC临床适应症地图](https://chatgpt.com/g/g-p-68c041b4df6881918a83a55e2dd7ac70/c/6a7a21a5-9474-83ea-895e-859b789fbe7c)。三轮审核；正式 review 同样因 GitHub 连接器 403 无法写回 PR，记录只保存在这里。

初审 head `51b9d8a`：网页版 ChatGPT 结论：**REQUEST_CHANGES**。方向正确、source verification 确实发现了新事实，但部分新事实没有反向修正 canonical 字段，且一个数据集的角色定性错误：(1) `GSE235917` 的 `module_classification.tsv` 仍写"确认 candidate 是 tumor-cell localized"，但自己验证过的 source_manifest.tsv 和官方 GEO 都显示这是 PBMC/TIL（免疫细胞）scRNA-seq，生物学上不成立；(2) `GSE225857` 的 `treatment_annotation` 被错误降级为 UNKNOWN，而 GEO 的 Overall design 字段其实已经明确写了 preoperative chemo/RT；(3) `CPTAC_COAD` 不能同时声称"13/13 verification complete"又承认 PDC repository identity 未验证；另有两个小的 metadata 纠正（`GSE196576` n_samples 混淆了 source count 与 analytic subset；`GSE5851` 的 publication 记错成 GEO-series 风格标题）。

修正 head `f8577d6`（round 2）：`GSE235917` 改分类到 `SUPPLEMENT_FROZEN`；`GSE225857.treatment_annotation` 恢复为 `CHEMOTHERAPY_AND_OR_RT_PREOPERATIVE`（独立重新 fetch GEO 页面确认 Overall design 原文后才改）；`CPTAC_COAD` 改为明确"12/13 landing-page verified + 1 publication-only"；`GSE196576.n_samples` 改为 579（真实 source count）；`GSE5851` 的 publication 改为真实同行评审论文（独立重新 fetch Europe PMC 确认后才改）。网页版 ChatGPT 复审：**REQUEST_CHANGES**（独立复核外部源确认以上 5 项全部落地正确，但指出两个剩余的 canonical metadata 不一致：`GSE196576.primary_or_metastatic` 仍简化写成 PRIMARY，而 GEO Overall design 实际是 primary/metastatic/unknown-origin 混合；`CPTAC_COAD` 在 `module_classification.tsv` 里仍残留"Phase 1 source-verified"的旧措辞，与其余文件不一致）。

最终修正 head `2a93817`（round 3）：`GSE196576.primary_or_metastatic` 改为 `UNKNOWN`（独立重新 fetch GEO Overall design 原文确认后才改）；`CPTAC_COAD` 的 `module_classification.tsv` reason 改为"publication verified only, PDC identity deferred"；`PROJECT_STATUS.md` 的 next-handoff 措辞同步更新，避免把已经建立的 12+1 区分在别处又抹平。网页版 ChatGPT 最终结论：**APPROVE**——确认关键问题全部到位；提到一处非阻断性的措辞（"469-primary-tumor analytic subset"应写成"469-profile analytic subset"，因为该子集已证实是混合来源），明确"不影响 canonical registry，也不会改变任何执行决策，不值得再挡一轮 PR"，顺手在同一次修改中改掉。明确下一步：不要继续打磨 Phase 1 metadata，直接进入 Module A 的 `ADC_TARGET_SEED_UNIVERSE.tsv`。

## PR #72 Module A ADC_TARGET_SEED_UNIVERSE.tsv v1 build

来源：同一对话 [CRC临床适应症地图](https://chatgpt.com/g/g-p-68c041b4df6881918a83a55e2dd7ac70/c/6a7a21a5-9474-83ea-895e-859b789fbe7c)。两轮审核；正式 review 同样因 GitHub 连接器 403 无法写回 PR，记录只保存在这里。

初审 head `01aa76b`：网页版 ChatGPT 结论：**REQUEST_CHANGES**。方向基本正确（23 个 `A_CLINICAL`/`ACTIVE` target 作为 v1 起点合理），但作为一个 canonical generated artifact，generator 本身不够 fail-closed，而且一个 CRC-precedent 字段已经出现可见的语义污染：(1) `build_target_seed_universe.py` 没有真正从 `config/external_sources.yaml` 读取 `path_env_var`（硬编码了两个 env var 字符串），也没有对 `adc_candidates.tsv` 的 `status=VALIDATED` gate、crossref 的 missing/extra/duplicate、antigen 文件消失、gene symbol 缺失做 hard fail，全部是 warning 后静默继续，最终生成一个可能不完整的 universe 而不自知；(2) `human_adc_exposure_evidence` 对每个 target 无条件写 YES，把"clinical stage 存在"错误升级成"documented human exposure 已证实"两个不同命题；(3) `adcdb_cancer_types_with_precedent` 的 distillation 有三个真实 bug——explicit negative-context indication string（如"...Excluding...Colorectal Cancer"）被当成 CRC-positive precedent 优先展示（ERBB2 的输出直接暴露了这个问题）；`split(";")` 把细胞遗传学记法（如 `t(9;22)(q34.1;q11.2)`）切成垃圾片段（CD22 输出里出现裸露的"22)(q34.1"）；`cap=8` 没有真正生效为 total cap，ERBB2 远超 8 项；(4) PR 未处于 draft 状态，违反 `CONTRIBUTING.md` 第 9 步。一个很小的 provenance 用词问题：crossref 实际是 27 个 direct wikilink + 2 个 antigen-file backlink + 1 个 unresolved，而不是"29 个都由 antigen field 解析得到"。

修正 head `a100198`（round 2）：`build_target_seed_universe.py` 改为真正从 YAML 读取 `path_env_var`（针对性轻量解析，不引入 PyYAML 依赖）；新增完整 reconciliation——先按 `status=VALIDATED` + 合法 stage 计算 expected candidate set，crossref 的 `asset_entity_id` 集合必须与之精确匹配，missing/extra/duplicate 全部 hard fail；crossref 新增 `resolution_status` 列（`RESOLVED_DIRECT` 27 / `RESOLVED_BACKLINK` 2 / `UNRESOLVED_SOURCE_GAP` 1），`RESOLVED_*` 行对应的 antigen 文件消失、Gene Name 无法解析、UniProt map 缺失，均 hard fail；`human_adc_exposure_evidence` 改为只有该 target 存在已获批资产时才是 YES，纯 clinical-stage target（`CDH6`/`CEACAM5`/`MET`/`EGFR`/`DLL3`/`ERBB3`/`AXL`/`CD276`/`ROR2`/`ITGB6`/`ROR1`/`SLC39A6`）改成 `UNKNOWN`，`derisking_tier` 仍保持 `A_CLINICAL`；indication distillation 的三个 bug 全部修复（negative-context 排除、括号深度感知的安全 split、cap 真正生效为 total cap），新增 `scripts/test_build_target_seed_universe.py` 覆盖四个场景全部通过；PR 转回 draft。网页版 ChatGPT 最终结论：**APPROVE**——逐项复核确认全部真正修掉而非改文案，未发现新的 blocker，明确"现在已经有 23 个真正 clinically derisked 的 target search space，足够验证整个系统"，下一步不要继续扩 Module A 到约 300 个 B/C-tier antigen，直接选一个 `target_id x indication_id` 跑通 Module B + E，产生第一批真正的 `target_evidence.tsv`。

## PR #73 first Module B + E vertical slice for tgt_ceacam5

来源：同一对话 [CRC临床适应症地图](https://chatgpt.com/g/g-p-68c041b4df6881918a83a55e2dd7ac70/c/6a7a21a5-9474-83ea-895e-859b789fbe7c)。三轮审核；正式 review 同样因 GitHub 连接器 403 无法写回 PR，记录只保存在这里。

初审 head `01aa76b`：网页版 ChatGPT 结论：**REQUEST_CHANGES**。方向对（选 `CEACAM5` × `mcrc_preop_chemotherapy_crlm` 合理，Module B 没数据就不编结果的纪律是对的），但这轮真实执行暴露了 4 个接口/科学语义问题：(1) `TE001`/`TE002` 用 `indication_id=normal_tissue_safety_reference`，和 Module B 用的 `mcrc_preop_chemotherapy_crlm` 不一致，把同一 target 拆成两个 dossier；(2) HPA provenance 两处事实错误——`rna_tissue_hpa.tsv` 被错误命名为"HPA RNA tissue consensus"（实际是官方"RNA expression (HPA)"40组织产品，不是"consensus"51组织产品），更关键的是 data lock 声称 IHC 不可用，但仓库自己的 `HPA_normal_tissue/source_manifest.tsv` 已经记录 `normal_ihc_data.tsv.zip`（连 SHA256 都有）下载在案，Module E 自己的核心要求就是 protein/IHC-first triage 却没用上；GTEx 也有 provenance drift（canonical manifest 未回填实际用到的 exact file）；(3) 两条 evidence 的 claim 发生 proxy upgrade——"confines...to GI-mucosal tissue" 自相矛盾（同一行报了 lung 28.5），"signal tracks epithelial content specifically" 超出 bulk RNA UNCALIBRATED_PROXY 能撑的结论；(4) Module B 的 blocker 理由与仓库自己的 `GSE178318/source_manifest.tsv` 矛盾——2026-08-11 已下载 matrix/genes/barcodes（SHA256 校验过），不能用 CANDIDATE 状态抹掉历史已发生的下载；同时 `mcrc_preop_chemotherapy_crlm` 的 `prior_therapy=CAPEOX_OR_FOLFOX_BEV` 对 `GSE225857`（只支持"chemo and/or RT"）来说定义过窄。

修正 head `32c4c1c`（round 2）：`TE001`-`TE003` 统一 `indication_id=mcrc_preop_chemotherapy_crlm`；查实并使用了本机确实存在的 `normal_ihc_data.tsv.zip`，真正做了 CEACAM5 的 cell-type-resolved IHC 分析（109 行，12 行 High 全在 Appendix/Colon/Rectum 的 enterocytes/endocrine/goblet cells），新增 `TE003`；`rna_tissue_hpa.tsv` 改名为正确的"RNA expression (HPA)"；GTEx manifest 回填 exact file+checksum；两处 proxy-upgrade claim 改写为 evidence 能支持的范围；Module B data lock 改为准确描述——`GSE178318` 的 matrix/gene index/sample_map 都在本机（确认 `CEACAM5` 在 gene index 第 31446 行），真正缺的是 malignant/epithelial cell-type annotation，`GSE225857` 才是真正的数据访问 blocker；`prior_therapy` 放宽为 `PREOPERATIVE_CHEMOTHERAPY_AND_OR_RT`。网页版 ChatGPT 复审：**REQUEST_CHANGES**（确认四项基本修到位，但指出一个真正的科学语义 blocker：`TE003` 不应标成 `CALIBRATED_PROXY`——IHC intensity != accessible antigen density，且没有任何真正的 calibration step，只是比 bulk RNA 更接近生物学的 uncalibrated protein proxy；同时 "resolves" 措辞仍然过头，应改成"does not corroborate...lowers but does not eliminate the concern"；外加 PR description 仍是 round 1 旧版本需要同步）。

最终修正 head `7474004`（round 3）：`TE003.evidence_directness` 改为 `UNCALIBRATED_PROXY`；"resolves/confines" 措辞在 `target_evidence.tsv`、Module E 的 `analysis_contracts`/`data_lock`/`README`、`PROJECT_STATUS.md`、`knowledge/README.md` 里全部替换为"does not corroborate...lowers but does not eliminate the concern"；PR description 同步到当前 head。网页版 ChatGPT 最终结论：**APPROVE**——确认四项验收点全部干净落地，没有出现"一边降级一边文档重新升级"的漂移，明确这个 PR 完成了它真正重要的事："第一次证明 `target_id x indication_id` dossier 可以装入真实 RNA/IHC evidence 同时保留 proxy 层级；数据不足时 Module B 能停在真实 blocker，而不是制造假闭环"。明确建议下一步：不要先批量跑另外四个 target 的 Module E，优先把这条 vertical slice 真正闭合——`GSE178318` 的 matrix/gene index/sample metadata 已经存在，剩下是一个明确、有限、可计算的 malignant/epithelial cell annotation 任务，先证明 CEACAM5 能从 Module A 走通 Module B+E，再复制到其他四个 target。

## PR #74 GSE178318 epithelial-proxy screen for tgt_ceacam5

来源：同一对话 [CRC临床适应症地图](https://chatgpt.com/g/g-p-68c041b4df6881918a83a55e2dd7ac70/c/6a7a21a5-9474-83ea-895e-859b789fbe7c)。两轮审核；正式 review 同样因 GitHub 连接器 403 无法写回 PR，记录只保存在这里。

初审 head `cf2b6a6`：网页版 ChatGPT 结论：**REQUEST_CHANGES**。工程细节（checksum、streaming、PBMC sanity check、GSE225857 保持 blocked、TE004=UNCALIBRATED_PROXY、primary→LM 方向如实报告）都做对了，但独立核了 `GSE178318` 原论文（Cell Discovery 2021, DOI `10.1038/s41421-021-00312-y`——顺带发现这个仓库自己的 `source_manifest.tsv` 记的 DOI `10.1038/s41598-021-96568-3` 根本不存在）后发现方法本身低于这个数据集已经公开建立的分析标准，四个真正的问题：(1) 当前做的是 epithelial proxy，不是 Module B 要求的 malignant-cell prevalence——论文自己已经给出更强路径：QC → EPCAM+ 识别 → InferCNV 确认恶性，而这次没有 QC 直接用了全部 140,281 个 barcode；(2) scoring 数学有 bug——所有类别除以同一个 total UMI，argmax 比较时分母抵消，实际是在比不同大小 marker panel 的 raw sum；(3) epithelial 5 基因面板（含 KRT8/KRT18/CDH1）在正常肝上皮里也表达，liver-metastasis 样本里是真实混淆风险；(4) `indication_id` 仍有语义污染——TE004 键到 `mcrc_preop_chemotherapy_crlm`，但 6 个患者全部算进去了，其中 COL07/COL12/COL16 是 treatment-naive，notes 字段不能修复错误的 cohort inclusion。给出两条路：(A，推荐) 复用论文已验证过的 QC/EPCAM/InferCNV 方法；(B，合法降级) 保留当前结果但明确改名为"epithelial-proxy screen"，不宣称 Module B 已关闭。

修正 head `2ab59fa`（round 2）：采用路径 B（不在本 PR 做 InferCNV，重新定位为 epithelial-proxy screen）加上路径 A 里可行的部分——用论文自己的 QC 阈值（>=500 detected genes、<=15% mito UMI、per-sample 3-SD outlier removal，140,281 里 123,330 通过）；epithelial 改成只用 EPCAM（匹配论文方法，不再用会被肝上皮混淆的 5 基因面板）；scoring 改成 marker-average 而不是 raw sum，修掉 denominator 抵消 bug；treated（COL15/COL17/COL18，`TE004`）和 untreated（COL07/COL12/COL16，`TE005`，改用 anatomy-only 的 `mcrc_liver_metastasis`）分开建行；修正后 COL17/COL18 的 epithelial-proxy 细胞数明显下降、COL15 明显更多，方向上跟论文自己报告的"化疗患者 EPC 少、主要来自 COL15"吻合；`DATA/registry/GSE178318/source_manifest.tsv` 的 DOI 也修正了；PR 标题/描述改为"epithelial-proxy screen, not malignancy-confirmed"，不再宣称 vertical slice 已关闭。网页版 ChatGPT 复审：**APPROVE**——确认四项都真正修掉：QC 是论文对齐的真实操作化（不是逐字复现，如实说明）、scoring bug 真的解决、treated/untreated 的 machine semantics 拆开了、claim level 诚实（`TE004`/`TE005` 都是 `UNCALIBRATED_PROXY`，反复声明 epithelial proxy ≠ malignant cell）。给了两条不阻断 merge 的措辞/维护建议：QC 文档里"paper's own exact thresholds"该说成"paper-aligned operationalization"（论文对 gene-count filter 没明说是 3-SD）；`cell_type_marker_set_v1.tsv` 还留着 KRT8/KRT18/KRT19/CDH1 的 epithelial 行，应该标出"当前不参与打分"避免以后的 agent 误用——两条都在 merge 前顺手改了。明确当前状态：CEACAM5 Module E 有真实 RNA/IHC evidence，Module B 有 QC 后的 epithelial-proxy evidence 但 malignant-cell prevalence 仍 UNKNOWN；如果继续这条 vertical slice，真正有价值的下一步是 InferCNV/malignancy confirmation，不是继续优化这个 proxy classifier。

## PR #75 CNV-lite malignancy confirmation attempt for tgt_ceacam5

来源：同一对话 [CRC临床适应症地图](https://chatgpt.com/g/g-p-68c041b4df6881918a83a55e2dd7ac70/c/6a7a21a5-9474-83ea-895e-859b789fbe7c)。三轮审核；正式 review 同样因 GitHub 连接器 403 无法写回 PR，记录只保存在这里。

初审 head `2fdb7d8`：网页版 ChatGPT 结论：**REQUEST_CHANGES**。整体设计方向合理（reference 用 tumor-site immune cell 而非 PBMC 避免 batch confound；threshold 用 held-out reference half 的 99th percentile，不是看完结果再选阈值），但暴露六个接口/语义问题：(1) `resolve_hgnc_path()` 硬编码 `HGNC_GENE_ID_MAPPING_PATH` 字符串，没有真正从 `config/external_sources.yaml` 读取——PR #72 round 1 已经出现过的同类 bug 复发；(2) 外部 HGNC 参考文件没有 checksum/version/source-date lock，同一个 commit 未来可能因为外部数据库更新而得到不同结果；(3) fit-half/holdout-half 记账自相矛盾——threshold 正确地来自 held-out half，但报告的"reference"对比数字（median 0.68）实际来自 fit half，且错误地把 fit half 的 99th percentile说成"就是 threshold，by construction"（实际 threshold 来自 holdout half，两个 half 只是同一群体的独立随机子集，不是构造性相等）；(4) "~1% of epithelial-proxy cells clear threshold"表述具有误导性——threshold 本身定义为 reference 的 99th percentile，~1% 是零假设期望值，没有同时报告 reference 自身在同一阈值下的 exceedance 就无法判断 epithelial tail 是否真的 enriched；(5) 输出文件名 `tgt_ceacam5_cnv_confirmed_prevalence.tsv` 和 console 文案"CNV-confirmed"都用了"confirmed"，与 PR 自己"not confirmatory"的结论矛盾，被指出这种 filename 比正文 disclaimer 更容易误导未来的 agent；(6) 科学解释把方法失效主因归为"no cross-cell smoothing"，但真实 InferCNV 的核心流程是在单个 cell 内部沿基因组顺序做 moving-window smoothing，再做 centering/reference-subtraction，cross-cell clustering/HMM 只是可选的下游精化步骤，不是主要区分机制；外加一个数字笔误（25,390 应为 25,376）。

修正 head `97c6aa7`（round 2）：全部七项修复——`resolve_hgnc_path()` 改为真正解析 YAML（新增 `load_gene_position_source_config()`，镜像 `build_target_seed_universe.py` 的既有写法）；新增 `DATA/reference/hgnc_gene_id_mapping_source_lock.tsv`（SHA256 checksum lock），运行时强校验；所有"reference"对比数字统一改用 held-out half（median 0.68→held-out half 的真实值，明确标注 n_holdout=38,281）；exceedance 表述改为精确计数（epithelial-proxy 122/9,973=1.22% vs held-out reference 自身 382/38,281=1.00%，enrichment ratio 1.23x）；输出文件改名为 `tgt_ceacam5_cnv_lite_attempt.tsv`，console 文案改为"CNV_HIGH exploratory subset"；科学解释改为准确描述缺失的 gene-order local structure / within-chromosome moving-window smoothing / centering-reference-subtraction pipeline / 可选 subclustering-HMM，同时新增说明 arm-level mean(z²) 会抹掉 gain/loss 方向，谱系混淆与分辨率不足并列为同等可信的解释；25,390 改为 25,376。网页版 ChatGPT 复审：**REQUEST_CHANGES**——确认全部七项真正落地，但发现一个新 blocker：`TE006`/`EV014` 的 `indication_id=mcrc_preop_chemotherapy_crlm` 是 treated territory（与 `TE004` 一致），但脚本的 reference 和 epithelial-proxy population 从未真正限定到 3 位 treated 患者（COL15/COL17/COL18）——两个 population 都把全部 6 位患者混在一起，导致报告的 n=9,973 epithelial-proxy 统计量里 82%（8,187/9,973）实际是 treatment-naive 患者的细胞，却被写进 treated-only dossier。与 PR #74 round 1 发现的 cohort-mismatch bug 是同一类问题。要求最小修复：canonical `TE006` 统计量只用 treated 三患者数据（reference 也建议同样限定，因为 treatment 本身会改变 immune transcriptional program），六患者 pooled 版本可保留为 analysis contract 里的 method diagnostic 但不能是 canonical 数字；另外要求同步 GitHub PR title/description（仍是 round 1 的"underpowered"旧文案，与已修正的 head 矛盾）。明确不要求这轮扩大方法学 scope（换 reference、真跑 InferCNV、加 clustering 等），接受 treated-only 重跑后不论得到什么真实数字。

最终修正 head `3b9cfde`（round 3）：新增 `build_populations()`/`score_population()` helper，把脚本拆成 canonical treated-only run（reference 和 epithelial-proxy 都限定到 COL15/COL17/COL18）与 pooled 六患者 diagnostic run（明确标注非 canonical，只打印到 stderr，不写入输出 TSV 或 TE006/EV014）；在 LOCAL 重跑得到真实 treated-only 数字：reference n=38,003（held-out half n=19,002），threshold=12.54，epithelial-proxy n=1,786，median 1.32 vs held-out reference median 0.63（~2.1x），CNV_HIGH 36/1,786(2.02%) vs held-out reference 自身 190/19,002(1.00%)，enrichment ratio 2.02x（比之前误报的 pooled 1.23x 略强，但仍远非明确分离）；同步到 analysis contract、TE006/EV014、module README/data_lock/question、`knowledge/README.md`、`PROJECT_STATUS.md`；GitHub PR title 从"underpowered, not confirmatory"改为"ambiguous, not confirmatory"，description 同步为 round-3 数字并新增 Review history 小节。网页版 ChatGPT 最终结论：**APPROVE**——确认 cohort mismatch 是从执行层真正修掉（canonical pipeline 同时限定 reference 和 epithelial-proxy 到 treated 三患者，pooled run 明确只是 diagnostic），`indication_id` 与实际计算 population 完全一致，且没有因为 2.02x 比 pooled 1.23x"看起来更好"就升级 claim（仍是 `UNCALIBRATED_PROXY`/`EXPLORATORY_UNDERPOWERED`/`LOW`，明确写成"observed CNV-like score shift with ambiguous, nonconfirmatory signal"）。指出一个不阻断的小问题：`evidence_level` 仍叫 `EXPLORATORY_UNDERPOWERED`，但更精确的结论是"ambiguous because resolution + lineage confounding"，不只是 power 不足——但认为不值得为此重新设计受控词表来挡这个 PR，claim/notes 已经把真实含义表达清楚。建议下一步停止继续优化 CNV-lite（v2/v3 局部优化风险），认为比起在同一个 6 患者旧 cohort 上追求更漂亮的 malignancy calling，解除 `GSE225857`（第二个独立、治疗暴露的 CRLM cohort）的数据访问 blocker 更可能真正降低 CEACAM5 transfer hypothesis 的残余不确定性。

## PR #76 Module B + E for the remaining four targets (ERBB2, F3, NECTIN4, TACSTD2)

来源：同一对话 [CRC临床适应症地图](https://chatgpt.com/g/g-p-68c041b4df6881918a83a55e2dd7ac70/c/6a7a21a5-9474-83ea-895e-859b789fbe7c)。三轮审核；正式 review 同样因 GitHub 连接器 403 无法写回 PR，记录只保存在这里。用户明确指示做这个 PR：优先横向跑通另外四个有 ADC precedent 的 target，覆盖了 PR #75 reviewer 之前"先别 batch-run"的建议（那是建议不是硬约束）。

初审 head `651ae72`：网页版 ChatGPT 结论：**REQUEST_CHANGES**。横向跑四个 target 这件事本身没有问题（reviewer 明确认可用户的 breadth-first scope 决策，不拿旧建议挡 PR），Module B 部分也基本认可（epithelial-proxy、treated/untreated 分开、没有复制 CNV-lite、NECTIN4→PVRL4 alias 显式处理都对）；问题集中在 Module E 的 evidence semantics 和 interpretation，三类：(1) F3 的 IHC 缺失（`Tissue=N/A`/`Level=N/A`/`Reliability=Uncertain`/`usable_data=NONE`）被错误编码成 `evidence_directness=UNCALIBRATED_PROXY`——"没有证据不能被编码成弱证据"，应该是 `UNKNOWN`；(2) 把 HPA normal-expression screen 升级成了没有 provenance 的 clinical-toxicity causal validation——最明显是 ERBB2 从"cardiomyocytes/lung alveolar cells Medium"直接跳到"well-documented cardiac and pulmonary...toxicities"和"reproduces a known, real liability"，NECTIN4/TACSTD2/F3 也有同类"matches known biology/toxicity"表述；其中 TACSTD2 那条不只是缺 citation，是事实错误——sacituzumab govitecan 的 urothelial cancer 适应症已在 FDA 2024 年批准信里记录为 sponsor 自愿撤回（当前只有 breast cancer），且真正的 boxed warning 是 neutropenia/diarrhea 不是 skin/mucosal toxicity；(3) 两处内部矛盾——"TACSTD2 是五个 target 里唯一有 IHC High 的"（错，CEACAM5 在 PR #73 已有 12 个 High rows）、NECTIN4/TACSTD2 都在同一句话里先列出 Esophagus:squamous=Medium 又说"no GI tissue scored High/Medium"（esophagus 本身就是 GI tract）。要求：不重新跑数据，只做 claims/编码修正。

修正 head `bd7eff2`（round 1）：TE014 改为 `UNKNOWN`；去掉 ERBB2/NECTIN4/TACSTD2 canonical claim 里没有 provenance 的 clinical-toxicity causal 声明；修正 TACSTD2 question.md 的 Trodelvy 适应症/毒性事实错误；"only IHC-High among five"改成"新增四个里唯一，CEACAM5 已有 12 个"；"no GI tissue"改成"colon/rectum/small intestine 具体偏低，esophagus 等上消化道有真实 Medium 信号"。网页版 ChatGPT 复审：**REQUEST_CHANGES**——确认大部分修复落地正确（TE014/GI-wide/IHC-High comparison 都对），但剩三个很小的 consistency blocker：(1) canonical evidence 里仍残留没有 provenance 的 external clinical/biology claims——ERBB2 的 TE009/EV017 仍把 cardiomyocytes/alveolar cells 称为"clinically-monitored toxicity domains for approved anti-HER2 ADCs"（即使加了"不做 causal claim"声明，这句话本身仍是外部事实）；F3 的 TE012/EV020 和 analysis contract 仍写"matches known F3 biology"；F3/TACSTD2 的 question.md 即使事实已经修正，仍在断言外部临床事实而非引用已有的 Module A 记录；(2) TE022/EV030 有字面自相矛盾"skin is the single highest, but esophagus is higher still"；(3) GitHub PR description 仍是 round 0/1 旧文案。明确不要求重新跑数据、不要改 Module B。

最终修正 head `491794f`（round 2）：清掉 ERBB2/F3 canonical evidence 里残留的 external clinical/biology claims；四个 target 的 question.md 全部重写为引用 Module A（`ADC_TARGET_SEED_UNIVERSE.tsv`，已有 source-verified 记录）而非在 Module E 重述药物/适应症/机制事实；修正 TE022/EV030 的"single highest"字面矛盾为"esophagus 最高，skin/urinary bladder/salivary gland/tonsil 也是显著信号"；GitHub PR description 同步到当前 head 真实状态。网页版 ChatGPT 最终结论：**APPROVE**——确认上一轮三个 blocker 全部真正消失：F3/TE014 正确编码为 `UNKNOWN` 且保留 `usable_data=NONE`，"没有把缺证据继续伪装成弱 proxy"；ERBB2 canonical IHC row 现在只报告 HPA 自身观察到的 expression，不再用 clinical toxicity domain 做外部解释；四个 question.md 都已把 ADC precedent 回指 Module A；TACSTD2 的 HPA claim 逻辑一致，同时准确保留"colon/rectum low 但不是 GI-wide low"；TACSTD2 的 High-IHC comparison 限定为"本 PR 新增四个 target 中唯一"，同时列出 CEACAM5 已有的 12 个 High rows。给了一条不阻断的措辞点：TE022 把 bulk RNA 总结成"broad non-colorectal epithelial expression"，严格说 bulk RNA 本身只能证明 normal-tissue expression 不能单独证明来自 epithelial cells，但同 dossier 的 TE024 IHC 确实提供了 epithelial cell-type support 且 TE022 已显式指向 TE024，不值得再挡一轮。明确下一步：五个 CRC-precedented target 现在都有同构的 Module B+E screening evidence，应该进入横向 decision/pruning（比较谁接近 KILL、谁 HOLD、谁值得进入下一模块），而不是继续为每个 target 堆同类证据。

## PR #77 横向 evidence-pattern comparison（五个 target）

来源：同一对话 [CRC临床适应症地图](https://chatgpt.com/g/g-p-68c041b4df6881918a83a55e2dd7ac70/c/6a7a21a5-9474-83ea-895e-859b789fbe7c)。四轮审核；正式 review 同样因 GitHub 连接器 403 无法写回 PR，记录只保存在这里。按 PR #76 round 3 reviewer 自己的建议做的横向比较：五个 target 现在证据同构，把已有证据并排读出来，没有新数据、没有重新跑脚本。

初审 head `40570d4`：网页版 ChatGPT 结论：**REQUEST_CHANGES**——scope 很干净（只新增比较报告，没有动原始 evidence），但真正的问题是把"五个 target 证据同构"进一步推成了"可以横向定量排序"，这一步不成立：(1) Module B 的跨 target prevalence ranking 没有校准——五个基因本身 transcript abundance/dropout propensity/dynamic range 不同，同一 pipeline 的 detection fraction 差异不能直接升级成"biological prevalence 更强/更弱"，更不能据此说 NECTIN4"weakest primary rationale"；(2) Module E 的 HPA IHC High/Medium 不能跨 target 当同一把尺——不同 target 用不同 antibody/staining，"TACSTD2 High"不能定量断言比"ERBB2 Medium"更强的 accessible antigen exposure，报告后段自己也承认"Module E cannot establish accessible antigen density"，前段却又用"single highest-intensity"、"risk/benefit least favorable"，语义上越过了自己的 evidence boundary；(3) CEACAM5 的 normal-tissue interpretation 有概念性方向错误——"normal-tissue signal 集中在 indication 自己的组织"不等于"normal-tissue risk 已经解决"，正常结直肠组织依然是正常组织，若 antigen 真正 accessible 依然可能有 on-target/off-tumor liability；把"跟癌种同一解剖部位"当成"比较没问题"是一个不应该被系统固化的危险 heuristic。建议把整份报告的定位从"target pruning lean"降为"evidence-based next-step prioritization"（下一步该往哪花钱/花算力，而不是哪个 target 该被淘汰）。

修正 head `aa3a140`（round 1）：Module B 一节改名为"cross-target observed RNA detection-fraction screen, not a calibrated prevalence ranking"，删掉决策性语言，保留原始表格和数字；Module E 一节只保留"within-target tissue/cell-type 数量分布"这个可以安全支持的比较，删掉所有跨 target 的强度/risk-benefit 语言；修正 CEACAM5 的概念性错误为"pattern is anatomically concentrated, safety implication remains unresolved"；整份文档从"target pruning lean"改成"next-uncertainty prioritization"：CEACAM5 下一步是独立 cohort/protein evidence，NECTIN4 下一步是验证低 detection fraction 是否复现，ERBB2/TACSTD2 需要 protein/surface-density evidence，F3 的 gap 是否值得填看其他轴。网页版 ChatGPT 复审：**REQUEST_CHANGES**——确认核心重构方向正确（title/body 已改成 horizontal evidence-pattern comparison / next-uncertainty prioritization，不再做 KILL/HOLD/SHORTLIST），但发现一个实质 blocker 加两个小语义问题：(1) round 1 新引入的"唯一允许跨 target 比较的量尺"（distinct tissues/cell types 数量）本身算错了——报告说 TACSTD2"spans the most distinct tissues/cell types"，但按同一张表重新数，ERBB2 实际涉及的 distinct tissues 更多（TACSTD2 9 个 vs ERBB2 13 个），这是直接事实错误，且既然要把这个 count 当唯一安全的跨 target 说法，必须先把单位定义清楚（"distinct HPA tissues with ≥1 High/Medium row"）再算对；(2) 文件名还叫`TARGET_PRUNING_COMPARISON.md`，与文档正文"not target pruning"的定位冲突，是未来 agent 的语义陷阱，建议改名；(3) "comparable Module B + E evidence"的措辞容易被读成"量尺可直接比较"，建议改成"structurally parallel"。外加一个非阻断措辞：Suggested next step 里"lowest-cost"没有成本分析支撑（CEACAM5 建议的下一步 GSE225857 本身还被 CNSA access 卡住），应删掉。

修正 head `400be1d`（round 2）：按建议的固定单位重新数了一遍 distinct HPA tissues with ≥1 High/Medium row：ERBB2=13、TACSTD2=9、CEACAM5=6、NECTIN4=6、F3=unmeasured，替换掉原来错的"TACSTD2 most distinct"表述；文件改名为`TARGET_EVIDENCE_PATTERN_COMPARISON.md`，同步更新 README.md 链接；"comparable"改成"structurally parallel"；删掉"lowest-cost"改成"highest-information next checks under the current plan"。网页版 ChatGPT 复审：**REQUEST_CHANGES**——确认 round 1 三项核心修复都正确落地，tissue-count 也按固定单位重新算对，但在重新读修正后的表时发现一个新的、局部的直接矛盾：正文紧接着说"CEACAM5's narrow count sits entirely inside colorectal/appendix tissue"，但同一张表列出的 CEACAM5 6 个 tissue 里还有 Esophagus/Oral mucosa/Stomach，不是"entirely"colorectal/appendix——这是 round 2 自己修表格时新造出来的矛盾，不是重复问题。要求区分 High-level calls（确实限于 Appendix/Colon/Rectum）与完整 High+Medium footprint（还包括 Esophagus/Oral mucosa/Stomach）两件事。

最终修正 head `8be320b`（round 3）：把那一句话拆成两句话说清楚——High-level IHC calls 限于 Appendix/Colon/Rectum，完整 High+Medium footprint 还包括 Esophagus/Oral mucosa/Stomach，准确表述改为"GI/oral-mucosal concentrated"而非"entirely colorectal/appendix"。网页版 ChatGPT 最终结论：**APPROVE**——重新通读确认前几轮建立的所有 evidence boundary 都保持住了：Module B 明确是 per-gene RNA detection fraction 不冒充 calibrated biological prevalence；Module E 的 High/Medium 不再跨 antibody 当统一强度标尺；跨 target tissue breadth 用固定单位（ERBB2 13、TACSTD2 9、CEACAM5 6、NECTIN4 6、F3 unmeasured）且内部一致；CEACAM5 的解剖集中性没有再被错误解释成安全窗口；F3 继续保持真正的 UNKNOWN；最终输出是 next-uncertainty prioritization 而不是 KILL/HOLD/SHORTLIST。提到一处不值得再改的措辞（CEACAM5 段"RNA detection is the most stable of the five in this assay"仍有一点像跨 target judgement，但已限定"in this assay"且全文反复锁定不能解释成 prevalence，不构成 blocker）。总结这份报告的真正价值：不是给五个 target 排名，而是第一次把"已有证据还缺什么"变成了 target-specific 的下一步 acquisition strategy。

## PR #78 GSE225857 CNSA 访问条款审查

来源：同一对话 [CRC临床适应症地图](https://chatgpt.com/g/g-p-68c041b4df6881918a83a55e2dd7ac70/c/6a7a21a5-9474-83ea-895e-859b789fbe7c)。三轮审核；正式 review 同样因 GitHub 连接器 403 无法写回 PR，记录只保存在这里。用户明确选择这个方向：PR #77 完成后所有 target 的下一步都指向"需要更多证据"，其中 CEACAM5/多个 target 共同依赖的 `GSE225857`（第二个独立 CRLM cohort）访问条款此前只有一个未审核的 placeholder，值得先解决。

初审 head `46ca3d5`：独立复核 `GSE225857` 的 CNSA/CNGBdb 访问条款（原记录的 `source_url` 是 404 死链，重新找到真实的 `db.cngb.org` project 页面）。网页版 ChatGPT 结论：**REQUEST_CHANGES**——三个真实问题，不是措辞挑剔：(1) 结论"扩展 Module B 需要 DAC 申请"过度断言——网页版 ChatGPT 自己独立核实了 `GSE225857` 自己的 GEO 页面，发现 GSM7058754（immune）/GSM7058755（non-immune）各自公开提供可下载的 count matrix + per-cell metadata，不需要访问申请；这是一条真实的、未验证是否够用的更便宜的替代路径，"必须走 DAC"这个结论没有资格成立；(2)"outside what this repository or its operator can satisfy directly (no Chinese-institution affiliation on record here)"是一个没有支撑的资格推断——CNGBdb policy 原文只说 controlled data 接受用户申请，受 submitter 批准和适用法律/HGR compliance 约束，没有写机构国籍门槛；(3) `CNP0002540`（scRNA-seq）和 `CNP0003321`（spatial transcriptomics）两个不同 modality 的 accession 被挤进一行 provenance 记录，只有一个 accession 的 `source_url`，可追溯性不足，应该拆成独立行，跟 `GSE117548` 的 EGA 行是同一套模式。

修正 head `408fb36`（round 1）：独立重新核实了 GEO 上 GSM7058754/GSM7058755 的 per-GSM supplementary files（213.9MB+9.6MB、86.2MB+1.9MB，GEO 自己的 Data Processing 字段写"Matrix table with raw UMI counts and metadata for every cells"），确认 reviewer 的事实完全准确后才动手改；把"CNSA route 是 CONTROLLED_ACCESS"这个已确认事实和"是否需要走 CNSA 才能扩展 Module B"这个未验证推断分开，后者改写为 UNKNOWN，真正的下一步记录为"先检查两个公开 meta.txt.gz 文件的列结构"；删掉没有支撑的机构国籍资格推断，只保留 policy 原文实际说的；`CNP0002540`/`CNP0003321` 拆成两个独立 provenance row，各自有完整的 source_url/size/access notes。网页版 ChatGPT 复审：**REQUEST_CHANGES**——确认上一轮三个核心问题真正修掉，但指出一个新的、更细的 provenance 语义问题：round 1 的修复本身仍然把"raw sequencing data"和"raw UMI count matrix"混用——GEO 对 GSM7058754 的页面同时写"Matrix table with raw UMI counts and metadata"和"Raw data not provided for this record / Processed data provided as supplementary file"，也就是说这两个文件数值上是 raw（未标准化）UMI counts，但文件本身属于 processed supplementary data，不是 raw sequencing reads；真正受 CNSA controlled access 约束的是 sequencing-level raw data。要求最小修改：GEO 的公开路径统一称为"public processed count-matrix + per-cell metadata route"，不再称"public raw-data route"；CNSA 明确叫"raw sequencing-data route"；`no_file_inventory_disposition.tsv` 里"not a raw-access blocker"改成"publicly accessible processed count/meta files are available without an access request"；PR 标题从"confirmed real CONTROLLED_ACCESS blocker"收窄为"GSE225857 CNSA raw-data access review -- CONTROLLED_ACCESS; public GEO processed route remains open"，因为 controlled-access blocker 是 CNSA raw-sequencing route 的属性，不是 `GSE225857` 整体的数据可用性 blocker。除此之外确认 next artifact 定义正确（先用约 12MB 公开 metadata 判断是否需要碰 2.7TB controlled raw-data route，而不是反过来）。

最终修正 head `c17a0e3`（round 2）：`source_manifest.tsv`/`no_file_inventory_disposition.tsv`/`PROJECT_STATUS.md`/`knowledge/README.md`/`data_lock/tgt_ceacam5.md` 五处统一按 reviewer 的精确措辞修正——"raw UMI count matrix"改为"processed count matrix (raw UMI counts, per GEO's own field name)"，"a real, public alternative route to...raw data"改为"a public processed count-matrix + per-cell metadata route, not a public raw-sequencing-data route"，"not a raw-access blocker"改为"publicly accessible processed count/meta files are available without an access request"，CNSA 两行统一改称"raw sequencing-data route"；PR 标题按建议收窄。`data_lock/tgt_erbb2.md` 本来就没有"raw"字样的混用，未改动。网页版 ChatGPT 最终结论：**APPROVE**——确认上一轮唯一 blocker 真正修掉，provenance boundary 现在清楚：GEO 是公开的 processed count-matrix + per-cell metadata（矩阵数值是 raw UMI counts 但文件属于 processed supplementary data）；CNSA 是 raw sequencing-data route，`CNP0002540`/`CNP0003321` 分别记录，均 CONTROLLED_ACCESS；CNSA controlled access 不等于 `GSE225857` 整体不可用于 Module B，公开 GEO route 是否足够仍保持 UNVERIFIED，没有再发生"raw UMI counts → raw sequencing data"这种 provenance 层级偷换；`no_file_inventory_disposition.tsv` 的 next artifact 也已经是正确的最小信息增益动作。提到一处非阻断的小措辞（`tgt_ceacam5.md` 把 spatial 也包进"single-cell sequencing data"不够精确，但同句已明确标注 `CNP0003321` spatial，不构成实际 provenance 判断错误，不值得再挡一轮）。明确下一步：不是继续做 access archaeology 也不是申请 DAC，而是直接做一个很小的 GEO metadata sufficiency check——检查 `GSM7058754_immune_meta.txt.gz`/`GSM7058755_non_immune_meta.txt.gz` 是否已经带 patient/site/treatment labels；如果够用，`GSE225857` 这个所谓的 institutional-access blocker 可能直接消失。
