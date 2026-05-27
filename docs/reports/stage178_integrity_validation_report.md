# Stage178 Integrity Validation Report

## Scope

- Target: `Stage178 - Page06 Release Seal`
- Review lenses:
  - chief architect: release authority, lineage seal, platform invariance
  - chief compiler: deterministic bytes, reproducible checksum ledger, CI/local parity

## Findings

1. `Stage178` logic and gate flow were already correct.
2. `check_release_asset_integrity.py` could still block on Windows even when GitHub Actions passed on Linux.
3. The mismatch came from hashing checkout bytes directly, which made `SHA256SUMS.txt` sensitive to `CRLF` vs `LF`.

## Risk

- false negative local release integrity verdicts
- developers regenerating different ledgers on different operating systems
- authority drift between local audit results and GitHub CI

## Resolution

- canonicalized text hashing inside `src/v1700/release_integrity/asset_checker.py`
- preserved raw hashing for non-UTF-8 / binary files
- added `tools/regenerate_sha256sums.py` to rebuild `SHA256SUMS.txt` from the canonical rule
- added regression tests covering `LF` and `CRLF` equivalence
- updated workflow and predevelopment guidance to use the canonical checksum regeneration path

## Validation

- `python tools/run_mandatory_predevelopment_check.py`
- `gitnexus.cmd analyze --force`
- `gitnexus.cmd status`
- `python tools/regenerate_sha256sums.py`
- `python tools/check_release_asset_integrity.py`
- `python tools/run_stage178_page06_release_seal.py`
- `python tools/run_stage178_release_gate.py`
- `python tools/run_release_gate.py`
- `python tools/run_stage72_repo_doctor.py`
- `python -m pytest tests/test_release_asset_integrity.py tests/test_stage174_release_policy_registry.py tests/test_stage175_project_boundary_governor.py tests/test_stage176_lineage_review_gate.py tests/test_stage177_operational_safety_rollback_governance.py tests/test_stage178_page06_release_seal.py tests/stage_gates/test_stage72_repo_doctor.py -q`

## Final Verdict

`Stage178` is sealed and logically sound, and its release integrity path is now deterministic across local Windows audits and Linux CI.
