# Stage97.1: Adversarial Longform Validation Hardening

Stage97.1 inserts a safety stage before Stage98. It does not generate a Studio workflow. It deliberately mutates Stage97 longform proof into broken structures and verifies that the correct gate blocks each failure.

## Scope

- Adversarial negative corpus.
- Broken topology, payoff, agency, scene, dialogue, voice, attention, security, and manifest cases.
- Stage96 coefficient memory bridge.
- Local-only manuscript ingest privacy skeleton.
- Structural-scene to production-scene mapping.
- Stage97.1 release gate.

## Guarantees

- Provider default calls remain `0`.
- Live provider calls during release remain `0`.
- Node2 raw reveal access remains `0`.
- Raw manuscript provider leakage remains `0`.
- Branchpoint lineage remains preserved.

## Commands

```bash
python tools/run_stage97_release_gate.py
python tools/run_stage97_1_adversarial_validation.py
python tools/run_stage97_1_release_gate.py
python tools/run_release_gate.py
python -m pytest -q tests/test_stage97_1_release_gate.py
```
