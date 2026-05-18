from v1700.ir.scene_intent import SceneIntentIR
from .marker_stripper import InternalMarkerStripper

class Node2ConstraintValidator:
    def __init__(self):
        self.marker = InternalMarkerStripper()

    def validate(self, scene: SceneIntentIR, text: str) -> tuple[dict[str, float], tuple[str, ...]]:
        risks: list[str] = []
        if self.marker.leakage(text):
            risks.append("internal_marker_leakage")
        for reveal in scene.forbidden_reveals:
            if reveal and reveal in text:
                risks.append(f"reveal_leakage:{reveal}")
        missing_facts = [fact for fact in scene.must_keep_facts if fact and fact not in text]
        if missing_facts:
            risks.append("missing_must_keep_fact")
        scores = {
            "fact_preservation": 10.0 if not missing_facts else 8.5,
            "reveal_preservation": 10.0 if not any(r.startswith("reveal_leakage") for r in risks) else 0.0,
            "scene_goal_preservation": 9.8 if scene.scene_goal.split()[0] in text or scene.scene_goal in text else 9.5,
        }
        return scores, tuple(risks)
