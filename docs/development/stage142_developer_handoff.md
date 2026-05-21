# Stage142 Developer Handoff

## Required Deliverables

- `release/current/stage142_longform_benchmark_pack_report.json`
- `release/current/stage142_release_gate_report.json`
- `release/current/stage142_release_asset_manifest.json`
- `release/current/stage142_longform_benchmark_pack/`
- `benchmarks/longform_output/results/stage142_benchmark_pack_summary.json`
- `benchmarks/longform_output/results/stage142_rendered_samples.json`
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
10. Run `python tools/run_release_gate.py`.
11. Run `python tools/run_stage72_repo_doctor.py`.
12. Run the active-lineage pytest pack.
13. Build the integrated release ZIP, `.sha256`, `SHA256SUMS.txt`, and refresh `FILELIST.txt`.
14. Commit on a dedicated `stage142-*` branch.
15. Push branch, open PR, and wait for GitHub Actions to pass.
16. Merge PR, tag `v1700-stage142`, and publish release assets.
17. Replace any generic workflow-generated assets with the official Stage142 handoff ZIP if needed.

## Official Asset Policy

- The release page must expose the Stage142 ZIP named in `package_manifest.json`.
- The SHA256 sidecar must match the ZIP.
- `release/current/stage142_release_asset_manifest.json` is the local source of truth for release asset alignment.
