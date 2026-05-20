# CI and Release

- `ci-core`: fast unit/integration/runtime checks
- `ci-full`: full lineage and regression checks
- release evidence goes to `release/current`
- historical packages are release assets, not default tracked files
- Stage136 release flow runs `run_stage136_schema_registry.py`, `run_stage136_release_gate.py`, `run_release_gate.py`, and `run_stage72_repo_doctor.py` before tag publication
- the official Stage136 ZIP name must match `package_manifest.json` and `release/current/stage136_release_asset_manifest.json`
