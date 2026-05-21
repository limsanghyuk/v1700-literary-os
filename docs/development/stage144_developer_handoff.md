# Stage144 Developer Handoff

## Scope

Stage144 closes the Stage140-144 roadmap by implementing the split CI/runtime strategy as a gated release artifact.

## Required Evidence

- `FILELIST.txt`
- `SHA256SUMS.txt`
- `release/current/stage144_split_ci_runtime_strategy_report.json`
- `release/current/stage144_release_gate_report.json`
- `release/current/stage144_release_asset_manifest.json`
- `release/current/stage144_split_ci_runtime_strategy_pack/`

## Required Workflows

- `.github/workflows/ci-fast.yml`
- `.github/workflows/ci-core.yml`
- `.github/workflows/ci-full.yml`
- `.github/workflows/cd-dry-run.yml`
- `.github/workflows/release.yml`

## Finalization Steps

1. Run compile, pytest, Stage143 baseline, and Stage144 tools.
2. Confirm metadata consistency and release asset integrity pass.
3. Confirm `ci-fast`, `ci-core`, `ci-full`, `cd-dry-run`, and `release` all exist and mention Stage144 tooling where required.
4. Refresh `FILELIST.txt` and `SHA256SUMS.txt`.
5. Push the branch, open the PR, verify Actions, and merge only after the Stage144 gates pass.
6. Create the Stage144 tag/release; the tagged `release` workflow builds the integrated release ZIP and `.sha256` sidecar from `package_manifest.json`.

## 2026-05-21 Integrity Notes

- `SHA256SUMS.txt` is excluded from `FILELIST.txt` to avoid self-referential checksum drift.
- Release asset integrity checks the exclusion policy, checksum coverage, extra checksum entries, listed file existence, and current digest matches.
- Generated `release/current/**/*_report.json` and `release/current/**/*_summary.json` files are still listed, but are exempt from content-digest blocking during gate execution because the gate commands rewrite them.
- Text-file checksum entries are based on LF-normalized bytes so Windows and Linux checkouts share the same ledger.
- Stage144 command wrappers must be runnable without setting `PYTHONPATH`.
- Stage144 command wrappers must return non-zero if the emitted report is blocked.
