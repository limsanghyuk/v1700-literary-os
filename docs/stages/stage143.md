# Stage143 - User CLI/API Minimum Docs

Stage143 upgrades the Stage142 benchmark baseline into minimum user-facing CLI and API documentation.

## Purpose

- Lock the current CLI entrypoint, flags, and example outputs into user-facing documentation.
- Publish a documentation-only minimum API contract without enabling a live service.
- Preserve provider-zero, write-zero, and training-zero boundaries while preparing Stage144 CI/runtime split work.

## Blocked

- Provider calls.
- Runtime training.
- Active meta-learning.
- Model weight updates.
- LOSDB write path.
- Migration execution.
- Canon auto-resolution.
- AutoRepair mutation.

## Evidence

- `release/current/stage143_user_cli_api_docs_report.json`
- `release/current/stage143_release_gate_report.json`
- `release/current/stage143_release_asset_manifest.json`
- `release/current/stage143_user_cli_api_docs_pack/`
- `docs/user/cli_quickstart.md`
- `docs/user/api_minimum.md`
