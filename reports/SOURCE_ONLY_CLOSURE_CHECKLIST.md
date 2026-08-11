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
- [x] Candidate-level source manifest, file inventory, download-method and update-coverage dispositions are materialized in `SOURCE_ONLY_CLOSURE_MATRIX.tsv`.
- [ ] Every update target has completed first scan and drift disposition.
- [ ] Final closure PR confirms all remaining blockers are documented and no biological data is present.

## Definition of done

The source-only phase is complete only when all internal requirements in `config/project_completion.yaml` are complete. Upstream access, missing public metadata and absent user-staged files may remain as external blockers, but they must be recorded in the closure matrix with a named next artifact. Internal work such as the first scan disposition, validator/test run, no-data audit and final closure PR cannot be waived as an external blocker. `APPROVED` is not required for this phase and must not be inferred from source-only completion.

## Next closure batches

1. Normalize candidate-level closure and update-target coverage into one machine-readable matrix.
2. Add a validator rule that every candidate has a source manifest or an explicit missing-source disposition.
3. Run a first-scan disposition for every configured update target.
4. Run a final no-biological-data audit and archive the final ChatGPT review in the same conversation.
5. Merge the final closure PR; this internal step is mandatory even if upstream blockers remain.
