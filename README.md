# V1700 Literary OS - Stage133

> NarrativeStateTensor 8D Measurement Layer
> Provider-Zero AI longform novel and drama scenario generation system.

## Current Stage

Stage133 measures Stage132 contradiction classifications through an 8D NarrativeStateTensor.

The central rule is simple:

- Stage127 preflight and isolation audit remains required.
- Stage128 SharedWorld / SharedCharacter adapters remain read-only.
- Stage129 MultiWorkCIM and Cross-Work Canon Governor remain authoritative.
- Stage130 authorizes only the safe MultiWork operational surface.
- Stage131 classifies true contradiction, intentional mystery, character misunderstanding, and reveal delay without enabling a hard block.
- Stage132 requires evidence before granting mystery exemption: a reveal lock and payoff budget must exist.
- Stage133 measures every Stage132 conflict category across eight local-only narrative state dimensions without mutating canon.
- Cross-project write, raw manuscript sharing, direct V571 trunk merge, canon auto-resolution, Gate26 hard block, active learning, and AutoRepair mutation remain blocked.

## Quick Start

```bash
pip install -e ".[dev]"

python -m compileall src tools
python -m pytest tests/ -q
python tools/run_ci_dependency_preflight.py
python tools/run_stage133_narrative_state_tensor.py
python tools/run_stage133_release_gate.py
python tools/run_stage130_multiwork_release.py
python tools/run_stage130_release_gate.py
python tools/run_release_gate.py
python tools/run_stage72_repo_doctor.py
```

## GitHub CI/CD

The repository uses GitHub Actions as the shared authority for work across multiple computers.

- `ci-core`: runs on push, pull request, and version tags. It installs `.[dev]`, runs `pytest tests/ -q`, Stage133 release gate, the main release gate, repo doctor, and GitNexus/GraphNexus preflight checks.
- `ci-full`: scheduled/manual full-lineage verification.
- `release`: runs on `v1700-stage*` or `v*` tags and publishes an integrated ZIP, SHA256 sidecar, and `SHA256SUMS.txt` snapshot as GitHub Release assets.

## Stage133 Core Modules

```text
src/v1700/narrative_state_tensor/
  contracts.py
  measurement.py
  preflight.py
  report.py

src/v1700/stage133/
  stage133_runner.py

src/v1700/gates/
  stage133_release_gate.py
```

## Stage132 Foundation Modules

```text
src/v1700/contradiction_classifier/
  contracts.py
  classifier.py
  mystery_exemption.py
  preflight.py
  report.py

src/v1700/stage132/
  stage132_runner.py

src/v1700/gates/
  stage132_release_gate.py
```

## Stage131 Foundation Modules

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

## Stage133 Release Gate

The Stage133 gate validates:

- Stage130 baseline gate pass
- Stage131 baseline gate pass
- Stage132 baseline gate pass
- 8D NarrativeStateTensor measurement contract
- true contradictions are measured as `REVIEW_REQUIRED`, not auto-repaired
- intentional mysteries pass only when Stage132 reveal-lock/payoff-budget evidence exists
- Gate26 remains advisory-only
- true contradictions require writer review
- intentional mysteries, character misunderstandings, and reveal delays remain valid narrative categories
- mystery exemption requires a reveal lock and payoff budget
- no-conflict cases pass without unnecessary review
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
Stage132  Contradiction Classifier + Mystery Exemption
```

## Next Direction

```text
Stage133 - NarrativeStateTensor 8D Measurement Layer
Stage134 - MetaLearner Audit Mode
```

## Repository Evidence

- Stage manifest: `manifests/stage132_manifest.json`
- Live manifest: `manifests/live_core_manifest.json`
- Release report: `release/current/stage132_contradiction_classifier_report.json`
- Release gate: `release/current/stage132_release_gate_report.json`
