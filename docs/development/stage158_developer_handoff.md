# Stage158 Developer Handoff

## Commands

```bash
python -m compileall -q src tools
python tools/run_stage157_release_gate.py
python tools/run_stage158_dependency_conflict_preflight.py
python tools/run_stage158_release_gate.py
python tools/check_stage_metadata_consistency.py
python tools/check_release_asset_integrity.py
python tools/run_release_gate.py
python tools/run_stage72_repo_doctor.py
python -m pytest tests/test_stage158_dependency_conflict_preflight.py -q
```

## Rules

Stage158 remains deterministic, local-only, provider-zero, write-zero, Node2-safe, and dry-run-only. Stage159 can begin only if the Stage158 release gate passes.
