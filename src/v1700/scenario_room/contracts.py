from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Literal


@dataclass
class SceneBeat:
    beat_id: str
    scene_id: str
    beat_function: str
    visible_action: str
    conflict_vector: str
    emotional_pressure_delta: float
    reveal_state: Literal["NONE", "SETUP", "DELAY", "PAYOFF"]
    production_note: str
    microplot_id: str
    payoff_debt_id: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class InvestigationActionBeat:
    beat_id: str
    scene_id: str
    actor_id: str
    action_goal: str
    clue_or_obstacle: str
    agency_delta: float
    scene_necessity_anchor: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class DialogueSilenceCue:
    cue_id: str
    scene_id: str
    speaker_id: str
    speech_level: str
    silence_function: str
    subtext: str
    forbidden_reveal: list[str]
    node2_surface_only: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class PropRevealCue:
    cue_id: str
    prop_id: str
    first_appearance_scene: str
    reveal_budget_slot: str
    payoff_episode: str
    status: Literal["SETUP", "ACTIVE", "PAID", "BLOCKED"]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ScenarioRoomPlan:
    series_id: str
    episode_id: str
    mode: Literal["SCENARIO"]
    scene_beat_count: int
    action_movement_count: int
    dialogue_silence_cue_count: int
    prop_reveal_cue_count: int
    reveal_budget_safe: bool
    node2_raw_reveal_access: int
    provider_call_count: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

