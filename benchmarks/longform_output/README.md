# Stage142 Longform Benchmark Pack

This benchmark pack is a public-safe Stage142 longform benchmark authority.

It now includes deterministic multi-case Stage142 benchmark results while still avoiding provider calls, private manuscripts, and training flows.

## Scope

- Stage140 validates benchmark contract presence only.
- Stage141 attaches deterministic prose-generation E2E results under `results/`.
- Stage142 upgrades the result set into a multi-case benchmark scoreboard and rendered sample bundle.
- All sample inputs are synthetic placeholders.
- Provider calls remain disabled by default.

## Expected command path

```bash
python tools/check_stage_metadata_consistency.py
python tools/check_release_asset_integrity.py
python tools/run_stage140_release_integrity.py
python tools/run_stage140_release_gate.py
python tools/run_stage141_prose_generation_e2e.py
python tools/run_stage141_release_gate.py
python tools/run_stage142_longform_benchmark_pack.py
python tools/run_stage142_release_gate.py
```
