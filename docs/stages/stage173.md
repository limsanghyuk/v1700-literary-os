# Stage173 — Governance Contract

Stage173 opens Page06 Governance Body by defining deterministic governance contracts over sealed Page05 evidence.

It records policy shape, default-deny authority, precedence, approval requirements, and Stage174 readiness. It does not execute release promotion, project propagation, generation, writes, training, mutation, or repair.

## Validation

```bash
python tools/run_stage173_governance_contract.py
python tools/run_stage173_release_gate.py
python -m pytest tests/test_stage173_governance_contract.py -q
```
