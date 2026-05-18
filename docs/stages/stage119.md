# Stage119 — NIE Adversarial Regression Pack

Stage119 hardens Stage118 NIL Orchestrator by adding a deterministic negative
corpus for Narrative Intelligence Engine failure modes. The stage proves that
broken MAE reward contracts, PhysicsRewardBridge boundary violations, AMW drift,
CIM asymmetry failures, structural-balance omissions, domain RAG policy breaks,
missing tension loss, and missing NIL evidence are blocked by release checks.

## Invariants

- Release gate live provider calls remain 0.
- PhysicsRewardBridge never calls an LLM.
- QueryIntentClassifier never calls an LLM.
- Node2 raw reveal access remains 0.
- Raw manuscript provider leakage remains 0.
- Every BLOCK case has expected block reason, triggered gate, and evidence.
- FILELIST.txt and SHA256SUMS.txt are included inside the ZIP package.

## Output

- `release/current/stage119_nie_adversarial_regression_report.json`
- `release/current/stage119_release_gate_report.json`
- `release/current/stage119_nie_adversarial_pack/`
