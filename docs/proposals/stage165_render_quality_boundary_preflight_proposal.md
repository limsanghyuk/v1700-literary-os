# Stage165 Proposal — Render Quality and Boundary Preflight

## Problem

Stage164 creates surface-safe dry-run draft units, but Page04 needs a deterministic quality and boundary preflight before sealing the rendering body.

## Proposal

Add Stage165 as a local-only quality and boundary preflight. It consumes Stage164 evidence and emits quality metrics, boundary checks, Node2 projection safety, blocked render operation registry, and Stage166 entry criteria.

## Non-goals

- No live provider generation
- No runtime rendering
- No render writes
- No memory writes
- No canon mutation
- No runtime training
- No final publication workflow
