# Stage164 Developer Handoff

Stage164 is complete when the local dry-run renderer, report, release gate, manifests, docs, tests, and release asset manifest all pass.

## Required commands

```bash
python -m compileall -q src tools
python tools/run_mandatory_predevelopment_check.py
python tools/run_stage164_surface_draft_dry_run_renderer.py
python tools/run_stage164_release_gate.py
python tools/run_release_gate.py
python tools/run_stage72_repo_doctor.py
python -m pytest tests/test_stage164_surface_draft_dry_run_renderer.py -q
```

## Next

Stage165 — Render Quality and Boundary Preflight.
