# Page15 Local GitNexus Execution Guide

Status: local validation guide
Created: 2026-06-03
Page: Page15 — Collaboration / Review Share Boundary
Stage range: Stage225~Stage230
Branch: roadmap-page08-page17-commercial-absorption

## Purpose

This guide tells local Codex how to validate the Page15 fallback-backed implementation and convert it into recorded GitNexus evidence.

The web-side result is intentionally not marked `PASS_WITH_GITNEXUS_OUTPUT`.

## Required first-read files

```text
docs/development/MANDATORY_PRE_DEVELOPMENT_PROTOCOL.md
docs/architecture/web_fallback_development_blueprint.md
docs/development/gitnexus_index_result_storage_protocol.md
docs/architecture/page15_blueprint.md
docs/proposals/page15_collaboration_review_share_proposal.md
docs/architecture/page15_gate_alignment_note.md
release/current/page14_release_gate_report.md
release/current/stage224_gitnexus_evidence_report.json
release/current/page15_release_gate_report.md
```

## Required local commands

Run from repository root:

```bash
git fetch --all --tags --prune
git checkout roadmap-page08-page17-commercial-absorption
git pull --ff-only origin roadmap-page08-page17-commercial-absorption
python tools/session_start.py
python tools/run_mandatory_predevelopment_check.py
python tools/check_stage_metadata_consistency.py
python tools/check_release_asset_integrity.py
python tools/run_release_gate.py
python tools/run_stage72_repo_doctor.py
gitnexus.cmd analyze --force
gitnexus.cmd status
```

Alternative GitNexus command names are allowed only if they refer to the same local GitNexus runtime:

```bash
gitnexus analyze --force
gitnexus status
```

## Required evidence paths

For Page15, store GitNexus output under:

```text
release/gitnexus/stage230/gitnexus_index_report.json
release/gitnexus/stage230/gitnexus_status.txt
release/gitnexus/stage230/gitnexus_analyze_log.txt
release/gitnexus/stage230/gitnexus_summary.md
manifests/gitnexus/stage230_symbol_connectivity.json
manifests/gitnexus/stage230_orphan_symbol_report.json
manifests/gitnexus/stage230_successor_trace_matrix.json
release/current/stage230_gitnexus_evidence_report.json
```

If validating the whole page instead of the seal stage, also create page-level aliases:

```text
release/gitnexus/page15/gitnexus_index_report.json
manifests/gitnexus/page15_symbol_connectivity.json
manifests/gitnexus/page15_orphan_symbol_report.json
manifests/gitnexus/page15_successor_trace_matrix.json
release/current/page15_gitnexus_evidence_report.json
```

## Required trace checks

At minimum, confirm:

```text
Page14 -> Page15
Stage224 -> Stage225
Stage225 -> Stage226
Stage226 -> Stage227
Stage227 -> Stage228
Stage228 -> Stage229
Stage229 -> Stage230
Stage230 -> Page16 design handoff
```

## Blocking failures

Do not promote Page15 if any of these occur:

```text
review-share projection can mutate canonical story state
external comment becomes canonical story state
Page16 export behavior appears in Page15
Page14 dependency is missing
Stage224 GitNexus evidence is ignored
Page10~Page13 warnings disappear without refreshed evidence
orphan critical node count is non-zero
```

## Update rule

Only after local GitNexus evidence is committed may Page15 change from:

```text
PASS_WITH_APPROVED_FALLBACK_PENDING_GITNEXUS
```

to:

```text
PASS_WITH_GITNEXUS_OUTPUT
```

Terminal output alone is not evidence. Evidence must be pushed to the hub.
