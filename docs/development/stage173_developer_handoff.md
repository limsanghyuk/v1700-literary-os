# Stage173 Developer Handoff

## Baseline

Stage172.3 Page05 Release Seal.

## Start

```bash
python tools/run_mandatory_predevelopment_check.py
python tools/run_stage172_release_gate.py
```

## Implement

```bash
python tools/run_stage173_governance_contract.py
python tools/run_stage173_release_gate.py
python -m pytest tests/test_stage173_governance_contract.py -q
```

## Completion target

```text
stage173 Governance Contract pass
stage174_release_policy_registry_ready = true
```
