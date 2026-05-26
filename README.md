# V1700 Literary OS - Stage171

> Evaluation Boundary and Leakage Preflight
> Provider-zero AI longform novel and drama scenario generation system.

## Current Stage

Stage171 verifies Page05 evaluation boundaries after Stage170. It checks inherited gates, boundary invariant freeze, Node2 surface-only projection, controlled negative fixture quarantine, leakage-zero evidence, and Stage172 entry criteria.

Stage171 does not enable provider evaluation, provider generation, runtime execution, writes, memory writes, canon mutation, runtime training, or auto-repair apply.

## Quick Start

```bash
python -m compileall -q src tools
python tools/run_stage170_release_gate.py
python tools/run_stage171_evaluation_boundary_leakage_preflight.py
python tools/run_stage171_release_gate.py
python tools/check_stage_metadata_consistency.py
python tools/check_release_asset_integrity.py
python tools/run_release_gate.py
python tools/run_stage72_repo_doctor.py
python -m pytest tests/test_stage171_evaluation_boundary_leakage_preflight.py -q
```

## Stage Lineage

```text
Stage167  Evaluation Contract
Stage168  Local Evaluation Packet Store
Stage169  Deterministic Quality and Continuity Evaluator
Stage170  Regression and Negative Fixture Harness
Stage171  Evaluation Boundary and Leakage Preflight
```

Next: Stage172 Page05 Release Seal.
