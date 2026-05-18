# Stage72.3 Phase 0 Baseline Lock Report

## Summary

Stage72.3 Phase 0 is complete.

The current Stage72.2 baseline remains valid after the Stage72.3 council/design documents were added.

## Scope

Phase 0 locks the current baseline before Stage01-39 lineage recovery begins.

This prevents the next phase from mixing two different questions:

```text
1. Is the current V1700 baseline healthy?
2. Which pre-Stage40 concepts should be recovered and mapped?
```

Only after question 1 is green should Phase 1 begin.

## Actions Performed

### Stage72.2 Gate

Command:

```powershell
python tools/run_stage72_2_release_gate.py
```

Result:

```text
status: pass
provider_default_calls: 0
node2_raw_reveal_access_count: 0
```

### GitNexus Index Refresh

Initial observation:

```text
Stage72.3 documents made the existing GitNexus index stale.
```

The index mirror was refreshed from:

```text
C:\AI_Codex\codex-work\gpt\active\v1700\literary_generator
```

to:

```text
C:\AI_Codex\codex-work\gpt\gitnexus_index\v1700_stage72_2_ascii
```

Then GitNexus was re-run:

```powershell
gitnexus analyze "C:\AI_Codex\codex-work\gpt\gitnexus_index\v1700_stage72_2_ascii" --force --skip-git
```

Result:

```text
files: 166
nodes: 1301
edges: 1963
clusters: 15
flows: 45
stale: false
```

### Main Release Gate

Command:

```powershell
python tools/run_release_gate.py
```

Result:

```text
status: pass
runtime_smoke: pass
graph_nexus_release_gate: pass
stage72_2_release_gate: pass
provider_default_calls: 0
node2_raw_reveal_access_count: 0
```

### Test Suite

Command:

```powershell
python -m pytest -q tests
```

Result:

```text
20 passed
```

## Current GitNexus Alias

```text
alias: v1700_stage72_2_ascii
path: C:\AI_Codex\codex-work\gpt\gitnexus_index\v1700_stage72_2_ascii
```

## Decision

Phase 0 is approved.

The project may proceed to Phase 1:

```text
Historical Evidence Scan
```

Phase 1 should create:

```text
manifests/pre_stage40_raw_evidence_index.json
```

and should begin from the historical knowledge base:

```text
C:\AI_Codex\codex-work\gpt\knowledge_base\v1650_stage35_critic_comparison_gate
```
