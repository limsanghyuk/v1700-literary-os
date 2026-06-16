# Script Feature Record Contract

## Purpose

Standardize learning-ready scene feature records derived from scripts.

## Required Signal Keys

```text
conflict_intensity
scene_energy_ratio
motif_residue_score
curiosity_gradient
dialogue_ratio
```

## Required Record Shape

```json
{
  "work_id": "string",
  "feature_scene_count": 0,
  "mean_conflict_intensity": 0.0,
  "mean_scene_energy_ratio": 0.0,
  "mean_motif_residue_score": 0.0,
  "mean_curiosity_gradient": 0.0,
  "mean_dialogue_ratio": 0.0,
  "signal_keys": [
    "conflict_intensity",
    "scene_energy_ratio",
    "motif_residue_score",
    "curiosity_gradient",
    "dialogue_ratio"
  ],
  "learning_ready": true
}
```

## Mapping Direction

- Feature records feed V1700 learning candidates.
- They do not replace writer authority.
- They can be mapped into Formula Signal, EAT8D, and Narrative State Tensor layers later.
