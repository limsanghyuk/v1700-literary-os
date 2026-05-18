# Stage97.2 - Unified Multi-Provider Runtime Governance Layer

Stage97.2 absorbs the applicable parts of the Claude/V411 multi-provider design into the V1700 lineage without replacing Stage96 provider ensemble arbitration.

## Purpose

Provider runtime calls are governed through typed contracts, deterministic routing, health monitoring, fixture-only release policy, cost evidence, and contract gates.

## Key modules

```text
src/v1700/provider_runtime/
  context.py
  response.py
  interface.py
  openai_compatible_adapter.py
  ollama_adapter.py
  task_router.py
  health_monitor.py
  unified_gateway.py
  cost_ledger.py
  release_policy.py
  contract_gate.py
```

## Invariants

```text
provider default calls = 0
live provider call count in release gate = 0
release mode provider = fixture/mock only
TaskRouter route() provider calls = 0
provider health live checks in release gate = 0
Node2 raw reveal access = 0
raw manuscript provider leakage = 0
branchpoint lineage preserved
```

## Evidence

```text
release/current/stage97_2_provider_runtime_report.json
release/current/stage97_2_release_gate_report.json
release/current/stage97_2_provider_runtime_pack/
```
