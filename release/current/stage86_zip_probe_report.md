# Stage86 ZIP Probe Report

## Package

- ZIP: `V1700_stage86_v380_arc_reveal_knowledge_absorption_integrated_repository.zip`
- SHA256: recorded externally in `V1700_stage86_v380_arc_reveal_knowledge_absorption_integrated_repository.zip.sha256.txt`
- Local-only exclusions verified: `.git`, `.gitnexus`, `.venv`, `venv`, `__pycache__`, `.pytest_cache`, `*.pyc`
- Excluded entry count: `0`

## Extracted Repository Probe

The ZIP was extracted to a clean probe folder and tested from:

```text
C:\AI_Codex\codex-work\gpt\packages\v1700_stage86\_zip_probe\gpt\active\v1700\literary_generator
```

## Results

- `compileall src tools`: `pass`
- `python tools/run_stage86_release_gate.py`: `pass`
- `pytest -q tests/test_stage86_arc_reveal_knowledge.py`: `7 passed`
- `pytest -q tests`: `79 passed`

## GitNexus Evidence

GitNexus was run on the Stage86 work repository before packaging:

```text
GitNexus 1.6.4
465 files
3989 nodes
6402 edges
52 clusters
181 flows
```

The native `.gitnexus` directory is intentionally excluded from the package. Its evidence snapshot is preserved in:

```text
release/current/stage86_gitnexus_meta_snapshot.json
release/current/stage86_gitnexus_index_quality_report.json
```
