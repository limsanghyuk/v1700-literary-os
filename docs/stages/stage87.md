# Stage87 — 8-16 Episode Scale-up Evidence

Stage87 scales the Stage86 V380 Arc-Reveal-Knowledge absorption from a 16-episode contract smoke into explicit 8-episode and 16-episode evidence packs.

## Purpose

Stage87 is not a final market release. It proves that the V1700 branchpoint-governed OS can carry the following controls across longer episode maps:

- Series arc planning
- Causal plot graph continuity
- Episode reveal budget constraints
- Character knowledge leakage prevention
- Node2 surface-only prose contracts
- Stage85 GitNexus/GraphNexus traceability

## Acceptance Criteria

- 8-episode evidence has at least 80 scene-level contracts.
- 16-episode evidence has at least 160 scene-level contracts.
- Four-act coverage is present: 기/승/전/결.
- Causal, foreshadow, callback, and emotional escalation edges remain connected.
- Reveal budget is exercised and direct premature reveal is blocked.
- Character knowledge constraints are exercised.
- Provider default calls remain 0.
- Node2 raw reveal access remains 0.
- Stage86 release gate remains pass.
- Stage87 release gate remains pass.

## Developer Commands

```bash
python -m pip install -e .
python tools/export_stage87_artifacts.py
python tools/run_stage87_release_gate.py
python tools/run_symbol_to_branchpoint_trace_gate.py
python tools/run_release_gate.py
python -m pytest -q tests
```

## Next Direction

Stage88 should add external human/editor/reader benchmark evidence over the Stage87 8-16 episode scale-up pack.
