# V1700 Literary OS - Stage131

> GIG / Gate26 Advisory Absorption
> Provider-Zero AI longform novel and drama scenario generation system.

## Current Stage

Stage131 absorbs the deferred GIG / Gate26 problem as an advisory-only governance layer over the Stage130 MultiWork release.

The central rule is simple:

- Stage127 preflight and isolation audit remains required.
- Stage128 SharedWorld / SharedCharacter adapters remain read-only.
- Stage129 MultiWorkCIM and Cross-Work Canon Governor remain authoritative.
- Stage130 authorizes only the safe MultiWork operational surface.
- Stage131 classifies true contradiction, intentional mystery, character misunderstanding, and reveal delay without enabling a hard block.
- Cross-project write, raw manuscript sharing, direct V571 trunk merge, canon auto-resolution, Gate26 hard block, active learning, and AutoRepair mutation remain blocked.

## Quick Start

```bash
pip install -e ".[dev]"

python -m compileall src tools
python -m pytest tests/ -q
python tools/run_ci_dependency_preflight.py
python tools/run_stage131_gig_advisory.py
python tools/run_stage131_release_gate.py
python tools/run_stage130_multiwork_release.py
python tools/run_stage130_release_gate.py
python tools/run_release_gate.py
python tools/run_stage72_repo_doctor.py
```

## GitHub CI/CD

The repository uses GitHub Actions as the shared authority for work across multiple computers.

- `ci-core`: runs on push, pull request, and version tags. It installs `.[dev]`, runs `pytest tests/ -q`, Stage131 release gate, the main release gate, repo doctor, and GitNexus/GraphNexus preflight checks.
- `ci-full`: scheduled/manual full-lineage verification.
- `release`: runs on `v1700-stage*` or `v*` tags and publishes an integrated ZIP, SHA256 sidecar, and `SHA256SUMS.txt` snapshot as GitHub Release assets.

## Stage131 Core Modules

```text
src/v1700/gig_advisory/
  contracts.py
  classifier.py
  policy.py
  preflight.py
  report.py

src/v1700/stage131/
  stage131_runner.py

src/v1700/gates/
  stage131_release_gate.py
```

## Stage130 Foundation Modules

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

## Stage131 Release Gate

The Stage131 gate validates:

- Stage129 baseline gate pass
- Stage127~129 evidence preserved
- MultiWork release matrix pass
- operational surface pass
- release seal pass
- Stage130 baseline gate pass
- Gate26 remains advisory-only
- true contradictions require writer review
- intentional mysteries, character misunderstandings, and reveal delays remain valid narrative categories
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
Stage131  GIG / Gate26 Advisory Absorption
```

## Next Direction

```text
Stage132 - Contradiction Classifier + Mystery Exemption
Stage133 - NarrativeStateTensor 8D Measurement Layer
```

## Repository Evidence

- Stage manifest: `manifests/stage131_manifest.json`
- Live manifest: `manifests/live_core_manifest.json`
- Release report: `release/current/stage131_gig_advisory_report.json`
- Release gate: `release/current/stage131_release_gate_report.json`
