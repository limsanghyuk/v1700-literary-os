# CI and Release

- `ci-core`: fast unit/integration/runtime checks
- `ci-full`: full lineage and regression checks
- release evidence goes to `release/current`
- historical packages are release assets, not default tracked files
- Stage138 release flow runs `run_stage138_losdb_storage_contracts.py`, `run_stage138_release_gate.py`, `run_release_gate.py`, and `run_stage72_repo_doctor.py` before tag publication
- the official Stage138 ZIP name must match `package_manifest.json` and `release/current/stage138_release_asset_manifest.json`
