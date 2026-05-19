# V1700 Literary OS - Stage134

> MetaLearner Audit Mode
> Provider-Zero AI longform novel and drama scenario generation system.

## Current Stage

Stage134 audits Stage133 NarrativeStateTensor output through a MetaLearner shell that is strictly audit-only. It records review and weight-candidate recommendations without training, mutating canon, updating weights, or activating repair.

The central rule is simple:

- Stage127 preflight and isolation audit remains required.
- Stage128 SharedWorld / SharedCharacter adapters remain read-only.
- Stage129 MultiWorkCIM and Cross-Work Canon Governor remain authoritative.
- Stage130 authorizes only the safe MultiWork operational surface.
- Stage131 keeps Gate26 advisory-only.
- Stage132 requires evidence before granting mystery exemption: a reveal lock and payoff budget must exist.
- Stage133 measures every Stage132 conflict category across eight local-only narrative state dimensions without mutating canon.
- Stage134 may recommend review or future weight-candidate tracking, but runtime training, active learning, canon auto-resolution, and AutoRepair mutation remain blocked.
- Cross-project write, raw manuscript sharing, direct V571 trunk merge, canon auto-resolution, Gate26 hard block, active learning, and AutoRepair mutation remain blocked.

## Quick Start

```bash
pip install -e ".[dev]"

python -m compileall src tools
python -m pytest tests/ -q
python tools/run_ci_dependency_preflight.py
python tools/run_stage134_meta_learner_audit.py
python tools/run_stage134_release_gate.py
python tools/run_stage133_narrative_state_tensor.py
python tools/run_stage133_release_gate.py
python tools/run_release_gate.py
python tools/run_stage72_repo_doctor.py
```

## GitHub CI/CD

The repository uses GitHub Actions as the shared authority for work across multiple computers.

- `ci-core`: runs on push, pull request, and version tags. It installs `.[dev]`, runs `pytest tests/ -q`, Stage134 release gate, the main release gate, repo doctor, and GitNexus/GraphNexus preflight checks.
- `ci-full`: scheduled/manual full-lineage verification.
- `release`: runs on `v1700-stage*` or `v*` tags and publishes an integrated ZIP, SHA256 sidecar, and `SHA256SUMS.txt` snapshot as GitHub Release assets.

## Stage134 Core Modules

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

## Stage133 Foundation Modules

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

## Stage134 Release Gate

The Stage134 gate validates:

- Stage133 baseline gate pass
- MetaLearner audit report pass
- audit-only mode is enforced
- runtime training disabled
- active learning disabled
- model weight update count = 0
- AutoRepair mutation count = 0
- review recommendation exists for true contradiction
- Gate26 remains advisory-only
- canon auto-resolution blocked
- cross-project write blocked
- provider default calls = 0
- Node2 raw reveal access = 0
- raw manuscript leakage = 0
- credential leakage = 0
- GitNexus/Python fallback preflight pass
- branchpoint survival pass
- repo doctor active stage ready

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
Stage133  NarrativeStateTensor 8D Measurement Layer
Stage134  MetaLearner Audit Mode
```

## Next Direction

```text
Stage135 - Bounded Active MetaLearner
Stage136 - ASD Patch Proposal Mode
```

## Repository Evidence

- Stage manifest: `manifests/stage134_manifest.json`
- Live manifest: `manifests/live_core_manifest.json`
- Release report: `release/current/stage134_meta_learner_audit_report.json`
- Release gate: `release/current/stage134_release_gate_report.json`
