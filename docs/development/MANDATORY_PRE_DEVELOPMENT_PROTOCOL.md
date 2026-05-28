# Mandatory Pre-Development Protocol

This protocol is mandatory before every V1700 proposal, blueprint, roadmap, implementation, gate change, release packaging task, post-release integrity repair, and web-to-local handoff closure.

It translates the `literary-os` workflow model into GPT-native V1700 rules. In `v1700`, the equivalent rule is stronger than "run tests before coding." It means that planning, design, and stage work do not start until GitHub authority, session context, stage lineage, gate visibility, and release-asset authority are all re-confirmed.

## Canonical Documents

The following documents are authoritative and must be treated as one linked policy set:

- `docs/development/MANDATORY_PRE_DEVELOPMENT_PROTOCOL.md`
- `docs/workflow/PREFLIGHT_GUIDE_v1.1_GPT_STAGE.md`
- `docs/workflow/SESSION_PROTOCOL.md`
- `docs/workflow/BRANCH_STRATEGY.md`
- `docs/workflow/WORKFLOW.md`
- `manifests/predevelopment_priority_manifest.json`

## Source Authority

The workflow philosophy is derived from the external `literary-os` workflow documents, then translated into GPT/V1700 operating rules:

- `PREFLIGHT_GUIDE_v1.1.md`
- `WORKFLOW.md`
- `BRANCH_STRATEGY.md`

The external repository remains unchanged. V1700 carries an internal translation that fits Stage lineage, release gates, repo doctor, package manifests, and Provider-Zero invariants.

## Priority

This document has priority over any stage-specific proposal or implementation note. A new Stage is not complete unless its logic is connected to:

- proposal and blueprint documents
- manifests, lineage records, and branchpoint traces
- tests and stage gate evidence
- release gate and repo doctor recognition
- GitNexus analysis or documented Python fallback
- clean package, checksum, and release assets

## Non-Negotiable Start Rule

Before touching code, docs, proposals, or blueprints, every session must perform the following:

```text
1. Pull or verify the latest remote state from GitHub.
2. Confirm current main, latest relevant Stage tag, and active working branch.
3. Read the latest session note in docs/sessions/ when relevant.
4. Read this protocol and the Stage-specific proposal and blueprint.
5. Run `python tools/session_start.py`.
6. Run `python tools/run_mandatory_predevelopment_check.py`.
7. Refresh GitNexus, or record Python fallback as the active authority.
```

This rule applies twice:

- before planning or drafting a new proposal/blueprint
- before starting code or document work for a specific Stage

## Fixed GPT Preflight Sequence

```text
1. Read the canonical workflow documents.
2. Confirm GitHub main, tags, and local branch state.
3. Run `python tools/session_start.py`.
4. Run `python tools/run_mandatory_predevelopment_check.py`.
5. Run `gitnexus.cmd status`; if stale or missing, run `gitnexus.cmd analyze --force`.
6. Inspect target symbols, processes, and branchpoint lineage.
7. Review concept impact on provider-zero, write-zero, privacy-zero, and Stage lineage.
8. Confirm proposal and blueprint exist or create/update them first.
9. Define or update contracts, manifests, tests, release evidence, and branchpoint trace.
10. Implement in small steps.
11. Run the stage-specific gate.
12. Run `python tools/run_release_gate.py`.
13. Run `python tools/run_stage72_repo_doctor.py`.
14. Run the relevant pytest pack.
15. Re-index GitNexus after material code changes.
16. Regenerate `SHA256SUMS.txt` through `python tools/regenerate_sha256sums.py` so checksum authority stays platform-neutral.
17. Build the clean ZIP, sidecar SHA256, and verify re-extraction before handoff or release.
18. Record session closure through docs and `python tools/session_end.py`.
```

## Hook And Session Enforcement

The V1700 translation of the `literary-os` hook model is:

- `python tools/install_predevelopment_hooks.py`
- `powershell -File tools/install_predevelopment_hooks.ps1`
- `bash tools/install_predevelopment_hooks.sh`

The installed hooks are expected to block commits or pushes when:

- the mandatory predevelopment protocol is broken
- staged changes introduce `DEV_MODE=True`
- staged changes introduce non-zero provider or leakage counters
- a larger Python change set fails the repository release gate

## Branch And Release Rule

- work starts from `main` or a sealed authority package explicitly mirrored into a fresh branch
- each task uses a dedicated branch
- the branch is pushed before review
- GitHub Actions must be green before merge
- merge to `main` happens before tag and release
- official release authority is `commit + tag + release assets`
- official release assets are `ZIP + .sha256 + SHA256SUMS.txt`
- session closure requires push when a meaningful work unit is finished

## Web-To-Local Handoff Rule

When web development reaches a partial or connector-limited state, local Codex becomes the authority-finishing environment. Before PR closure:

- mirror the web branch contents into a clean local branch
- run the full GPT preflight sequence again
- regenerate release evidence and checksum authority locally
- only then push, review, merge, tag, and publish

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
- `session_start_required = true`
- `session_end_required = true`
- `hook_install_available = true`
