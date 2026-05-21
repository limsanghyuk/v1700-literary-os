# Stage144 Proposal - Split CI Runtime Strategy

Stage144 converts the Stage143 CI/runtime readiness marker into a declared and gated operating model.

## Problem

By Stage143 the repository had enough release evidence to justify separate fast, core, full, and release-oriented automation lanes, but the split itself was still implicit.

## Proposal

Add a Stage144 workflow contract that:

- introduces a dedicated `ci-fast` lane
- preserves `ci-core`, `ci-full`, `cd-dry-run`, and `release` as distinct responsibilities
- records the runtime lane matrix as release evidence
- makes the split part of the release gate

## Required Invariants

- Provider calls remain disabled.
- Runtime training remains disabled.
- Active meta-learning remains disabled.
- Model weight updates remain disabled.
- LOSDB writes remain disabled.
- Migration execution remains disabled.
- Node2 raw reveal access remains zero.
- Raw manuscript leakage remains zero.

## Implementation Status

As of 2026-05-21, Stage144 is implemented and release-gated.

- `ci-fast`, `ci-core`, `ci-full`, `cd-dry-run`, and `release` are declared as separate workflow lanes.
- Stage144 command wrappers are self-contained from a fresh checkout and insert `src` into `sys.path`.
- Stage144 wrappers return a non-zero process status when their report status is not `pass`.
- Release asset integrity verifies `FILELIST.txt` and `SHA256SUMS.txt` coverage, extra entries, file existence, and current file digests.
- `SHA256SUMS.txt` is intentionally excluded from `FILELIST.txt` to avoid self-referential checksum drift; the policy is checked by the release asset integrity gate.
- Workflow contract checks cover required trigger declarations, Stage144 command presence, dry-run package artifacts, and release package/sidecar publication.

## Current Verification

The current Stage144 evidence set is aligned with:

- `python tools/run_stage144_split_ci_runtime_strategy.py`
- `python tools/run_stage144_release_gate.py`
- `python tools/check_release_asset_integrity.py`
- `python -m pytest tests/test_stage144_split_ci_runtime_strategy.py -q`
- `python -m compileall -q src tools`

The canonical release ZIP and `.sha256` sidecar are produced by the tagged GitHub `release` workflow from `package_manifest.json`.
