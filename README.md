# V1700 Literary OS - Stage135

> LearningQualityGate & Candidate Registry
> Provider-Zero AI longform novel and drama scenario generation system.

## Current Stage

Stage135 is the official active development baseline after Stage134. It converts Stage134 MetaLearner audit output into a deterministic candidate registry while keeping runtime training, active learning, model weight updates, canon mutation, provider calls, and AutoRepair mutation blocked.

The central rule is simple:

- Stage134 remains audit-only.
- Stage135 is candidate-only.
- Review-required cases are routed to `REVIEW_ONLY` and never become training examples.
- Future learning candidates may be recorded, but no training trigger is allowed.
- Runtime training remains disabled.
- Active meta-learning remains disabled.
- Model weight update count remains zero.
- Provider calls remain zero.
- Node2 raw reveal access remains zero.
- Canon auto-resolution and AutoRepair mutation remain blocked.

## Quick Start

```bash
pip install -e ".[dev]"

python -m compileall src tools
python -m pytest tests/ -q
python tools/run_ci_dependency_preflight.py
python tools/run_stage134_meta_learner_audit.py
python tools/run_stage134_release_gate.py
python tools/run_stage135_learning_quality_gate.py
python tools/run_stage135_release_gate.py
python tools/run_release_gate.py
python tools/run_stage72_repo_doctor.py
```

## GitHub CI/CD

The repository uses GitHub Actions as the shared authority for work across multiple computers.

- `ci-core`: runs on push, pull request, and version tags. It installs `.[dev]`, runs `pytest tests/ -q`, Stage134 baseline checks, Stage135 LearningQualityGate, Stage135 release gate, the main release gate, repo doctor, and GitNexus/GraphNexus preflight checks.
- `cd-dry-run`: builds a release dry-run archive and SHA256 artifact on PR/push.
- `release`: runs on `v1700-stage*` or `v*` tags and publishes an integrated ZIP, SHA256 sidecar, and `SHA256SUMS.txt` snapshot as GitHub Release assets.

## Stage135 Core Modules

```text
src/v1700/learning_quality_gate/
  contracts.py
  gate.py
  preflight.py
  report.py

src/v1700/stage135/
  stage135_runner.py

src/v1700/gates/
  stage135_release_gate.py
```

## Stage134 Baseline Modules

```text
src/v1700/meta_learner_audit/
  contracts.py
  audit.py
  preflight.py
  report.py

src/v1700/stage134/
  stage134_runner.py

src/v1700/gates/
  stage134_release_gate.py
```

## Stage135 Release Gate

The Stage135 gate validates:

- Stage134 baseline gate pass
- LearningQualityGate report pass
- candidate registry pass
- candidate-only mode enforced
- learning allowed count = 0
- training triggered count = 0
- active meta-learning disabled
- model weight update count = 0
- AutoRepair mutation count = 0
- review-only route exists
- provider default calls = 0
- Node2 raw reveal access = 0
- raw manuscript leakage = 0
- credential leakage = 0
- canon auto-resolution blocked
- cross-project write blocked
- Gate26 advisory-only
- branchpoint survival pass
- docs/manifest evidence present

## Invariants

```json
{
  "provider_default_calls": 0,
  "live_provider_call_count_in_release_gate": 0,
  "cross_project_write_allowed": false,
  "canon_auto_resolution_count": 0,
  "auto_repair_mutation_count": 0,
  "runtime_training_enabled": false,
  "active_meta_learning_enabled": false,
  "model_weight_update_count": 0,
  "learning_allowed_count": 0,
  "training_triggered_count": 0,
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
Stage133  NarrativeStateTensor 8D Measurement Layer
Stage134  MetaLearner Audit Mode
Stage135  LearningQualityGate & Candidate Registry
```

## Next Direction

```text
Stage136 - SchemaRegistry
Stage137 - MigrationManager
Stage138 - LOSDB Storage Contracts
Stage139 - Corpus Governance Pipeline
Stage140 - Production Release Automation Closure
```

## Repository Evidence

- Stage manifest: `manifests/stage135_manifest.json`
- Live manifest: `manifests/live_core_manifest.json`
- Release report: `release/current/stage135_learning_quality_gate_report.json`
- Release gate: `release/current/stage135_release_gate_report.json`
- Official asset manifest: `release/current/stage135_official_asset_manifest.json`
