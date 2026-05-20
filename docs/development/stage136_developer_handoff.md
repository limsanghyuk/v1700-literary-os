# Stage136 Developer Handoff

## Required Deliverables

- `release/current/stage136_schema_registry_report.json`
- `release/current/stage136_release_gate_report.json`
- `release/current/stage136_schema_registry_pack/`
- `release/current/stage136_release_asset_manifest.json`
- `package_manifest.json`
- `FILELIST.txt`
- `SHA256SUMS.txt`
- official release ZIP and `.sha256` sidecar

## Completion Procedure

1. Run `python tools/run_mandatory_predevelopment_check.py`.
2. Run `python tools/run_stage136_schema_registry.py`.
3. Run `python tools/run_stage136_release_gate.py`.
4. Run `python tools/run_release_gate.py`.
5. Run `python tools/run_stage72_repo_doctor.py`.
6. Run `python -m pytest tests/ -q`.
7. Build the integrated release ZIP, `.sha256`, `SHA256SUMS.txt`, and refresh `FILELIST.txt`.
8. Commit on a dedicated `stage136-*` branch.
9. Push branch, open PR, and wait for GitHub Actions to pass.
10. Merge PR, tag `v1700-stage136`, and publish release assets.
11. Replace any generic workflow-generated assets with the official Stage136 handoff ZIP if needed.

## Official Asset Policy

- The release page must expose the Stage136 ZIP named in `package_manifest.json`.
- The SHA256 sidecar must match the ZIP.
- `release/current/stage136_release_asset_manifest.json` is the local source of truth for release asset alignment.
