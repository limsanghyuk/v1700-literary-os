# Stage131: GIG / Gate26 Advisory Absorption

Stage131 absorbs the deferred Gate26 problem from Stage130.

The key decision is that Gate26 remains advisory-only. It may classify a problem and route it to writer review, but it does not hard-block generation, rewrite canon, auto-repair manuscript state, or promote a shared source of truth.

## What Stage131 Adds

- Gate26 advisory contracts.
- Four deterministic contradiction-like categories.
- Writer review requirement for true contradiction.
- Mystery, misunderstanding, and reveal-delay exemptions.
- GitNexus/Python fallback preflight evidence.
- Stage131 release gate and repo doctor recognition.

## What Stage131 Blocks

- Gate26 hard block.
- Canon auto-resolution.
- AutoRepair mutation.
- Cross-project writes.
- Raw manuscript provider leakage.
- Node2 raw reveal access.
- Live provider calls in release gate.

## Verification

```bash
python tools/run_stage131_gig_advisory.py
python tools/run_stage131_release_gate.py
python tools/run_release_gate.py
python tools/run_stage72_repo_doctor.py
python -m pytest tests/test_stage131_gig_advisory.py -q
```
