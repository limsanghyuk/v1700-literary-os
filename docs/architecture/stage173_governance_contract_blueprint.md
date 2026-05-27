# Stage173 Blueprint — Governance Contract

## Components

```text
src/v1700/governance_contract/
src/v1700/stage173/
src/v1700/gates/stage173_release_gate.py
tools/run_stage173_governance_contract.py
tools/run_stage173_release_gate.py
tests/test_stage173_governance_contract.py
```

## Evidence pack

```text
release/current/stage173_governance_contract_pack/page06_readiness_matrix.json
release/current/stage173_governance_contract_pack/governance_contract_catalog.json
release/current/stage173_governance_contract_pack/policy_precedence_matrix.json
release/current/stage173_governance_contract_pack/authority_scope_registry.json
release/current/stage173_governance_contract_pack/approval_requirement_matrix.json
release/current/stage173_governance_contract_pack/stage174_entry_criteria.json
```

## Core rule

Unknown governance requests default to DENY. DENY overrides ALLOW at the same precedence. Sensitive authority requires approval evidence and remains non-executing in Stage173.
