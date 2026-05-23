
# V1700 Stage152 Proposal — Memory Query Interface

## Purpose

Stage152 turns the Stage151 local read-only memory store into a deterministic local query and ranking surface.

It does not add live RAG, vector database runtime dependencies, write execution, canon mutation, training, or auto-repair. The stage only proves that V1700 can find, rank, and safely project local memory records using deterministic scoring.

## Required API

```text
find_project_memory
find_characters
find_episodes
find_scenes
find_events
find_reveals
find_payoffs
query_by_intent
rank_memory_candidates
project_for_node2
```

## Scoring

```text
lexical term overlap
field priority
temporal metadata
simple rank fusion
boundary-safe penalty
```

## Decision

Proceed with Stage152 as deterministic local query/ranking only. Stage153 may start only after Stage152 proves memory query health and Node2-safe projection.
