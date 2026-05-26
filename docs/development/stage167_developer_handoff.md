# Stage167 Developer Handoff

Stage167 starts Page05 Evaluation Body with Evaluation Contract only.

## Commands

```bash
python -m compileall -q src tools
python tools/run_stage166_release_gate.py
python tools/run_stage167_evaluation_contract.py
python tools/run_stage167_release_gate.py
python tools/check_stage_metadata_consistency.py
python tools/check_release_asset_integrity.py
python tools/run_release_gate.py
python tools/run_stage72_repo_doctor.py
python -m pytest tests/test_stage167_evaluation_contract.py -q
```

## Required invariants

```text
provider_default_calls = 0
provider_evaluation_enabled = false
evaluation_write_enabled = false
memory_write_enabled = false
cross_project_write_enabled = false
canon_mutation_enabled = false
runtime_training_enabled = false
node2_raw_reveal_access = 0
boundary_criteria_non_overridable = true
```

