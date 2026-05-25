# Stage164 Proposal — Surface Draft Dry-Run Renderer

## Problem

Stage163 produces a deterministic render plan, but Page04 still needs a safe way to inspect what surface draft units would be produced before any real rendering or provider generation is opened.

## Proposal

Add a local deterministic dry-run renderer that converts render plan nodes into surface-safe draft units and a replay trace. The output is review evidence, not final prose.

## Non-goals

- No live provider generation
- No runtime rendering
- No write path
- No canon mutation
- No memory write
- No runtime training
- No hidden render payload exposure to Node2
