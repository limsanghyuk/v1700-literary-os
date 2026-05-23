
# V1700 Literary OS - Stage152

> Deterministic Local Query / Ranking
> Provider-Zero AI longform novel and drama scenario generation system.

## Current Stage

Stage152 is the official Page02 Narrative Memory Body query stage after Stage151. It exposes deterministic local query and ranking over the read-only memory store.

Stage152 does not enable live provider RAG, vector DB runtime dependencies, memory write, canon mutation, runtime training, or auto-repair apply.

## Quick Start

```bash
pip install -e ".[dev]"

python -m compileall -q src tools
python tools/run_mandatory_predevelopment_check.py
python tools/check_stage_metadata_consistency.py
python tools/check_release_asset_integrity.py
python tools/run_stage151_release_gate.py
python tools/run_stage152_memory_query_interface.py
python tools/run_stage152_release_gate.py
python tools/run_release_gate.py
python tools/run_stage72_repo_doctor.py
python -m pytest tests/test_stage150_memory_contract.py tests/test_stage151_local_read_only_memory_store.py tests/test_stage152_memory_query_interface.py -q
```

## Stage152 Core Modules

```text
src/v1700/memory_query_interface/
  contracts.py
  query.py
  report.py

src/v1700/stage152/
  stage152_runner.py

src/v1700/gates/
  stage152_release_gate.py
```

## Stage Lineage

```text
Stage150  Memory Contract
Stage151  Local Read-Only Memory Store
Stage152  Deterministic Local Query / Ranking
```

## Repository Evidence

- Stage manifest: `manifests/stage152_manifest.json`
- Live manifest: `manifests/live_core_manifest.json`
- Release report: `release/current/stage152_memory_query_interface_report.json`
- Release gate: `release/current/stage152_release_gate_report.json`
- Official asset manifest: `release/current/stage152_release_asset_manifest.json`
