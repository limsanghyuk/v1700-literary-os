# Stage114 — AdaptiveMomentumWeights

Stage114 converts the hard-coded emotional momentum mixing ratios into bounded, auditable alpha parameters.

## Purpose

Previous emotional momentum logic used fixed ratios such as process/target signal plus keyword observation signal. Stage114 introduces an AdaptiveMomentumWeights layer so each emotional dimension can calibrate its alpha with cached MAE dimension scores while preserving deterministic release behavior.

## Contract

```text
alpha ∈ [0.30, 0.80]
delta_dim = alpha_dim * process_signal + (1-alpha_dim) * observation_signal
loss = (delta_dim - mae_dim_score)^2
gradient = 2 * (delta_dim - mae_dim_score) * (process_signal - observation_signal)
```

## Release guards

- no live provider call in release gate
- no LLM call inside PhysicsRewardBridge or AMW
- max single alpha shift ≤ 0.03
- max run total alpha shift ≤ 0.10
- surface safety tolerance cannot loosen
- branchpoint sensitivity cannot decrease
- provider-zero policy cannot change

## Evidence

- `release/current/stage114_adaptive_momentum_weights_report.json`
- `release/current/stage114_release_gate_report.json`

## Next

Stage115 — CharacterInfluenceMatrix + Structural Balance.
