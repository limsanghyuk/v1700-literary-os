from v1700.ir.rendered_prose import RenderedProseIR

class Node3CriticGate:
    SURFACE_MIN = {
        "anti_llm": 8.0,
        "emotion_accessibility": 8.0,
        "naturalness": 8.0,
        "rhythm": 7.8,
        "dialogue_taste": 7.8,
        "sensory_afterimage": 7.5,
    }
    CONSTRAINT_MIN = {
        "fact_preservation": 9.8,
        "reveal_preservation": 10.0,
        "scene_goal_preservation": 9.5,
    }

    def validate(self, rendered: RenderedProseIR) -> tuple[bool, list[str]]:
        issues = list(rendered.risk_flags)
        for key, minimum in self.SURFACE_MIN.items():
            if rendered.surface_score.get(key, 0) < minimum:
                issues.append(f"surface_below_threshold:{key}")
        for key, minimum in self.CONSTRAINT_MIN.items():
            if rendered.constraint_score.get(key, 0) < minimum:
                issues.append(f"constraint_below_threshold:{key}")
        return (not issues), issues
