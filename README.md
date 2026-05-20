# V1700 Literary OS - Stage140

> Release Integrity & Product Proof Gate
> Provider-Zero AI longform novel and drama scenario generation system.

## Current Stage

Stage140 is the official active development baseline after Stage139. It converts Stage139 corpus-governance readiness into deterministic release integrity and product proof checks.

Stage140 remains a gate-only stage. It does not enable provider calls, runtime training, model updates, LOSDB writes, migration execution, canon mutation, or AutoRepair mutation.

## Quick Start

```bash
pip install -e ".[dev]"

python -m compileall -q src tools
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
python tools/run_stage139_corpus_governance_pipeline.py
python tools/run_stage139_release_gate.py
python tools/check_stage_metadata_consistency.py
python tools/check_release_asset_integrity.py
python tools/run_stage140_release_integrity.py
python tools/run_stage140_gate.py
python tools/run_release_gate.py
python tools/run_stage72_repo_doctor.py
```

## GitHub CI/CD

The repository uses GitHub Actions as the shared authority for work across multiple computers.

- `ci-core`: runs the full test suite, Stage134~Stage140 checks, the main release gate, repo doctor, and GitNexus/GraphNexus preflight checks.
- `cd-dry-run`: builds a release dry-run archive and SHA256 artifact on PR/push.
- `release`: runs on `v1700-stage*` or `v*` tags and publishes an integrated ZIP, SHA256 sidecar, and `SHA256SUMS.txt` snapshot as GitHub Release assets.

## Stage140 Core Modules

```text
src/v1700/release_integrity/
  contracts.py
  metadata_checker.py
  asset_checker.py
  report.py

src/v1700/product_proof/
  contracts.py
  sample_project_contract.py
  benchmark_contract.py

src/v1700/stage140/
  stage140_runner.py

src/v1700/gates/
  stage140_release_gate.py
```

## Stage140 Release Gate

The Stage140 gate validates:

- Stage139 baseline gate pass
- README, pyproject, live manifest, package manifest, release notes, and asset manifest consistency
- release asset declaration consistency
- synthetic sample project contract presence
- longform benchmark skeleton contract presence
- Stage141 product E2E readiness marker
- provider default calls = 0
- Node2 raw reveal access = 0
- branchpoint survival pass
- docs/manifest evidence present
- CI/release procedure alignment present

## Stage Lineage

```text
Stage134  MetaLearner Audit Mode
Stage135  LearningQualityGate & Candidate Registry
Stage136  SchemaRegistry
Stage137  MigrationManager
Stage138  LOSDB Storage Contracts
Stage139  Corpus Governance Pipeline
Stage140  Release Integrity & Product Proof Gate
```

## Next Direction

```text
Stage141 - Prose Generation E2E Harness
```

## Repository Evidence

- Stage manifest: `manifests/stage140_manifest.json`
- Live manifest: `manifests/live_core_manifest.json`
- Release report: `release/current/stage140_release_integrity_report.json`
- Release gate: `release/current/stage140_release_gate_report.json`
- Official asset manifest: `release/current/stage140_release_asset_manifest.json`
