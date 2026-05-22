# V1700 Literary OS - Stage147

> Project Manifest Body
> Provider-Zero AI longform novel and drama scenario generation system.

## Current Stage

Stage147 is the official active development baseline after Stage146. It binds the synthetic sample project to the canonical narrative state contracts and materializes a read-only manifest body for series, episode, scene, character, world, reveal, and continuity packets.

Stage147 is not a memory or generation feature release. It hardens the Page01 manifest packet surface before Stage148 Node Boundary Constitution, Stage149 Body Constitution Release Gate, and Stage150 Memory Body.

## Quick Start

```bash
pip install -e ".[dev]"

python -m compileall -q src tools
python -m pytest tests/test_stage135_learning_quality_gate.py tests/test_stage136_schema_registry.py tests/test_stage137_migration_manager.py tests/test_stage138_losdb_storage_contracts.py tests/test_stage139_corpus_governance_pipeline.py tests/test_stage140_release_integrity.py tests/test_stage141_prose_generation_e2e.py tests/test_stage142_longform_benchmark_pack.py tests/test_stage143_user_cli_api_docs.py tests/test_stage144_split_ci_runtime_strategy.py tests/test_stage145_body_constitution.py tests/test_stage146_narrative_state_contract.py tests/test_stage147_project_manifest_body.py tests/stage_gates/test_stage72_repo_doctor.py -q
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
python tools/run_stage140_release_gate.py
python tools/run_stage141_prose_generation_e2e.py
python tools/run_stage141_release_gate.py
python tools/run_stage142_longform_benchmark_pack.py
python tools/run_stage142_release_gate.py
python tools/run_stage143_user_cli_api_docs.py
python tools/run_stage143_release_gate.py
python tools/run_stage144_split_ci_runtime_strategy.py
python tools/run_stage144_release_gate.py
python tools/run_stage145_body_constitution.py
python tools/run_stage145_body_constitution_gate.py
python tools/run_stage146_narrative_state_contract.py
python tools/run_stage146_release_gate.py
python tools/run_stage147_project_manifest_body.py
python tools/run_stage147_release_gate.py
python tools/run_release_gate.py
python tools/run_stage72_repo_doctor.py
```

## GitHub CI/CD

The repository uses GitHub Actions as the shared authority for work across multiple computers.

- `ci-fast`: runs current-stage invariant checks for Stage147 fast feedback.
- `ci-core`: runs the active-lineage regression pack, Stage134~Stage145 checks, the main release gate, repo doctor, and GitNexus/GraphNexus preflight checks.
- `ci-full`: runs scheduled or manual full-suite verification.
- `cd-dry-run`: builds a release dry-run archive and SHA256 artifact on PR/push.
- `release`: runs on `v1700-stage*` or `v*` tags and publishes an integrated ZIP, SHA256 sidecar, and `SHA256SUMS.txt` snapshot as GitHub Release assets.

## Stage147 Core Modules

```text
src/v1700/project_manifest_body/
  contracts.py
  loader.py
  report.py

src/v1700/stage147/
  stage147_runner.py

src/v1700/gates/
  stage147_release_gate.py
```

## Stage147 Release Gate

The Stage147 gate validates:

- Stage146 baseline gate pass
- README, pyproject, live manifest, package manifest, release notes, and asset manifest consistency
- canonical manifest bundle coverage
- project manifest catalog coverage
- manifest-state binding coverage
- synthetic/public-safe/provider-zero/raw-manuscript-free policy boundaries
- deterministic manifest load order
- Stage148 and Stage150 readiness declarations
- provider default calls = 0
- runtime training disabled
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
Stage141  Prose Generation E2E Harness
Stage142  Longform Benchmark Pack
Stage143  User CLI/API Minimum Docs
Stage144  Split CI Runtime Strategy
Stage145  Body Constitution
Stage146  Narrative State Contract
Stage147  Project Manifest Body
```

## Next Direction

```text
Stage148  Node Boundary Constitution
Stage149  Body Constitution Release Gate
Stage150  Memory Body
```

## Repository Evidence

- Stage manifest: `manifests/stage147_manifest.json`
- Live manifest: `manifests/live_core_manifest.json`
- Release report: `release/current/stage147_project_manifest_body_report.json`
- Release gate: `release/current/stage147_release_gate_report.json`
- Official asset manifest: `release/current/stage147_release_asset_manifest.json`
