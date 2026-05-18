# Stage85: GitNexus Density Upgrade and Symbol-to-Branchpoint Traceability

Stage85 upgrades V1700 from a coarse repository map into a higher-resolution traceability system.

The baseline comparison was:

| Metric | GPT V1700 Stage84 | Claude V381 reference |
| --- | ---: | ---: |
| Files | 409 | 332 |
| Nodes/symbols | 3,430 | 10,443 |
| Edges | 5,384 | 21,487 |
| Clusters | 38 | 361 |
| Flows/processes | 137 | 140 |

The interpretation is:

```text
V1700 already has comparable execution-flow breadth.
The next improvement is trace density: branchpoint -> code symbol -> test -> release gate -> GitNexus evidence.
```

## Stage85 Rule

GitNexus remains an optional developer sidecar. It is not promoted to a mandatory runtime dependency.

Authority remains:

```text
GraphNexus = internal authority graph
GitNexus = optional code-impact sidecar
Python fallback = required runtime safety path
```

## New Runtime Evidence

- `src/v1700/traceability/contracts.py`
- `src/v1700/traceability/symbol_trace.py`
- `src/v1700/traceability/index_quality.py`
- `src/v1700/gates/symbol_to_branchpoint_trace_gate.py`
- `src/v1700/gates/gitnexus_index_quality_gate.py`
- `src/v1700/gates/stage85_release_gate.py`

## New Manifests

- `manifests/symbol_to_branchpoint_trace_manifest.json`
- `manifests/stage85_manifest.json`

## New Release Evidence

- `release/current/stage85_gitnexus_index_quality_report.json`
- `release/current/stage85_release_gate_report.json`
- `release/current/stage85_developer_handoff_report.md`
- `release/current/stage85_zip_probe_report.md`

## Success Conditions

```text
stage83_1_release_gate = pass
stage84_release_gate = pass
graph_nexus_release_gate = pass
symbol_to_branchpoint_trace_gate = pass
gitnexus_index_quality_gate = pass
stage85_release_gate = pass
provider_default_calls = 0
node2_raw_reveal_access_count = 0
```

