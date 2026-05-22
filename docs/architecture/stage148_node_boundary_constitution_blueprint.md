# Stage148 Blueprint - Node Boundary Constitution

## Target Architecture

```text
Stage146 Narrative State Contract
  -> reveal boundary matrix
Stage147 Project Manifest Body
  -> canonical manifest bundle
  -> manifest load order
Stage148 Node Boundary Constitution
  -> node authority matrix
  -> packet route map
  -> surface projection registry
  -> boundary enforcement summary
  -> Stage149 entry signals
Stage149 Body Constitution Release Gate
Stage150 Memory Body
```

## Repository Layout

```text
src/v1700/node_boundary_constitution/
  contracts.py
  report.py

src/v1700/stage148/
  stage148_runner.py

src/v1700/gates/
  stage148_release_gate.py

docs/proposals/
  stage148_node_boundary_constitution_proposal.md

docs/architecture/
  stage148_node_boundary_constitution_blueprint.md

docs/development/
  stage148_developer_handoff.md

manifests/
  stage148_manifest.json
  stage148_node_boundary_constitution_manifest.json
  stage148_branchpoint_trace_manifest.json
  live_core_stage148_overlay.json

release/current/
  stage148_node_boundary_constitution_report.json
  stage148_release_gate_report.json
  stage148_release_asset_manifest.json
  stage148_node_boundary_constitution_pack/
```

## Evidence Pack

- `node_authority_matrix.json`
- `packet_route_map.json`
- `surface_projection_registry.json`
- `boundary_enforcement_summary.json`
- `stage149_entry_signals.json`

## Design Notes

- Stage148 does not replace Stage147 packets. It binds node authority on top of them.
- Node1 keeps full planning authority over canonical packets.
- Node2 consumes only reader-surface packets and reveal projections.
- Node3 receives critic summaries and rendered-surface validation inputs, not mutation authority.
