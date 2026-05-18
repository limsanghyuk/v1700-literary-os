# V1700 Literary OS - Stage129

> MultiWorkCIM + Cross-Work Canon Governor
> Provider-Zero AI longform novel and drama scenario generation system.

## Quick Start

```bash
pip install -e .

python -m compileall src tools
python tools/run_stage129_multiwork_cim_governor.py
python tools/run_stage129_release_gate.py
python tools/run_release_gate.py
python tools/run_stage72_repo_doctor.py
python -m pytest -q tests/test_stage129_multiwork_cim_governor.py
```

## Current Stage

Stage129 promotes the Stage128 read-only SharedWorld / SharedCharacter absorption into a MultiWork-aware governance layer.

The central rule is simple:

- each work keeps its own local Character Influence Matrix
- cross-work influence is read-only
- canon conflicts are reported and blocked, not auto-resolved
- cross-work canon merge is deferred to Stage130
- provider calls remain zero in release gates

## Stage129 Core Modules

```text
src/v1700/multiwork_cim/
  contracts.py
  project_local_cim.py
  cross_project_influence.py
  canon_governor.py

src/v1700/stage129/
  orchestrator.py
  report.py

src/v1700/gates/
  stage129_release_gate.py
```

## Stage129 Release Gate

The Stage129 gate validates:

- Stage128 baseline gate pass
- project-local CIM builder pass
- cross-project influence read-only pass
- Cross-Work Canon Governor pass
- cross-project write blocked
- unauthorized cross reads/writes = 0
- license boundary preserved
- canon conflict block fixture pass
- canon auto-resolution disabled
- cross-work canon merge disabled
- raw manuscript leakage = 0
- provider default calls = 0
- Node2 raw reveal access = 0
- credential leakage = 0
- GitNexus/Python fallback preflight pass
- branchpoint survival pass
- Stage130 MultiWork Release deferred
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
  "cross_work_canon_merge_allowed": false,
  "raw_manuscript_provider_leakage": 0,
  "raw_manuscript_cross_project_leakage": 0,
  "node2_raw_reveal_access": 0,
  "credential_leakage": 0,
  "branchpoint_lineage_preserved": true
}
```

## Stage Lineage

```text
Stage120  Gate25 NIE v1 Release
Stage121  Cross-Lineage Formula Reconciliation
Stage122  NIE v2 Stability Absorption
Stage123  ASD / Gate28 Absorption
Stage124  PNE / Gate29 Absorption
Stage125  Gate25/28/29 Governor
Stage126  Cross-Lineage Intelligence Release
Stage127  MultiWork Preflight & Isolation Audit
Stage128  SharedWorld / SharedCharacter Read-Only Absorption
Stage129  MultiWorkCIM + Cross-Work Canon Governor
```

## Next Direction

```text
Stage130 - MultiWork Release
Stage131 - GIG / Gate26 Advisory Absorption
```

## Repository Evidence

- Stage manifest: `manifests/stage129_manifest.json`
- Live manifest: `manifests/live_core_manifest.json`
- Release report: `release/current/stage129_multiwork_cim_governor_report.json`
- Release gate: `release/current/stage129_release_gate_report.json`
- Filelist: `V1700_stage129_multiwork_cim_cross_work_canon_governor_filelist.txt`
