from __future__ import annotations

from v1700.nie.predictive.contracts import RepairOutcome

PNE_REPAIR_OUTCOMES: tuple[RepairOutcome, ...] = tuple(
    RepairOutcome(
        scene_id=f"s{i:02d}",
        recommendation_id=f"r{i:02d}",
        category=category,
        severity=severity,
        success=success,
        blast_ratio=blast,
    )
    for i, (category, severity, success, blast) in enumerate([
        ("unresolved_secret", 0.72, True, 0.25),
        ("unresolved_secret", 0.68, True, 0.30),
        ("unresolved_secret", 0.81, False, 0.35),
        ("unresolved_secret", 0.66, True, 0.20),
        ("unresolved_secret", 0.77, False, 0.32),
        ("broken_foreshadow", 0.70, True, 0.26),
        ("broken_foreshadow", 0.75, False, 0.41),
        ("broken_foreshadow", 0.60, True, 0.22),
        ("broken_foreshadow", 0.64, True, 0.18),
        ("broken_foreshadow", 0.83, False, 0.37),
        ("abandoned_thread", 0.48, True, 0.12),
        ("abandoned_thread", 0.50, True, 0.16),
        ("abandoned_thread", 0.58, False, 0.20),
        ("arc_not_tracked", 0.56, True, 0.10),
        ("arc_post_death", 0.80, False, 0.44),
        ("arc_contradiction", 0.86, False, 0.50),
        ("arc_inversion", 0.76, True, 0.28),
    ], start=1)
)

# TP=3, FP=1, FN=0, TN=2 -> precision 0.75, recall 1.0, F1 ~0.857143.
FEEDBACK_RECORDS: tuple[tuple[str, str, float, bool], ...] = (
    ("s101", "unresolved_secret", 0.78, True),
    ("s102", "broken_foreshadow", 0.71, True),
    ("s103", "arc_contradiction", 0.82, True),
    ("s104", "arc_post_death", 0.66, False),
    ("s105", "abandoned_thread", 0.32, False),
    ("s106", "arc_inversion", 0.28, False),
)
