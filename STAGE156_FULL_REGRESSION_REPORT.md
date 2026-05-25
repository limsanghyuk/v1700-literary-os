# Stage156 Full Regression Report

## Target

- Stage: Stage156 — Local Execution Packet Store
- Baseline: Stage155 Execution Contract
- Artifact reviewed: `V1700_stage156_local_execution_packet_store_release_integrated_repository_with_artifacts.zip`
- Repaired artifact: `V1700_stage156_local_execution_packet_store_regression_repaired_release_integrated_repository_with_artifacts.zip`

## Principal Engineer Finding

Stage156 logic, algorithms, release gates, metadata, asset integrity, and Page03 linkage passed regression. The only issue found in the input package was packaging hygiene: the ZIP included Python cache artifacts (`__pycache__` / `.pyc`). This was repaired without changing Stage156 execution logic.

## Repair Applied

- Removed all `__pycache__` directories.
- Removed all `.pyc` files.
- Removed `.pytest_cache` directories if present.
- Regenerated `FILELIST.txt` with `SHA256SUMS.txt` excluded by policy.
- Regenerated `SHA256SUMS.txt` using normalized newline hashing.
- Repacked the repository and re-extracted it for verification.

## Commands Executed

```bash
python -m compileall -q src tools
python tools/run_stage156_local_execution_packet_store.py
python tools/run_stage156_release_gate.py
python tools/run_mandatory_predevelopment_check.py
python tools/check_stage_metadata_consistency.py
python tools/check_release_asset_integrity.py
python tools/run_release_gate.py
python tools/run_stage72_repo_doctor.py
python -m pytest tests/test_stage156_local_execution_packet_store.py -q
python -m pytest tests/test_stage150_memory_contract.py -q
python -m pytest tests/test_stage151_local_read_only_memory_store.py -q
python -m pytest tests/test_stage152_memory_query_interface.py -q
python -m pytest tests/test_stage153_memory_health_leakage_boundary.py -q
python -m pytest tests/test_stage154_page02_release_seal.py -q
python -m pytest tests/test_stage155_execution_contract.py -q
python -m pytest tests/test_stage156_local_execution_packet_store.py -q
```

## Results

- ZIP integrity: pass
- Forbidden cache scan before final verification: 0
- compileall: pass
- Stage156 report: pass
- Stage156 release gate: pass
- mandatory predevelopment: pass
- metadata consistency: pass
- release asset integrity: pass
- main release gate: pass
- repo doctor: pass
- Stage156 pytest: 5 passed
- Stage150 pytest: 2 passed
- Stage151 pytest: 3 passed
- Stage152 pytest: 4 passed
- Stage153 pytest: 4 passed
- Stage154 pytest: 7 passed
- Stage155 pytest: 5 passed
- Stage156 pytest: 5 passed
- Stage150~156 targeted regression total: 30 passed

## Full Repository Pytest Note

A full `pytest -q` run was attempted, but it exceeded the execution time limit in this environment before producing a failure summary. The stage-targeted regression suite and all release gates passed.

## Invariants

- provider_default_calls = 0
- live_provider_call_count_in_release_gate = 0
- runtime_execution_enabled = false
- provider_execution_enabled = false
- execution_write_enabled = false
- store_write_enabled = false
- memory_write_enabled = false
- node2_raw_reveal_access = 0
- boundary_violation_count = 0
- runtime_training_enabled = false
- credential_leakage = 0

## Final Decision

Stage156 is regression-pass after packaging hygiene repair. The repaired integrated repository ZIP is the preferred handoff artifact.
