# Stage157 Blueprint — Deterministic Plan Graph Builder

## Architecture

```text
Stage156 Local Execution Packet Store
  ↓
Stage157 Deterministic Plan Graph Builder
  ├── plan_graph_nodes.json
  ├── plan_graph_edges.json
  ├── topological_order.json
  ├── dependency_integrity.json
  ├── deterministic_graph_checksum.json
  ├── node2_plan_projection_matrix.json
  ├── plan_graph_policy.json
  └── regression_snapshot.json
```

## Algorithm

1. Validate the Stage156 JSONL packet store.
2. Index packets by `packet_id`.
3. Convert `dependency_ids` into directed edges from dependency to dependent.
4. Reject missing dependencies and self-dependencies.
5. Run deterministic Kahn topological sorting with lexical tie-breaks.
6. Reject unresolved nodes as cycles.
7. Emit stable graph checksum from sorted nodes, edges, and order.

## Boundary

Stage157 emits graph evidence only. It does not execute graph nodes and does not write runtime state.
