
# V1700 Stage152 Blueprint — Memory Query Interface

## Architecture

```text
Stage151 Local Read-Only Memory Store
  ↓
Stage152 Deterministic Local Query / Ranking
  ├── Query API Catalog
  ├── Query Policy
  ├── Intent Query Result
  ├── Type Query Results
  ├── Deterministic Ranking Report
  └── Node2 Projection Report
```

## Package layout

```text
src/v1700/memory_query_interface/
  __init__.py
  contracts.py
  query.py
  report.py

src/v1700/stage152/
  __init__.py
  stage152_runner.py

src/v1700/gates/
  stage152_release_gate.py
```

## Boundary

Node2 projection must not include hidden reveal payloads, private notes, write handles, canon mutation commands, learning payloads, or raw manuscript payloads.
