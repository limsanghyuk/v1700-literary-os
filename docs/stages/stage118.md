# Stage118 — NIL Orchestrator

Stage118 composes the Stage113~Stage117 Narrative Intelligence Engine components into one deterministic Narrative Intelligence Loop evidence layer.

## Purpose

Stage118 proves that the NIE spine is connected end-to-end before adversarial regression hardening:

```text
CharacterInfluenceMatrix
→ StructuralBalance
→ AdaptiveMomentumWeights
→ MAERewardSignal
→ PhysicsRewardBridge
→ CoefficientUpdateProposal
→ DomainSpecificRAGFusion
→ NarrativeTensionCurve
```

The stage is deterministic. It consumes cached/fixture component reports and performs no live provider calls, no raw manuscript export, and no Node2 raw reveal access.

## Added components

- `src/v1700/nie/nil/contracts.py`
- `src/v1700/nie/nil/nil_orchestrator.py`
- `src/v1700/nie/nil/nil_report.py`
- `src/v1700/stage118/orchestrator.py`
- `src/v1700/gates/stage118_release_gate.py`

## Invariants

- provider default calls = 0
- live provider call count in release gate = 0
- PhysicsRewardBridge LLM call = 0
- MAE live provider call = 0
- QueryIntentClassifier LLM call = 0
- Node2 raw reveal access = 0
- raw manuscript provider leakage = 0
- credential leakage = 0
- branchpoint lineage preserved
