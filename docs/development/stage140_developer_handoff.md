# Stage140 Developer Handoff

## Required Deliverables

- `release/current/stage140_release_integrity_report.json`
- `release/current/stage140_release_gate_report.json`
- `release/current/stage140_release_asset_manifest.json`
- `release/current/stage140_release_integrity_pack/`
- `package_manifest.json`
- `FILELIST.txt`
- `SHA256SUMS.txt`
- official release ZIP and `.sha256` sidecar

## Completion Procedure

1. Run `python tools/run_mandatory_predevelopment_check.py`.
2. Run `python tools/run_stage139_corpus_governance_pipeline.py`.
3. Run `python tools/run_stage139_release_gate.py`.
4. Run `python tools/check_stage_metadata_consistency.py`.
5. Run `python tools/check_release_asset_integrity.py`.
6. Run `python tools/run_stage140_release_integrity.py`.
7. Run `python tools/run_stage140_release_gate.py`.
8. Run `python tools/run_release_gate.py`.
9. Run `python tools/run_stage72_repo_doctor.py`.
10. Run `python -m pytest tests/test_stage135_learning_quality_gate.py tests/test_stage136_schema_registry.py tests/test_stage137_migration_manager.py tests/test_stage138_losdb_storage_contracts.py tests/test_stage139_corpus_governance_pipeline.py tests/test_stage140_release_integrity.py tests/stage_gates/test_stage72_repo_doctor.py -q`.
11. Build the integrated release ZIP, `.sha256`, `SHA256SUMS.txt`, and refresh `FILELIST.txt`.
12. Commit on a dedicated `stage140-*` branch.
13. Push branch, update the open PR, and wait for GitHub Actions to pass.
14. Merge PR, tag `v1700-stage140`, and publish release assets.
15. Replace any generic workflow-generated assets with the official Stage140 handoff ZIP if needed.

## Official Asset Policy

- The release page must expose the Stage140 ZIP named in `package_manifest.json`.
- The SHA256 sidecar must match the ZIP.
- `release/current/stage140_release_asset_manifest.json` is the local source of truth for release asset alignment.

## Invariants

- Provider calls remain zero in release gates.
- Runtime training remains disabled.
- Active meta-learning remains disabled.
- Model weight updates remain disabled.
- LOSDB writes remain disabled.
- Migration execution remains disabled.
- Canon auto-resolution remains disabled.
- AutoRepair mutation remains disabled.
