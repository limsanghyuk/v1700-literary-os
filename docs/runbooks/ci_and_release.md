# CI and Release

- `ci-core`: fast unit/integration/runtime checks
- `ci-full`: full lineage and regression checks
- release evidence goes to `release/current`
- historical packages are release assets, not default tracked files
- Stage137 release flow runs `run_stage137_migration_manager.py`, `run_stage137_release_gate.py`, `run_release_gate.py`, and `run_stage72_repo_doctor.py` before tag publication
- the official Stage137 ZIP name must match `package_manifest.json` and `release/current/stage137_release_asset_manifest.json`
