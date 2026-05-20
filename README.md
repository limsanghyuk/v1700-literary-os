# V1700 Literary OS - Stage136

> SchemaRegistry
> Provider-Zero AI longform novel and drama scenario generation system.

## Current Stage

Stage136 is the official active development baseline after Stage135. It converts Stage135 candidate-only output into a deterministic schema registry while keeping LOSDB writes, migration execution, runtime training, active learning, model weight updates, canon mutation, provider calls, and AutoRepair mutation blocked.

The central rule is simple:

- Stage134 remains audit-only.
- Stage135 remains candidate-only.
- Stage136 is schema-only.
- Review-required cases stay in `REVIEW_ONLY`.
- Future migration metadata may be prepared, but no write or migration execution is allowed.
- Runtime training remains disabled.
- Active meta-learning remains disabled.
- Model weight update count remains zero.
- LOSDB write count remains zero.
- Migration execution count remains zero.
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
python tools/run_stage136_schema_registry.py
python tools/run_stage136_release_gate.py
python tools/run_release_gate.py
python tools/run_stage72_repo_doctor.py
```

## GitHub CI/CD

The repository uses GitHub Actions as the shared authority for work across multiple computers.

- `ci-core`: runs on push, pull request, and version tags. It installs `.[dev]`, runs `pytest tests/ -q`, Stage134 baseline checks, Stage135 LearningQualityGate, Stage136 SchemaRegistry, the stage release gates, the main release gate, repo doctor, and GitNexus/GraphNexus preflight checks.
- `cd-dry-run`: builds a release dry-run archive and SHA256 artifact on PR/push.
- `release`: runs on `v1700-stage*` or `v*` tags and publishes an integrated ZIP, SHA256 sidecar, and `SHA256SUMS.txt` snapshot as GitHub Release assets.

## Stage136 Core Modules

```text
src/v1700/schema_registry/
  contracts.py
  gate.py
  preflight.py
  report.py

src/v1700/stage136/
  stage136_runner.py

src/v1700/gates/
  stage136_release_gate.py
```

## Stage135 Baseline Modules

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

## Stage136 Release Gate

The Stage136 gate validates:

- Stage135 baseline gate pass
- SchemaRegistry report pass
- schema catalog present
- every candidate is bound to a schema
- migration-ready metadata present
- storage-contract-ready metadata present
- LOSDB write blocked
- migration execution blocked
- provider default calls = 0
- Node2 raw reveal access = 0
- raw manuscript leakage = 0
- credential leakage = 0
- branchpoint survival pass
- docs/manifest evidence present
- CI/release procedure alignment present

## Invariants

```json
{
  "provider_default_calls": 0,
  "live_provider_call_count_in_release_gate": 0,
  "losdb_write_enabled": false,
  "migration_execution_enabled": false,
  "storage_contract_write_enabled": false,
  "cross_project_write_allowed": false,
  "canon_auto_resolution_count": 0,
  "auto_repair_mutation_count": 0,
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
Stage136  SchemaRegistry
```

## Next Direction

```text
Stage137 - MigrationManager
Stage138 - LOSDB Storage Contracts
Stage139 - Corpus Governance Pipeline
Stage140 - Production Release Automation Closure
```

## Repository Evidence

- Stage manifest: `manifests/stage136_manifest.json`
- Live manifest: `manifests/live_core_manifest.json`
- Release report: `release/current/stage136_schema_registry_report.json`
- Release gate: `release/current/stage136_release_gate_report.json`
- Official asset manifest: `release/current/stage136_release_asset_manifest.json`
