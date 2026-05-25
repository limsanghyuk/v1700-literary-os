# Stage163 Developer Handoff

Stage163 is complete when the deterministic render plan builder is connected to code, tools, tests, docs, manifests, release evidence, release gate, repo doctor, metadata consistency, asset integrity, and a clean ZIP artifact.

## Required commands

```bash
python -m compileall -q src tools
python tools/run_mandatory_predevelopment_check.py
python tools/check_stage_metadata_consistency.py
python tools/check_release_asset_integrity.py
python tools/run_stage162_release_gate.py
python tools/run_stage163_deterministic_render_plan_builder.py
python tools/run_stage163_release_gate.py
python tools/run_release_gate.py
python tools/run_stage72_repo_doctor.py
python -m pytest tests/test_stage163_deterministic_render_plan_builder.py -q
```

## Handoff rule

If web tooling cannot push the full repository tree, use the ZIP as canonical handoff and mirror it through local Codex or Antigravity to `stage163-deterministic-render-plan-builder`.
