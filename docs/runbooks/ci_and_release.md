# CI and Release

- `ci-core`: active-lineage regression pack plus runtime/release checks
- `ci-full`: full lineage and regression checks
- release evidence goes to `release/current`
- historical packages are release assets, not default tracked files
- Stage140 release flow runs `check_stage_metadata_consistency.py`, `check_release_asset_integrity.py`, `run_stage140_release_integrity.py`, `run_stage140_release_gate.py`, `run_release_gate.py`, and `run_stage72_repo_doctor.py` before tag publication
- the official Stage140 ZIP name must match `package_manifest.json` and `release/current/stage140_release_asset_manifest.json`
