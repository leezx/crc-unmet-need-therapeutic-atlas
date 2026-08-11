# GitHub target update candidates

`github_tree_update_candidates.tsv` is metadata-only evidence from the weekly scan. A row with `update_available=TRUE` means the configured tracking ref moved beyond the pinned commit; it does not approve the new commit and does not download any files.

Reviewers must inspect the new commit and update `config/github_tree_targets.tsv` only through a separate reviewed change. The weekly workflow may open a draft PR when this report changes.
