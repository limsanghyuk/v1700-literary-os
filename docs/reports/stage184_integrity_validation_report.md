# Stage184 Integrity Validation Report

## Scope

- Target: `Stage184 - Page07 Release Seal`
- Review lenses:
  - chief architect: release authority, Page07 seal continuity, future-stage handoff stability
  - chief compiler: deterministic bytes, reproducible checksum ledger, Windows/Linux parity

## Findings

1. `Stage179` through `Stage184` logic and gate flow were already structurally sound.
2. `check_release_asset_integrity.py` could still block on Windows because `SHA256SUMS.txt` was evaluated against checkout bytes instead of canonical text bytes.
3. The mismatch affected authority files and generated seal artifacts even though the stage logic itself remained correct.

## Risk

- false-negative local release integrity verdicts for Page07
- different checksum ledgers regenerated on Windows and Linux
- release authority drift between developer audit results and GitHub CI

## Resolution

- canonicalized text hashing inside `src/v1700/release_integrity/asset_checker.py`
- preserved raw hashing behavior for binary and non-UTF-8 files
- aligned `tools/regenerate_sha256sums.py` with the canonical checksum authority path
- retained CRLF/LF normalization regression coverage in `tests/test_release_asset_integrity.py`
- updated README and workflow/predevelopment guidance to regenerate `SHA256SUMS.txt` before release-asset validation

## Validation

- `python -m compileall -q src tools tests`
- `python tools/run_mandatory_predevelopment_check.py`
- `gitnexus.cmd analyze --force`
- `gitnexus.cmd status`
- `python tools/regenerate_sha256sums.py`
- `python tools/check_release_asset_integrity.py`
- `python tools/run_stage184_page07_release_seal.py`
- `python tools/run_stage184_release_gate.py`
- `python tools/run_release_gate.py`
- `python tools/run_stage72_repo_doctor.py`
- `python -m pytest tests/test_release_asset_integrity.py tests/test_stage179_evolution_contract.py tests/test_stage180_architecture_drift_self_audit.py tests/test_stage181_migration_plan_compiler.py tests/test_stage182_upgrade_simulation_compatibility_sandbox.py tests/test_stage183_future_absorption_deprecation_planner.py tests/test_stage184_page07_release_seal.py tests/stage_gates/test_stage72_repo_doctor.py -q`

## Final Verdict

`Stage184` is sealed and logically sound, and its release integrity path is now deterministic across local Windows audits and Linux CI.
