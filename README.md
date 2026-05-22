# V1700 Literary OS - Stage146

> Narrative State Contract
> Provider-Zero AI longform novel and drama scenario generation system.

## Current Stage

Stage146 is the official active development baseline after Stage145. It turns the Page01 body constitution into canonical narrative state objects for series, episode, scene, character, world, reveal, and continuity layers.

Stage146 is not a memory or generation feature release. It hardens the Page01 contract before Stage147 Project Manifest Body, Stage148 Node Boundary Constitution, Stage149 Body Constitution Release Gate, and Stage150 Memory Body.

## Quick Start

```bash
pip install -e ".[dev]"

python -m compileall -q src tools
python -m pytest tests/test_stage135_learning_quality_gate.py tests/test_stage136_schema_registry.py tests/test_stage137_migration_manager.py tests/test_stage138_losdb_storage_contracts.py tests/test_stage139_corpus_governance_pipeline.py tests/test_stage140_release_integrity.py tests/test_stage141_prose_generation_e2e.py tests/test_stage142_longform_benchmark_pack.py tests/test_stage143_user_cli_api_docs.py tests/test_stage144_split_ci_runtime_strategy.py tests/test_stage145_body_constitution.py tests/test_stage146_narrative_state_contract.py tests/stage_gates/test_stage72_repo_doctor.py -q
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
python tools/run_release_gate.py
python tools/run_stage72_repo_doctor.py
```

## GitHub CI/CD

The repository uses GitHub Actions as the shared authority for work across multiple computers.

- `ci-fast`: runs current-stage invariant checks for Stage145 fast feedback.
- `ci-core`: runs the active-lineage regression pack, Stage134~Stage145 checks, the main release gate, repo doctor, and GitNexus/GraphNexus preflight checks.
- `ci-full`: runs scheduled or manual full-suite verification.
- `cd-dry-run`: builds a release dry-run archive and SHA256 artifact on PR/push.
- `release`: runs on `v1700-stage*` or `v*` tags and publishes an integrated ZIP, SHA256 sidecar, and `SHA256SUMS.txt` snapshot as GitHub Release assets.

## Stage146 Core Modules

```text
src/v1700/narrative_state/
  contracts.py
  series_state.py
  episode_state.py
  scene_state.py
  report.py

src/v1700/stage146/
  stage146_runner.py

src/v1700/gates/
  stage146_release_gate.py
```

## Stage146 Release Gate

The Stage146 gate validates:

- Stage145 baseline gate pass
- README, pyproject, live manifest, package manifest, release notes, and asset manifest consistency
- seven canonical state contracts
- series/episode/scene hierarchy
- continuity rulebook
- reveal boundary matrix
- Stage147 and Stage150 readiness declarations
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
```

## Next Direction

```text
Stage147  Project Manifest Body
Stage148  Node Boundary Constitution
Stage149  Body Constitution Release Gate
Stage150  Memory Body
```

## Repository Evidence

- Stage manifest: `manifests/stage146_manifest.json`
- Live manifest: `manifests/live_core_manifest.json`
- Release report: `release/current/stage146_narrative_state_contract_report.json`
- Release gate: `release/current/stage146_release_gate_report.json`
- Official asset manifest: `release/current/stage146_release_asset_manifest.json`
