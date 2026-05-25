# V1700 Stage158 Proposal — Dependency and Conflict Preflight

Stage158 adds a deterministic preflight layer over the Stage157 plan graph. It verifies that packet dependencies, execution order, conflict rules, boundary restrictions, and Node2 projections are safe before Stage159 dry-run tracing begins.

## Baseline

- Stage157 Deterministic Plan Graph Builder
- Page03 Execution Body

## Goals

- Validate dependency order against the deterministic plan graph.
- Block forbidden packet types such as provider execution, memory write, canon mutation, runtime training, and auto-repair apply.
- Confirm hidden reveal guard packets have safe dependencies.
- Preserve provider-zero, write-zero, Node2 surface-only, and local-only execution planning.
- Embed the GitNexus/Preflight Step15 connectivity principle into Stage158 evidence.

## Non-goals

- No runtime execution
- No final prose generation
- No provider call
- No memory write
- No graph write
- No canon mutation
- No runtime training
