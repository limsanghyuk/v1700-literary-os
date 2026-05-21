# Stage143 Developer Handoff

## Required Deliverables

- `release/current/stage143_user_cli_api_docs_report.json`
- `release/current/stage143_release_gate_report.json`
- `release/current/stage143_release_asset_manifest.json`
- `release/current/stage143_user_cli_api_docs_pack/`
- `docs/user/cli_quickstart.md`
- `docs/user/api_minimum.md`
- `docs/user/examples/render_request.json`
- `docs/user/examples/render_response.json`
- `package_manifest.json`
- `FILELIST.txt`
- `SHA256SUMS.txt`
- official release ZIP and `.sha256` sidecar

## Completion Procedure

1. Run `python tools/run_mandatory_predevelopment_check.py`.
2. Run `python tools/check_stage_metadata_consistency.py`.
3. Run `python tools/check_release_asset_integrity.py`.
4. Run `python tools/run_stage140_release_integrity.py`.
5. Run `python tools/run_stage140_release_gate.py`.
6. Run `python tools/run_stage141_prose_generation_e2e.py`.
7. Run `python tools/run_stage141_release_gate.py`.
8. Run `python tools/run_stage142_longform_benchmark_pack.py`.
9. Run `python tools/run_stage142_release_gate.py`.
10. Run `python tools/run_stage143_user_cli_api_docs.py`.
11. Run `python tools/run_stage143_release_gate.py`.
12. Run `python tools/run_release_gate.py`.
13. Run `python tools/run_stage72_repo_doctor.py`.
14. Run the active-lineage pytest pack.
15. Build the integrated release ZIP, `.sha256`, `SHA256SUMS.txt`, and refresh `FILELIST.txt`.
16. Commit on a dedicated `stage143-*` branch.
17. Push branch, open PR, and wait for GitHub Actions to pass.
18. Merge PR, tag `v1700-stage143`, and publish release assets.
19. Replace any generic workflow-generated assets with the official Stage143 handoff ZIP if needed.

## Official Asset Policy

- The release page must expose the Stage143 ZIP named in `package_manifest.json`.
- The SHA256 sidecar must match the ZIP.
- `release/current/stage143_release_asset_manifest.json` is the local source of truth for release asset alignment.
