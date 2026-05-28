# Contributing to V1700 Literary OS

## Branch Policy

- `main` is the verified integration branch.
- Use `stageNNN-topic` for stage work.
- Use `hotfix-stageNNN-topic` for release-authority repairs after a sealed stage.
- Use `docs-workflow-topic` for workflow and protocol upgrades.
- Do not merge a branch into `main` unless CI, release gates, repo doctor, metadata consistency, and release-asset integrity pass.

## Required Local Checks

Before planning, implementation, or opening a pull request:

```bash
python -m pip install -e ".[dev]"
python tools/install_predevelopment_hooks.py
python tools/session_start.py
python -m compileall -q src tools
python tools/run_mandatory_predevelopment_check.py
python tools/check_stage_metadata_consistency.py
python tools/check_release_asset_integrity.py
python tools/run_stage184_release_gate.py
python tools/run_release_gate.py
python tools/run_stage72_repo_doctor.py
python -m pytest tests/test_mandatory_predevelopment_check.py tests/test_session_start.py tests/test_precommit_guard.py tests/test_release_asset_integrity.py tests/test_stage179_evolution_contract.py tests/test_stage180_architecture_drift_self_audit.py tests/test_stage181_migration_plan_compiler.py tests/test_stage182_upgrade_simulation_compatibility_sandbox.py tests/test_stage183_future_absorption_deprecation_planner.py tests/test_stage184_page07_release_seal.py tests/stage_gates/test_stage72_repo_doctor.py -q
```

## Version Tags

Use annotated stage tags for release points:

```bash
git tag -a v1700-stage131 -m "V1700 Stage131 <title>"
git push origin v1700-stage131
```

The release workflow publishes an integrated ZIP and SHA256 sidecar for pushed tags.

## Two-Machine Workflow

Do not move source code by ZIP as the primary workflow. Use GitHub as the source of truth:

```bash
git fetch --all --tags --prune
git checkout main
git pull --ff-only origin main
python tools/session_start.py
git checkout -b stage184-workflow-upgrade
```

If another machine has different work, push it as a branch and compare it with `main` rather than copying files over Google Drive.

## Session Closure

- update docs and `docs/sessions/` when authority changes
- run `python tools/session_end.py`
- commit and push the branch when the work unit is complete
