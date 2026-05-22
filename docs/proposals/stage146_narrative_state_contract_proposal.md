# Stage146 Proposal - Narrative State Contract

## Why

Stage145 declared the constitutional layer, but later body stages still need explicit state objects. Without a fixed contract for series, episode, scene, character, world, reveal, and continuity, future memory and generation logic would drift.

## Proposal

Stage146 should publish a local-only, provider-zero narrative state contract pack that:

1. Defines seven canonical state objects.
2. Declares hierarchy edges between them.
3. Declares continuity rules without enabling repair execution.
4. Declares reveal access boundaries that preserve Node2 surface-only behavior.
5. Signals readiness for Stage147, Stage148, Stage149, and Stage150 without enabling writes.

## Non-Goals

- no provider calls
- no runtime training
- no memory writes
- no migration execution
- no automatic canon mutation
- no automatic repair apply

## Exit Condition

Stage146 is complete when the narrative state report, release gate, manifests, documents, workflows, repo doctor, and regression tests all recognize the new state-contract baseline.
