# Stage132: Contradiction Classifier + Mystery Exemption

Stage132 deepens Stage131's Gate26 advisory layer.

It does not repair canon. It classifies conflicts with evidence and preserves writer authority.

## What Stage132 Adds

- Deterministic contradiction evidence contract.
- True contradiction classification.
- Intentional mystery exemption requiring reveal lock and payoff budget.
- POV misunderstanding exemption.
- Reveal-delay exemption.
- No-conflict pass-through case.
- Stage132 release gate and repo doctor recognition.

## What Stage132 Blocks

- Gate26 hard block.
- Canon auto-resolution.
- AutoRepair mutation.
- Cross-project writes.
- Raw manuscript provider leakage.
- Node2 raw reveal access.
- Live provider calls in release gate.

## Verification

```bash
python tools/run_stage132_contradiction_classifier.py
python tools/run_stage132_release_gate.py
python tools/run_release_gate.py
python tools/run_stage72_repo_doctor.py
python -m pytest tests/test_stage132_contradiction_classifier.py -q
```
