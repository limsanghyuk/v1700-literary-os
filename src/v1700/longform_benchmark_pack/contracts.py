from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BenchmarkCaseDefinition:
    case_id: str
    scene_goal: str
    conflict: str
    dialogue_seed: str
    timeline_position: str
    setting_suffix: str
    emotional_from: str
    emotional_to: str

    def to_dict(self) -> dict[str, str]:
        return {
            "case_id": self.case_id,
            "scene_goal": self.scene_goal,
            "conflict": self.conflict,
            "dialogue_seed": self.dialogue_seed,
            "timeline_position": self.timeline_position,
            "setting_suffix": self.setting_suffix,
            "emotional_from": self.emotional_from,
            "emotional_to": self.emotional_to,
        }
