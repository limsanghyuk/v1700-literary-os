# Stage113 — PhysicsRewardBridge + MAE Reward Wiring

Stage113 is the second step after Stage111 in the GitNexus-aware NIE roadmap. Stage112 established the preflight bridge. Stage113 wires a deterministic MAE reward contract into narrative physics without allowing live provider calls in release gates.

## Purpose

Convert cached or fixture MAE results into a release-safe physics reward signal.

```text
MAEResult(reader/writer/editor/cultural)
  ↓
PhysicsRewardBridge
  ↓
PhysicsRewardSignal(reward, advantage, EMA baseline)
  ↓
Bounded coefficient update proposals
```

## Reward formula

```text
R(scene) = 0.35·reader + 0.25·writer + 0.25·editor + 0.15·cultural
advantage = R(scene) - R_baseline
R_baseline ← 0.95·R_baseline + 0.05·R(scene)
```

## Release invariants

- `PhysicsRewardBridge` performs no LLM/provider call.
- Release gate uses fixture or cached `MAEResult` only.
- `provider_default_calls = 0`.
- `live_provider_call_count_in_release_gate = 0`.
- `Node2 raw reveal access = 0`.
- `raw manuscript provider leakage = 0`.
- Coefficient changes are proposals only and bounded by drift guard.

## Files

```text
src/v1700/nie/reward/contracts.py
src/v1700/nie/reward/mae_result_fixture.py
src/v1700/nie/reward/physics_reward_bridge.py
src/v1700/nie/reward/reward_signal_report.py
src/v1700/stage113/orchestrator.py
src/v1700/gates/stage113_release_gate.py
tools/run_stage113_physics_reward_bridge.py
tools/run_stage113_release_gate.py
```

## Next stage

Stage114 — AdaptiveMomentumWeights.
