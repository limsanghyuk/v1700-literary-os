# Page16 Local GitNexus Execution Guide

Status: local validation guide
Created: 2026-06-04
Page: Page16 — Screenplay / Production Bridge
Stage range: Stage231~Stage235
Branch: roadmap-page08-page17-commercial-absorption

## Purpose

This guide tells local Codex how to validate the Page16 fallback-backed implementation and convert it into recorded GitNexus evidence.

The web-side result is intentionally not marked `PASS_WITH_GITNEXUS_OUTPUT`.

## Required first-read files

```text
docs/development/MANDATORY_PRE_DEVELOPMENT_PROTOCOL.md
docs/architecture/web_fallback_development_blueprint.md
docs/development/gitnexus_index_result_storage_protocol.md
docs/architecture/page16_screenplay_production_bridge_blueprint.md
docs/proposals/page16_screenplay_production_bridge_proposal.md
release/current/page15_release_gate_report.md
release/current/stage230_gitnexus_evidence_report.json
release/current/page16_release_gate_report.md
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

For Page16, store GitNexus output under:

```text
release/gitnexus/stage235/gitnexus_index_report.json
release/gitnexus/stage235/gitnexus_status.txt
release/gitnexus/stage235/gitnexus_analyze_log.txt
release/gitnexus/stage235/gitnexus_summary.md
manifests/gitnexus/stage235_symbol_connectivity.json
manifests/gitnexus/stage235_orphan_symbol_report.json
manifests/gitnexus/stage235_successor_trace_matrix.json
release/current/stage235_gitnexus_evidence_report.json
```

If validating the whole page instead of the seal stage, also create page-level aliases:

```text
release/gitnexus/page16/gitnexus_index_report.json
manifests/gitnexus/page16_symbol_connectivity.json
manifests/gitnexus/page16_orphan_symbol_report.json
manifests/gitnexus/page16_successor_trace_matrix.json
release/current/page16_gitnexus_evidence_report.json
```

## Required trace checks

At minimum, confirm:

```text
Page15 -> Page16
Stage230 -> Stage231
Stage231 -> Stage232
Stage232 -> Stage233
Stage233 -> Stage234
Stage234 -> Stage235
Stage235 -> Page17 design handoff
```

## Blocking failures

Do not promote Page16 if any of these occur:

```text
screenplay projection changes canonical manuscript state
production packet is treated as final authority without a future approval contract
Page17 plugin or learning behavior appears in Page16
Page15 dependency is missing
Stage230 GitNexus evidence is ignored
Page10~Page13 warnings disappear without refreshed evidence
orphan critical node count is non-zero
```

## Update rule

Only after local GitNexus evidence is committed may Page16 change from:

```text
PASS_WITH_APPROVED_FALLBACK_PENDING_GITNEXUS
```

to:

```text
PASS_WITH_GITNEXUS_OUTPUT
```

Terminal output alone is not evidence. Evidence must be pushed to the hub.
