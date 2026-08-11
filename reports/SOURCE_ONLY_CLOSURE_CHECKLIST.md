# Source-only project closure checklist

This checklist defines completion for the current project phase. It does not require downloading or analyzing biological data.

## Completion criteria

- [x] Repository scope explicitly excludes biological data and analysis.
- [x] Candidate registry, source manifests, file inventories and metadata contracts exist.
- [x] Processed-first and no-raw-download rules are documented.
- [x] Offline checksum capture is available for future explicitly staged files.
- [x] Weekly source scan and pinned GitHub metadata scan are configured.
- [x] CI validates registry structure, offline scan stability and regression tests.
- [x] P0 gates have artifacts, source evidence, stop conditions and remaining blockers.
- [x] PR history and the single ChatGPT review conversation are archived.
- [ ] Every candidate has complete source-level file metadata; blocked candidates retain explicit UNKNOWN/NA fields and a next artifact.
- [x] Candidate-level source manifest, file inventory, download-method and update-coverage dispositions are materialized in `SOURCE_ONLY_CLOSURE_MATRIX.tsv`, with internal artifact gaps separated from external blockers.
- [x] Every configured update target has completed first scan and drift disposition in `reports/updates/UPDATE_TARGET_DISPOSITION.tsv`.
- [x] Final closure PR confirms all remaining internal blockers are closed, all remaining dataset-review handoffs are documented, and no biological data is present.

## Definition of done

The source-only phase is complete only when all internal requirements in `config/project_completion.yaml` are complete. Upstream access, missing public metadata and absent user-staged files may remain as external blockers, but they must be recorded in the closure matrix with a named next artifact. Internal work such as the first scan disposition, validator/test run, no-data audit and final closure PR cannot be waived as an external blocker. `APPROVED` is not required for this phase and must not be inferred from source-only completion.

- [x] Source-only boundary audit and CI guardrail are present; the latest audit is recorded in `reports/SOURCE_ONLY_FINAL_AUDIT.tsv`.
- [x] A source-manifest candidate may use a tracked `no_file_inventory_disposition.tsv` when exact file-level inventory is intentionally not asserted; this is not equivalent to `APPROVED` or to a biological-data result.

## Post-closure handoff

The source-only endpoint is complete. Remaining `SOURCE_INDEXED_REVIEW_REQUIRED` rows are dataset-specific handoffs and do not reopen this phase. Any future file staging, candidate approval, biological analysis or clinical interpretation requires a new scoped change and review.
