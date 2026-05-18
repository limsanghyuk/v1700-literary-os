from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class SceneFeature:
    scene_id: str
    episode_id: str
    word_count: int
    character_count: int
    active_characters: tuple[str, ...]
    goal_conflict_count: int
    belief_state_change_count: int
    reveal_event_count: int
    foreshadow_event_count: int
    emotional_delta: float
    scene_energy_input: float
    scene_energy_output: float
    motif_count: int
    callback_count: int
    curiosity_hook_count: int
    surface_safety_flags: tuple[str, ...]
    branchpoint_touchpoints: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "scene_id": self.scene_id,
            "episode_id": self.episode_id,
            "word_count": self.word_count,
            "character_count": self.character_count,
            "active_characters": list(self.active_characters),
            "goal_conflict_count": self.goal_conflict_count,
            "belief_state_change_count": self.belief_state_change_count,
            "reveal_event_count": self.reveal_event_count,
            "foreshadow_event_count": self.foreshadow_event_count,
            "emotional_delta": self.emotional_delta,
            "scene_energy_input": self.scene_energy_input,
            "scene_energy_output": self.scene_energy_output,
            "motif_count": self.motif_count,
            "callback_count": self.callback_count,
            "curiosity_hook_count": self.curiosity_hook_count,
            "surface_safety_flags": list(self.surface_safety_flags),
            "branchpoint_touchpoints": list(self.branchpoint_touchpoints),
        }
