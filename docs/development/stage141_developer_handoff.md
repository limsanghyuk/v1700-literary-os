# Stage141 Developer Handoff

## Required Deliverables

- `release/current/stage141_prose_generation_e2e_report.json`
- `release/current/stage141_release_gate_report.json`
- `release/current/stage141_release_asset_manifest.json`
- `release/current/stage141_prose_generation_e2e_pack/`
- `benchmarks/longform_output/results/stage141_scene_001_benchmark_result.json`
- `benchmarks/longform_output/results/stage141_scene_001_rendered.md`
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
8. Run `python tools/run_release_gate.py`.
9. Run `python tools/run_stage72_repo_doctor.py`.
10. Run the active-lineage pytest pack.
11. Build the integrated release ZIP, `.sha256`, `SHA256SUMS.txt`, and refresh `FILELIST.txt`.
12. Commit on a dedicated `stage141-*` branch.
13. Push branch, open PR, and wait for GitHub Actions to pass.
14. Merge PR, tag `v1700-stage141`, and publish release assets.
15. Replace any generic workflow-generated assets with the official Stage141 handoff ZIP if needed.

## Official Asset Policy

- The release page must expose the Stage141 ZIP named in `package_manifest.json`.
- The SHA256 sidecar must match the ZIP.
- `release/current/stage141_release_asset_manifest.json` is the local source of truth for release asset alignment.
