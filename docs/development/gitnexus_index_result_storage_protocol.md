# GitNexus Index Result Storage Protocol

Status: local Codex execution report
Created: 2026-05-29
Applies to: every future N-version / stage / page validation pass
Current example: Page10 Stage200

## 1. Purpose

This report defines where a local Codex session must store GitNexus index results in the hub repository and which result values the web project needs before continuing the next stage.

The rule is:

```text
Local Codex runs GitNexus.
Local Codex writes evidence files into repository paths.
Local Codex pushes the evidence.
Web project reads the pushed evidence before continuing development.
```

Terminal output alone is not evidence. Evidence must be committed to the repository.

## 2. Version variable

Use `N` for the target version, stage, or page seal point.

Examples:

```text
N = stage186
N = stage194
N = stage200
N = page10
N = page11
```

For a stage-level validation, use the stage id as the primary key.

For a page-level validation, use the page id as the primary key and include the stage range.

## 3. Required hub storage paths

For each N-version GitNexus run, local Codex must create or update these files:

```text
release/gitnexus/{N}/gitnexus_index_report.json
release/gitnexus/{N}/gitnexus_status.txt
release/gitnexus/{N}/gitnexus_analyze_log.txt
release/gitnexus/{N}/gitnexus_summary.md
manifests/gitnexus/{N}_symbol_connectivity.json
manifests/gitnexus/{N}_orphan_symbol_report.json
manifests/gitnexus/{N}_successor_trace_matrix.json
release/current/{N}_gitnexus_evidence_report.json
```

For Page10 Stage200, the concrete paths are:

```text
release/gitnexus/stage200/gitnexus_index_report.json
release/gitnexus/stage200/gitnexus_status.txt
release/gitnexus/stage200/gitnexus_analyze_log.txt
release/gitnexus/stage200/gitnexus_summary.md
manifests/gitnexus/stage200_symbol_connectivity.json
manifests/gitnexus/stage200_orphan_symbol_report.json
manifests/gitnexus/stage200_successor_trace_matrix.json
release/current/stage200_gitnexus_evidence_report.json
```

If the validation is for the whole Page10 state, also update:

```text
release/current/page10_release_gate_report.md
release/current/stage200_summary.md
```

## 4. Required GitNexus commands

Run from repository root:

```bash
git fetch --all --tags --prune
git status --short
python tools/session_start.py
python tools/run_mandatory_predevelopment_check.py
python tools/check_stage_metadata_consistency.py
python tools/check_release_asset_integrity.py
python tools/run_release_gate.py
python tools/run_stage72_repo_doctor.py
gitnexus.cmd analyze --force
gitnexus.cmd status
```

Alternative command names if needed:

```bash
gitnexus analyze --force
gitnexus status
```

Do not mark GitNexus as passed if the command did not run.

## 5. Required result values

The web project needs the following values in `release/gitnexus/{N}/gitnexus_index_report.json`:

```json
{
  "version_id": "stage200",
  "scope": "Page10 Stage195~200 full repository state",
  "branch": "roadmap-page08-page17-commercial-absorption",
  "indexed_commit": "<short-or-full-sha>",
  "current_commit_at_index_time": "<short-or-full-sha>",
  "gitnexus_status": "up-to-date | changed | failed | unavailable",
  "gitnexus_available": true,
  "commands_run": [
    "gitnexus.cmd analyze --force",
    "gitnexus.cmd status"
  ],
  "graph_summary": {
    "nodes": 0,
    "edges": 0,
    "clusters": 0,
    "flows": 0
  },
  "preflight": {
    "session_start": "PASS | FAIL | SKIPPED",
    "mandatory_predevelopment_check": "PASS | FAIL | SKIPPED",
    "stage_metadata_consistency": "PASS | FAIL | SKIPPED",
    "release_asset_integrity": "PASS | FAIL | SKIPPED",
    "release_gate": "PASS | FAIL | SKIPPED",
    "repo_doctor": "PASS | FAIL | SKIPPED"
  },
  "overall_result": "PASS | PASS_WITH_WARNINGS | FAIL",
  "warnings": [],
  "failures": []
}
```

Do not omit `indexed_commit`, `current_commit_at_index_time`, `gitnexus_status`, or `graph_summary`.

## 6. Symbol connectivity file

`manifests/gitnexus/{N}_symbol_connectivity.json` must contain:

```json
{
  "version_id": "stage200",
  "scope": "Page10 Stage195~200",
  "records": [
    {
      "owner": "Stage195",
      "artifact": "manifests/stage195_project_story_bible_contract.json",
      "status": "CONNECTED | MISSING | WEAK",
      "connected_to": ["Page10", "Stage200", "Page09 mapping"],
      "notes": []
    }
  ]
}
```

For Page10 Stage200, at minimum include records for:

