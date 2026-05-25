# Stage163 Blueprint — Deterministic Render Plan Builder

## Architecture

```text
Stage162 render packet JSONL
  -> render packet validation
  -> stable render packet ordering
  -> render plan nodes
  -> deterministic sequence edges
  -> render order
  -> render plan checksum
  -> Node2-safe projection matrix
```

## Deterministic Ordering

Stage163 orders packets by:

1. surface channel priority
2. render type priority
3. render packet id

This produces a stable render plan even when JSONL input order changes.

## Graph Model

The plan is a linear deterministic DAG. Edges represent sequence dependencies, not runtime execution. This is enough for Stage164 to perform dry-run rendering without opening provider or write privileges.

## Safety

- Runtime rendering disabled.
- Provider generation disabled.
- Render plan writes disabled.
- Canon mutation disabled.
- Node2 receives summaries only.
- Hidden render payloads, provider payloads, write handles, raw manuscript payloads, and credentials are blocked.

## Release Evidence

- `release/current/stage163_deterministic_render_plan_builder_report.json`
- `release/current/stage163_release_gate_report.json`
- `release/current/stage163_deterministic_render_plan_builder_pack/*.json`
