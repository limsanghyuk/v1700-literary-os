# Mandatory Pre-Development Protocol

This protocol is mandatory before every V1700 proposal, blueprint, roadmap, implementation, gate change, release packaging task, and post-release integrity repair.

It upgrades the original V1700 predevelopment policy with the `literary-os` workflow `V1.1` approach and translates that approach into V1700 Stage rules.

## Canonical Documents

The following documents are authoritative and must be treated as one linked policy set:

- `docs/development/MANDATORY_PRE_DEVELOPMENT_PROTOCOL.md`
- `docs/workflow/PREFLIGHT_GUIDE_v1.1_STAGE160.md`
- `docs/workflow/BRANCH_STRATEGY.md`
- `docs/workflow/WORKFLOW.md`
- `manifests/predevelopment_priority_manifest.json`

## Priority

This document has priority over any stage-specific proposal or implementation note. A new Stage is not complete unless its logic is connected to:

- proposal and blueprint documents
- manifests and lineage records
- tests and stage gate evidence
- release gate and repo doctor recognition
- GitNexus or documented fallback analysis
- clean package, checksum, and release assets

## Session Start Rule

Before touching code or docs, every session must perform the following:

```text
1. Pull or verify the latest remote state from GitHub.
2. Confirm current main, latest relevant Stage tag, and active working branch.
3. Read the latest session note in docs/sessions/ when relevant.
4. Read this protocol and the Stage-specific proposal and blueprint.
5. Run the mandatory predevelopment check.
6. Refresh GitNexus, or record Python fallback as the active authority.
```

## Fixed Preflight Sequence

```text
1. Read the canonical workflow documents.
2. Confirm GitHub main, tags, and local branch state.
3. Run `python tools/run_mandatory_predevelopment_check.py`.
4. Run `gitnexus.cmd status`; if stale or missing, run `gitnexus.cmd analyze --force`.
5. Inspect target symbols, processes, and branchpoint lineage.
6. Review concept impact on provider-zero, write-zero, privacy-zero, and Stage lineage.
7. Confirm proposal and blueprint exist or create/update them first.
8. Define or update contracts, manifests, tests, release evidence, and branchpoint trace.
9. Implement in small steps.
10. Run the stage-specific gate.
11. Run `python tools/run_release_gate.py`.
12. Run `python tools/run_stage72_repo_doctor.py`.
13. Run the relevant pytest pack.
14. Re-index GitNexus after material code changes.
15. Build the clean ZIP, sidecar SHA256, and verify re-extraction before handoff or release.
```

## Branch And Release Rule

- work starts from `main`
- each task uses a dedicated branch
- the branch is pushed before review
- GitHub Actions must be green before merge
- merge to `main` happens before tag and release
- official release authority is `commit + tag + release assets`
- official release assets are `ZIP + .sha256 + SHA256SUMS.txt`

## Non-Negotiable Invariants

- `provider_default_calls = 0`
- `live_provider_call_count_in_release_gate = 0`
- `node2_raw_reveal_access = 0`
- `reader_only_leakage = 0`
- `internal_marker_leakage = 0`
- `raw_manuscript_provider_leakage = 0`
- `credential_leakage = 0`
- `branchpoint_lineage_preserved = true`
- `python_fallback_required = true`
- `gitnexus_runtime_dependency_required = false`
- `github_main_green_required = true`
- `release_assets_triplet_required = true`