```text
Stage195 contract
Stage196 contract
Stage197 contract
Stage198 contract
Stage199 contract
Stage200 summary
Page10 release gate
Page10 proposal
Page10 design outline
Page09 release gate
Page08 GitNexus evidence
```

## 7. Orphan report file

`manifests/gitnexus/{N}_orphan_symbol_report.json` must contain:

```json
{
  "version_id": "stage200",
  "orphan_count": 0,
  "orphan_symbols": [],
  "unresolved_items": [],
  "decision": "PASS | PASS_WITH_WARNINGS | FAIL"
}
```

If orphan items exist, list them. Do not delete or hide them.

Each orphan item must include:

```text
symbol_or_file
reason
expected_owner
recommended_fix
blocking_level
```

## 8. Successor trace file

`manifests/gitnexus/{N}_successor_trace_matrix.json` must contain:

```json
{
  "version_id": "stage200",
  "successor_traces": [
    {
      "from": "Stage195",
      "to": "Stage196",
      "status": "CONNECTED | MISSING | WEAK",
      "evidence": []
    }
  ]
}
```

For Page10 Stage200, required traces are:

```text
Page08 -> Page09
Page09 -> Page10
Stage195 -> Stage196
Stage196 -> Stage197
Stage197 -> Stage198
Stage198 -> Stage199
Stage199 -> Stage200
Stage200 -> Page11 design
Stage200 -> Page12 future extraction input
```

## 9. Current evidence report

`release/current/{N}_gitnexus_evidence_report.json` is the compact file the web project reads first.

Required shape:

```json
{
  "version_id": "stage200",
  "status": "PASS_WITH_GITNEXUS_OUTPUT",
  "source_folder": "release/gitnexus/stage200",
  "indexed_commit": "<sha>",
  "current_commit_at_index_time": "<sha>",
  "graph_summary": {
    "nodes": 0,
    "edges": 0,
    "clusters": 0,
    "flows": 0
  },
  "orphan_count": 0,
  "required_traces_present": true,
  "page_gate_to_update": "release/current/page10_release_gate_report.md",
  "decision": "Page10 may advance | Page10 remains blocked | Page10 may advance with warnings"
}
```

## 10. Page10 Stage200 specific requirement

For current Page10 Stage200, local Codex must validate that these files are connected:

```text
docs/proposals/page10_story_repository_codex_context_proposal.md
docs/architecture/page10_design_outline.md
docs/contracts/stage195_contract.md
docs/contracts/stage196_note.md
docs/contracts/stage197_note.md
docs/contracts/stage198_note.md
docs/contracts/stage199_note.md
manifests/stage195_project_story_bible_contract.json
manifests/stage196_entity_registry_contract.json
manifests/stage197_relation_graph_contract.json
manifests/stage198_context_packet_contract.json
manifests/stage199_preview_contract.json
release/current/page10_release_gate_report.md
release/current/stage200_summary.md
release/current/stage200_integrity_repair_report.md
```

## 11. Commit and push instruction

After writing the evidence files:

```bash
git add release/gitnexus/{N}/ \
        manifests/gitnexus/{N}_symbol_connectivity.json \
        manifests/gitnexus/{N}_orphan_symbol_report.json \
        manifests/gitnexus/{N}_successor_trace_matrix.json \
        release/current/{N}_gitnexus_evidence_report.json

git add release/current/page10_release_gate_report.md release/current/stage200_summary.md

git commit -m "Apply GitNexus evidence for {N}"
git push origin roadmap-page08-page17-commercial-absorption
```

For Stage200:

```bash
git commit -m "Apply GitNexus evidence for Stage200"
```

## 12. Local Codex instruction

Use this instruction for local Codex:

```text
Run GitNexus for the current repository state of roadmap-page08-page17-commercial-absorption. Target version is Stage200 unless instructed otherwise. Store the full result under release/gitnexus/stage200 and write compact evidence into release/current/stage200_gitnexus_evidence_report.json. Also write symbol connectivity, orphan symbol report, and successor trace matrix under manifests/gitnexus. Update page10_release_gate_report.md and stage200_summary.md only if the evidence changes the decision. Push the result to the hub. Do not expose secrets. Do not start Page11 implementation in this task.
```

## 13. Web project review after push

After local Codex pushes results, the web project must check:

```text
1. Is indexed_commit equal to the pushed commit or an expected earlier commit?
2. Is GitNexus status up-to-date?
3. Are graph counts present?
4. Are orphan symbols zero or explained?
5. Are Stage195~200 traces connected?
6. Does Page10 gate need promotion from fallback-pending to GitNexus-backed status?
7. Can Page11 implementation proceed beyond design?
```

## 14. Final rule

A GitNexus run is useful only when its result is committed as repository evidence.

For every N-version:

```text
release/gitnexus/{N}/ = full evidence folder
manifests/gitnexus/{N}_*.json = structured analysis records
release/current/{N}_gitnexus_evidence_report.json = web review entry point
```
