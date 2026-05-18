# Stage108 — External Review & Editorial Board Mode

Stage108 connects Stage107.5 provider sandbox evidence and Stage107 longform production evidence to a deterministic editorial board.

## Invariants

- release gate live provider call count = 0
- raw manuscript provider leakage = 0
- credential leakage = 0
- raw provider response stored = false
- reviewer panel is fixture/local and deterministic

## Commands

```bash
python tools/run_stage108_0_editorial_preflight.py
python tools/run_stage108_1_editorial_board.py
python tools/run_stage108_2_editorial_consensus.py
python tools/run_stage108_release_gate.py
```
