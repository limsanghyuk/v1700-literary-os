# V1700 Stage151 Proposal — Local Read-Only Memory Store

## Purpose

Stage151 is the second Page02 Narrative Memory Body stage. It materializes the Stage150 memory contract as a deterministic local read-only store fixture.

Stage151 is not a retrieval engine, vector database, live RAG system, or write-enabled memory layer. It only proves that memory records can be loaded locally, validated against the Stage150 contract, indexed by checksum, and projected safely for Node2.

## Baseline

- Baseline stage: Stage150 Memory Contract
- Page: Page02 Narrative Memory Body
- Required upstream evidence: Stage150 memory contracts and release gate

## Goals

1. Add a local JSONL memory fixture store.
2. Validate Stage150 required fields.
3. Verify deterministic checksums.
4. Build a checksum index.
5. Enforce read-only access policy.
6. Prove Node2 receives only surface-safe projections.
7. Prepare Stage152 deterministic local query and ranking without enabling it.

## Non-goals

- No memory write execution
- No vector database runtime dependency
- No live provider RAG
- No SQL or graph write execution
- No canon mutation
- No runtime training
- No auto-repair apply

## Required outputs

- `release/current/stage151_local_read_only_memory_store_report.json`
- `release/current/stage151_release_gate_report.json`
- `release/current/stage151_local_read_only_memory_store_pack/store_spec.json`
- `release/current/stage151_local_read_only_memory_store_pack/record_validation_report.json`
- `release/current/stage151_local_read_only_memory_store_pack/checksum_index.json`
- `release/current/stage151_local_read_only_memory_store_pack/read_only_access_policy.json`
- `release/current/stage151_local_read_only_memory_store_pack/node2_projection_index.json`
