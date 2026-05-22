# Stage147 Proposal - Project Manifest Body

## Why

Stage146 established the canonical state contracts, but the repository still needed a concrete body that shows how a project manifest becomes a stable state-shaped packet set. Stage147 fills that gap with a local-only, synthetic-only manifest authority layer.

## Scope

Stage147 must:

1. Load the synthetic sample project from `samples/korean_drama_family_secret`.
2. Derive canonical manifest-body packets for series, episode, scene, character, world, reveal, and continuity state.
3. Preserve read-only policies, provider-zero, and Node2 reveal boundaries.
4. Publish release evidence proving Stage148 can start from a deterministic manifest packet surface.

## Non-Goals

- no provider calls
- no runtime training
- no LOSDB writes
- no migration execution
- no canon mutation
- no automatic repair apply

## Success Criteria

- Stage147 report and gate pass.
- The manifest catalog covers all sample sources used by the canonical bundle.
- The manifest-to-state binding map covers all seven canonical packets.
- Policy boundary checks prove the sample remains synthetic, public-safe, and raw-manuscript-free.
- Stage148 entry signals are published.
