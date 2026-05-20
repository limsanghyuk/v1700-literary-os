# Stage139 Developer Handoff

## Required Deliverables

- `release/current/stage139_corpus_governance_pipeline_report.json`
- `release/current/stage139_release_gate_report.json`
- `release/current/stage139_corpus_governance_pipeline_pack/`
- `release/current/stage139_release_asset_manifest.json`
- `package_manifest.json`
- `FILELIST.txt`
- `SHA256SUMS.txt`
- official release ZIP and `.sha256` sidecar

## Completion Procedure

1. Run `python tools/run_mandatory_predevelopment_check.py`.
2. Run `python tools/run_stage139_corpus_governance_pipeline.py`.
3. Run `python tools/run_stage139_release_gate.py`.
4. Run `python tools/run_release_gate.py`.
5. Run `python tools/run_stage72_repo_doctor.py`.
6. Run `python -m pytest tests/ -q`.
7. Build the integrated release ZIP, `.sha256`, `SHA256SUMS.txt`, and refresh `FILELIST.txt`.
8. Commit on a dedicated `stage139-*` branch.
9. Push branch, open PR, and wait for GitHub Actions to pass.
10. Merge PR, tag `v1700-stage139`, and publish release assets.
11. Replace any generic workflow-generated assets with the official Stage139 handoff ZIP if needed.

## Official Asset Policy

- The release page must expose the Stage139 ZIP named in `package_manifest.json`.
- The SHA256 sidecar must match the ZIP.
- `release/current/stage139_release_asset_manifest.json` is the local source of truth for release asset alignment.
