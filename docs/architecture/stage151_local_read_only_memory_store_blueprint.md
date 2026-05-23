# V1700 Stage151 Blueprint — Local Read-Only Memory Store

## Architecture

```text
Stage150 Memory Contract
  ↓
Stage151 Local Read-Only Memory Store
  ├── JSONL fixture store
  ├── contract field validation
  ├── deterministic checksum index
  ├── read-only access policy
  └── Node2 projection index
```

## Package layout

```text
src/v1700/local_memory_store/
  __init__.py
  contracts.py
  loader.py
  report.py

src/v1700/stage151/
  __init__.py
  stage151_runner.py

src/v1700/gates/
  stage151_release_gate.py

tools/
  run_stage151_local_read_only_memory_store.py
  run_stage151_release_gate.py

samples/stage151_memory_store/
  project_memory_records.jsonl
```

## Data model

Stage151 records reuse the Stage150 base fields:

```text
record_id, project_id, record_type, source_stage, source_state_id,
visibility, boundary_level, created_from, checksum, write_policy
```

## Read-only policy

The store may read deterministic local JSONL records and generate release evidence. It may not write, mutate, train, retrieve from a provider, call live RAG, or expose Node2 raw reveal payloads.

## Stage152 boundary

Stage151 does not rank or search. Stage152 may add deterministic local query and ranking only after Stage151 passes.
