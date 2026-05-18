# DRSE Formula

DRSE means Dynamic Relational Scoring Engine.

Formula:

```text
DRSE(node, scene) =
  scene_goal_similarity * W_scene
+ causality_marker * W_causality
+ emotion_marker * W_emotion
+ residue_marker * W_residue
+ legacy_marker * W_legacy
+ motif_marker * W_motif
+ base_weight
```

Default weights:

```text
W_causality = 1.50
W_emotion   = 1.20
W_residue   = 2.00
W_legacy    = 1.10
W_motif     = 0.90
```

DRSE output is never passed to Node2 as raw graph state. It is projected into surface-safe directives.
