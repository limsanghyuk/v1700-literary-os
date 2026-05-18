from dataclasses import dataclass, field

@dataclass(frozen=True)
class EmotionalDelta:
    from_state: str
    to_state: str

@dataclass(frozen=True)
class SceneIntentIR:
    scene_id: str
    scene_goal: str
    conflict: str
    emotional_delta: EmotionalDelta
    must_keep_facts: tuple[str, ...] = ()
    forbidden_reveals: tuple[str, ...] = ()
    timeline_position: str = "UNKNOWN"
    character_state_refs: tuple[str, ...] = ()
    dialogue_seed: str = ""
    setting_seed: str = ""

    @classmethod
    def from_dict(cls, data: dict) -> "SceneIntentIR":
        delta = data.get("emotional_delta", {})
        return cls(
            scene_id=data["scene_id"],
            scene_goal=data["scene_goal"],
            conflict=data.get("conflict", ""),
            emotional_delta=EmotionalDelta(delta.get("from") or delta.get("from_state", ""), delta.get("to") or delta.get("to_state", "")),
            must_keep_facts=tuple(data.get("must_keep_facts", [])),
            forbidden_reveals=tuple(data.get("forbidden_reveals", [])),
            timeline_position=data.get("timeline_position", "UNKNOWN"),
            character_state_refs=tuple(data.get("character_state_refs", [])),
            dialogue_seed=data.get("dialogue_seed", ""),
            setting_seed=data.get("setting_seed", ""),
        )

    def to_dict(self) -> dict:
        return {
            "scene_id": self.scene_id,
            "scene_goal": self.scene_goal,
            "conflict": self.conflict,
            "emotional_delta": {"from": self.emotional_delta.from_state, "to": self.emotional_delta.to_state},
            "must_keep_facts": list(self.must_keep_facts),
            "forbidden_reveals": list(self.forbidden_reveals),
            "timeline_position": self.timeline_position,
            "character_state_refs": list(self.character_state_refs),
            "dialogue_seed": self.dialogue_seed,
            "setting_seed": self.setting_seed,
        }
