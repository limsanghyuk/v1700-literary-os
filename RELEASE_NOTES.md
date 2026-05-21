# V1700 Stage144 - Split CI Runtime Strategy

Stage144 is the CI/runtime split layer after Stage143. It formalizes `ci-fast`, `ci-core`, `ci-full`, `cd-dry-run`, and `release` responsibilities while keeping migration execution, LOSDB writes, runtime training, active learning, model weight updates, provider calls, canon mutation, and AutoRepair mutation blocked.

## Release Highlights

- Stage134 remains audit-only, Stage135 remains candidate-only, Stage136 remains schema-only, Stage137 remains migration-plan-only, Stage138 remains storage-contract-catalog-only, Stage139 remains corpus-governance-pipeline-only, Stage140 remains release-integrity-gate-only, Stage141 remains local-E2E-only, Stage142 remains benchmark-pack-only, Stage143 remains docs-only, and Stage144 remains workflow-split-only.
- README, pyproject, package manifest, live manifest, and release notes are checked for deterministic Stage144 alignment.
- Release asset declarations are verified against the canonical Stage144 package contract.
- The repository now emits workflow inventory, runtime lane matrix, workflow trigger summary, and a release surface contract.
- Stage144 is the current roadmap terminus.
- Migration execution remains disabled.
- LOSDB writes remain disabled.
- Runtime training remains disabled.
- Active meta-learning remains disabled.
- Model weight updates remain blocked.
- Provider calls remain zero in release gates.
- Node2 raw reveal access remains zero.
- Canon auto-resolution and AutoRepair mutation remain blocked.

## Verification

The release workflow verifies the repository before publishing release assets:

```bash
python -m compileall -q src tools
python -m pytest tests/test_stage135_learning_quality_gate.py tests/test_stage136_schema_registry.py tests/test_stage137_migration_manager.py tests/test_stage138_losdb_storage_contracts.py tests/test_stage139_corpus_governance_pipeline.py tests/test_stage140_release_integrity.py tests/test_stage141_prose_generation_e2e.py tests/test_stage142_longform_benchmark_pack.py tests/test_stage143_user_cli_api_docs.py tests/test_stage144_split_ci_runtime_strategy.py tests/stage_gates/test_stage72_repo_doctor.py -q
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
python tools/run_release_gate.py
python tools/run_stage72_repo_doctor.py
python tools/run_ci_dependency_preflight.py
```

## Official Artifacts

The official Stage144 handoff assets are:

- `V1700_stage144_split_ci_runtime_strategy_release_integrated_repository_with_artifacts.zip`
- `V1700_stage144_split_ci_runtime_strategy_release_integrated_repository_with_artifacts.zip.sha256`
