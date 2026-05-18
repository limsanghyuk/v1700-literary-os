# V1700 Literary OS - Stage130

> MultiWork Release
> Provider-Zero AI longform novel and drama scenario generation system.

## Current Stage

Stage130 seals Stage127~129 into the first clean MultiWork release authority.

The central rule is simple:

- Stage127 preflight and isolation audit remains required.
- Stage128 SharedWorld / SharedCharacter adapters remain read-only.
- Stage129 MultiWorkCIM and Cross-Work Canon Governor remain authoritative.
- Stage130 authorizes only the safe MultiWork operational surface.
- Cross-project write, raw manuscript sharing, direct V571 trunk merge, canon auto-resolution, Gate26 hard block, active learning, and AutoRepair mutation remain blocked.

## Quick Start

```bash
pip install -e .

python -m compileall src tools
python tools/run_stage130_multiwork_release.py
python tools/run_stage130_release_gate.py
python tools/run_release_gate.py
python tools/run_stage72_repo_doctor.py
python -m pytest -q tests/test_stage127_multiwork_preflight.py tests/test_stage128_read_only_absorption.py tests/test_stage129_multiwork_cim_governor.py tests/test_stage130_multiwork_release.py
```

## Stage130 Core Modules

```text
src/v1700/multiwork_release/
  contracts.py
  release_matrix.py
  operational_surface.py
  gitnexus_preflight.py
  release_seal.py
  report.py

src/v1700/stage130/
  stage130_runner.py

src/v1700/gates/
  stage130_release_gate.py
```

## Stage130 Release Gate

The Stage130 gate validates:

- Stage129 baseline gate pass
- Stage127~129 evidence preserved
- MultiWork release matrix pass
- operational surface pass
- release seal pass
- direct V571 merge blocked
- cross-project write blocked
- unauthorized cross reads/writes = 0
- raw manuscript leakage = 0
- canon auto-resolution disabled
- SharedWorld source-of-truth promotion disabled
- Gate26 hard block deferred
- provider default calls = 0
- Node2 raw reveal access = 0
- credential leakage = 0
- GitNexus/Python fallback preflight pass
- branchpoint survival pass
- repo doctor and clean packaging pass

## Invariants

```json
{
  "provider_default_calls": 0,
  "live_provider_call_count_in_release_gate": 0,
  "cross_project_write_allowed": false,
  "unauthorized_cross_reads": 0,
  "unauthorized_cross_writes": 0,
  "canon_auto_resolution_count": 0,
  "raw_manuscript_provider_leakage": 0,
  "raw_manuscript_cross_project_leakage": 0,
  "node2_raw_reveal_access": 0,
  "credential_leakage": 0,
  "branchpoint_lineage_preserved": true
}
```

## Stage Lineage

```text
Stage127  MultiWork Preflight & Isolation Audit
Stage128  SharedWorld / SharedCharacter Read-Only Absorption
Stage129  MultiWorkCIM + Cross-Work Canon Governor
Stage130  MultiWork Release
```

## Next Direction

```text
Stage131 - GIG / Gate26 Advisory Absorption
Stage132 - Contradiction Classifier + Mystery Exemption
```

## Repository Evidence

- Stage manifest: `manifests/stage130_manifest.json`
- Live manifest: `manifests/live_core_manifest.json`
- Release report: `release/current/stage130_multiwork_release_report.json`
- Release gate: `release/current/stage130_release_gate_report.json`
