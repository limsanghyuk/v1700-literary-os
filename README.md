# V1700 Literary OS - Stage170

> Regression and Negative Fixture Harness

Stage170 adds the Page05 regression and negative fixture harness. It verifies safe and negative fixtures without provider calls, writes, mutation, runtime training, or auto-repair apply.

## Quick Start

```bash
python -m compileall -q src tools
python tools/run_stage168_release_gate.py
python tools/run_stage169_release_gate.py
python tools/run_stage170_regression_negative_fixture_harness.py
python tools/run_stage170_release_gate.py
python tools/check_stage_metadata_consistency.py
python tools/check_release_asset_integrity.py
python tools/run_release_gate.py
python tools/run_stage72_repo_doctor.py
python -m pytest tests/test_stage167_evaluation_contract.py tests/test_stage168_local_evaluation_packet_store.py tests/test_stage169_deterministic_quality_continuity_evaluator.py tests/test_stage170_regression_negative_fixture_harness.py -q
```

## Current Stage

```text
Stage167  Evaluation Contract
Stage168  Local Evaluation Packet Store
Stage169  Deterministic Quality and Continuity Evaluator
Stage170  Regression and Negative Fixture Harness
```

## Next

Stage171 - Evaluation Boundary and Leakage Preflight.
