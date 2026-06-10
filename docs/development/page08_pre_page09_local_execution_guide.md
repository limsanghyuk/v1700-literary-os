# Page08 Pre-Page09 Local Execution Guide

Status: required local guide before Page09 entry
Created: 2026-05-29
Page: Page08 — Lineage / Hub / Formula Authority
Stage range: Stage186~190
Branch: stage186-page08-branchpoint-map

## Purpose

Page08 has been implemented as a scaffold and authority seed on the hub, but Page09 must not begin until local connectivity evidence is applied.

This guide tells a local developer or local Codex session exactly what to run and which files to update before Page09 commercial absorption begins.

## Required documents to read first

```text
docs/roadmaps/page08_page17_commercial_absorption_writer_studio_roadmap.md
docs/roadmaps/page08_page17_codex_ide_absorption_addendum.md
docs/roadmaps/page08_page17_page_blueprint_drafts.md
docs/proposals/page08_lineage_hub_formula_authority_proposal.md
docs/architecture/page08_lineage_hub_formula_authority_blueprint.md
docs/development/page08_codex_local_execution_guide.md
docs/development/page08_pre_page09_local_execution_guide.md
```

## Required checkout

```bash
git fetch --all --tags --prune
git checkout stage186-page08-branchpoint-map
git pull --ff-only origin stage186-page08-branchpoint-map
python -m pip install -e ".[dev]"
```

## Required baseline checks

```bash
python tools/session_start.py
python tools/run_mandatory_predevelopment_check.py
python tools/check_stage_metadata_consistency.py
python tools/check_release_asset_integrity.py
python tools/run_stage184_release_gate.py
python tools/run_release_gate.py
python tools/run_stage72_repo_doctor.py
```

If any baseline check fails, stop and fix the baseline before adding local results.

## GitNexus execution

Try GitNexus first:

```bash
gitnexus.cmd analyze --force
gitnexus.cmd status
```

If the environment uses a non-Windows command:

```bash
gitnexus analyze --force
gitnexus status
```

If GitNexus is not available but an approved fallback analyzer exists, run that fallback and record it as fallback evidence. Do not pretend fallback evidence is GitNexus evidence.

## Files that must be updated after local evidence

```text
release/current/stage186_gitnexus_lineage_connectivity_report.json
manifests/stage186_symbol_to_branchpoint_connectivity.json
manifests/stage186_orphan_legacy_symbol_report.json
manifests/stage186_successor_trace_matrix.json
release/current/stage186_branchpoint_map_report.json
release/current/stage190_page08_release_seal_report.json
release/current/page08_release_gate_report.json
```

## Expected local evidence report shape

`release/current/stage186_gitnexus_lineage_connectivity_report.json` should state one of:

```text
PASS_WITH_GITNEXUS_OUTPUT
PASS_WITH_APPROVED_FALLBACK_OUTPUT
FAIL
```

Do not leave it as `PENDING_REQUIRED_EVIDENCE` before Page09.

Minimum fields:

```json
{
  "stage": 186,
  "title": "GitNexus Lineage Connectivity Evidence",
  "status": "PASS_WITH_GITNEXUS_OUTPUT",
  "required_for_page08_seal": true,
  "source": "local GitNexus run",
  "commands": [],
  "connectivity_summary": {},
  "orphan_legacy_symbols": [],
  "successor_trace_findings": [],
  "generated_at": "YYYY-MM-DD"
}
```

## Expected Page08 final statuses after local evidence

After local evidence is applied and reports are regenerated:

```text
Stage186: PASS or PASS_WITH_WARNINGS
Stage187: PASS or PASS_WITH_WARNINGS
Stage188: PASS or PASS_WITH_WARNINGS
Stage189: PASS or PASS_WITH_WARNINGS
Stage190: PASS
Page08 release gate: PASS
Page09 entry allowed: true
```

## Commit instruction

Commit the updated evidence files with a message like:

```bash
git add release/current/stage186_gitnexus_lineage_connectivity_report.json \
        manifests/stage186_symbol_to_branchpoint_connectivity.json \
        manifests/stage186_orphan_legacy_symbol_report.json \
        manifests/stage186_successor_trace_matrix.json \
        release/current/stage186_branchpoint_map_report.json \
        release/current/stage190_page08_release_seal_report.json \
        release/current/page08_release_gate_report.json

git commit -m "Apply Page08 local lineage connectivity evidence"
git push origin stage186-page08-branchpoint-map
```

## Local Codex prompt

```text
Continue V1700 Page08 from branch stage186-page08-branchpoint-map. Read docs/development/page08_pre_page09_local_execution_guide.md and all Page08 proposal/blueprint documents. Run local GitNexus if available. Update Stage186 connectivity, orphan legacy symbol, successor trace, Stage186 report, Stage190 report, and Page08 release gate report. Do not start Page09. Do not implement Story Patch, EAT8D extraction, Narrative PR, Narrative IDE, MultiWork, plugin, or learning. The only goal is to convert Page08 from BLOCKED_PENDING_LOCAL_GITNEXUS_OR_APPROVED_FALLBACK to PASS or PASS_WITH_WARNINGS if evidence supports it.
```

## Stop conditions

Stop and ask for review if:

```text
GitNexus output contradicts the branchpoint manifest.
Orphan legacy symbols are found without successor trace.
Stage185 appears hub-closed but no hub closure evidence exists.
Page09 files already exist on the branch.
A fallback analyzer is used without explicit approval.
```
