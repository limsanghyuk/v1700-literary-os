# Stage163 Proposal — Deterministic Render Plan Builder

## Purpose

Stage163 converts Stage162 local render packets into a deterministic render plan. It is a compiler layer only: it establishes render order, plan nodes, plan edges, checksums, and Node2-safe projection evidence without executing rendering or calling a provider.

## Baseline

- Stage161: Rendering Contract
- Stage162: Local Render Packet Store
- Stage163: Deterministic Render Plan Builder

## Scope

- Read Stage162 JSONL render packets.
- Build deterministic render plan nodes.
- Build deterministic render sequence edges.
- Generate stable render order.
- Generate render plan integrity and checksum reports.
- Generate Node2-safe render plan projection matrix.
- Keep provider generation, runtime rendering, writes, canon mutation, and training disabled.

## Non-goals

- No surface draft text rendering.
- No provider generation.
- No render write path.
- No canon mutation.
- No memory write.
- No hidden reveal projection.

## Next Stage

Stage164 Surface Draft Dry-Run Renderer may consume the Stage163 render plan, but it must remain dry-run and provider-zero by default.
