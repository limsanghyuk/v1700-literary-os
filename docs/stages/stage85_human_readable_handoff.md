# Stage85 Human-Readable Handoff

Stage85 answers one practical question:

```text
If a developer changes a module, which literary concept, test, and release gate may be affected?
```

## What Changed

Stage85 adds a traceability layer on top of Stage84.

Stage84 proved that Claude V370 prose-runtime strengths could be absorbed into V1700 while preserving:

- provider default calls: `0`
- Node2 raw reveal access: `0`
- Korean drama hierarchy
- GraphNexus authority
- GitNexus optional sidecar

Stage85 now proves where those ideas live in the repository.

## User Runtime

A normal user does not need GitNexus to run the program.

```text
GitNexus is optional.
Python fallback remains required.
V1700 runs local-first by default.
```

## Developer Runtime

A developer who installs GitNexus gets higher-resolution impact analysis.

Recommended developer checks:

```bash
gitnexus analyze --force
python tools/run_symbol_to_branchpoint_trace_gate.py
python tools/run_stage85_gitnexus_index_quality_gate.py
python tools/run_stage85_release_gate.py
python tools/run_release_gate.py
```

## What To Read First

1. `README.md`
2. `docs/stages/stage85.md`
3. `docs/stages/stage85_symbol_to_branchpoint_matrix.md`
4. `manifests/symbol_to_branchpoint_trace_manifest.json`
5. `release/current/stage85_gitnexus_index_quality_report.json`

