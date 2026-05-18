# Stage95 Developer Handoff

Stage95 introduces the V1700 Native Narrative Physics Engine.

## Runtime Boundary

- Provider ensemble arbitration moves to Stage96.
- Release verification performs zero live provider calls.
- Node2 receives surface-safe transform evidence only.
- Branchpoint survival remains the release authority.

## Evidence

- Tensor shape: `[16, 10, 12]`
- Reveal entropy status: `pass`
- Scene energy status: `pass`
- Branchpoint survival status: `pass`

## Commands

```bash
python tools/run_stage95_narrative_physics_smoke.py
python tools/run_stage95_release_gate.py
python tools/run_release_gate.py
```
