# V1700 Literary OS - Stage138

> LOSDB Storage Contracts
> Provider-Zero AI longform novel and drama scenario generation system.

## Current Stage

Stage138 is the official active development baseline after Stage137. It converts Stage137 migration planning authority into a deterministic LOSDB storage contract catalog while keeping migration execution, LOSDB writes, runtime training, active learning, model weight updates, canon mutation, provider calls, and AutoRepair mutation blocked.

The central rule is simple:

- Stage134 remains audit-only.
- Stage135 remains candidate-only.
- Stage136 remains schema-only.
- Stage137 remains migration-plan-only.
- Stage138 is storage-contract-catalog-only.
- Review-required cases stay in `REVIEW_ONLY`.
- Future governance metadata may be prepared, but no write or migration execution is allowed.
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
python tools/run_stage137_migration_manager.py
python tools/run_stage137_release_gate.py
python tools/run_stage138_losdb_storage_contracts.py
python tools/run_stage138_release_gate.py
python tools/run_release_gate.py
python tools/run_stage72_repo_doctor.py
```

## GitHub CI/CD

The repository uses GitHub Actions as the shared authority for work across multiple computers.

- `ci-core`: runs on push, pull request, and version tags. It installs `.[dev]`, runs `pytest tests/ -q`, Stage134 baseline checks, Stage135 LearningQualityGate, Stage136 SchemaRegistry, Stage137 MigrationManager, Stage138 LOSDB Storage Contracts, the stage release gates, the main release gate, repo doctor, and GitNexus/GraphNexus preflight checks.
- `cd-dry-run`: builds a release dry-run archive and SHA256 artifact on PR/push.
- `release`: runs on `v1700-stage*` or `v*` tags and publishes an integrated ZIP, SHA256 sidecar, and `SHA256SUMS.txt` snapshot as GitHub Release assets.

## Stage138 Core Modules

```text
src/v1700/losdb_storage_contracts/
  contracts.py
  gate.py
  preflight.py
  report.py

src/v1700/stage138/
  stage138_runner.py

src/v1700/gates/
  stage138_release_gate.py
```

## Stage137 Baseline Modules

```text
src/v1700/migration_manager/
  contracts.py
  gate.py
  preflight.py
  report.py

src/v1700/stage137/
  stage137_runner.py

src/v1700/gates/
  stage137_release_gate.py
```

## Stage138 Release Gate

The Stage138 gate validates:

- Stage137 baseline gate pass
- storage contract report pass
- storage contract catalog present
- schema contracts present
- every Stage137 binding route is covered
- review approval lane preserved
- dependency metadata preserved
- namespace uniqueness preserved
- rollback metadata present for every contract item
- Stage139 governance readiness present
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
  "storage_contract_catalog_only": true,
  "migration_execution_enabled": false,
  "losdb_write_enabled": false,
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
Stage137  MigrationManager
Stage138  LOSDB Storage Contracts
```

## Next Direction

```text
Stage139 - Corpus Governance Pipeline
Stage140 - Production Release Automation Closure
```

## Repository Evidence

- Stage manifest: `manifests/stage138_manifest.json`
- Live manifest: `manifests/live_core_manifest.json`
- Release report: `release/current/stage138_losdb_storage_contracts_report.json`
- Release gate: `release/current/stage138_release_gate_report.json`
- Official asset manifest: `release/current/stage138_release_asset_manifest.json`
