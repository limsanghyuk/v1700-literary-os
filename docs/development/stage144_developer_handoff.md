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
5. Build the integrated release ZIP, `.sha256`, `SHA256SUMS.txt`, and refresh `FILELIST.txt`.
6. Push the branch, open the PR, verify Actions, merge, tag, and release.
