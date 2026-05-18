# GitNexus Stage72.1 Validation

## Summary

GitNexus was installed as an external developer CLI/MCP sidecar and validated against the V1700 Stage72.1 active repository.

## Installation

```text
Node.js:   v24.15.0
npm/npx:   11.12.1
GitNexus:  1.6.4
CLI:       C:\Users\User\AppData\Roaming\npm\gitnexus.cmd
```

Setup result:

```text
Codex MCP configured
7 Codex skills installed
Cursor, Claude Code, and OpenCode skipped because they are not installed
```

## Current Active Repository

```text
C:\AI_Codex\codex-work\gpt\active\v1700\literary_generator
```

## Current GitNexus Index

```text
C:\AI_Codex\codex-work\gpt\gitnexus_index\v1700_stage72_1_ascii
```

Registered alias:

```text
v1700-stage72-1-gpt
```

GitNexus index result:

```text
123 files
762 symbols
1128 edges
10 clusters
13 flows
```

## GitNexus Queries

Validated commands:

```powershell
gitnexus list
gitnexus query -r v1700-stage72-1-gpt -l 3 Node2ProseCompiler
gitnexus impact -r v1700-stage72-1-gpt --include-tests Node2ProseCompiler
```

Impact result for `Node2ProseCompiler`:

```text
risk: LOW
impactedCount: 4
affected path includes:
- src/v1700/nodes/node2_prose_renderer/__init__.py
- src/v1700/cli.py
- src/v1700/gates/runtime_smoke.py
- src/v1700/gates/release_gate.py
```

## V1700 Verification

Executed from:

```text
C:\AI_Codex\codex-work\gpt\active\v1700\literary_generator
```

Results:

```text
python tools/run_graph_nexus_release_gate.py -> pass, gitnexus.installed=true
python tools/run_release_gate.py             -> pass
python -m pytest -q tests                    -> 15 passed
```

## Release Evidence

Detailed machine-readable reports are kept under:

```text
C:\AI_Codex\codex-work\gpt\releases\v1700\stage72_1
```
