from __future__ import annotations
from dataclasses import asdict, dataclass, field
from typing import Literal

@dataclass(frozen=True)
class SeasonArc:
    season_id: str
    season_index: int
    episode_count: int
    dramatic_function: str
    central_question: str
    payoff_targets: tuple[str, ...]
    branchpoint_refs: tuple[str, ...]
    def to_dict(self) -> dict:
        return asdict(self)

@dataclass(frozen=True)
class ProductionEpisode:
    episode_id: str
    season_id: str
    episode_index: int
    target_scene_count: int
    production_window: str
    narrative_function: str
    attention_budget: float
    payoff_due_count: int
    def to_dict(self) -> dict:
        return asdict(self)

@dataclass(frozen=True)
class CharacterMemoryPoint:
    character_id: str
    episode_id: str
    knowledge_state: str
    agency_delta: float
    relationship_delta: str
    memory_commit: str
    def to_dict(self) -> dict:
        return asdict(self)

@dataclass(frozen=True)
class PayoffCalendarItem:
    payoff_id: str
    planted_episode: str
    due_episode: str
    status: Literal['PLANTED','DUE','PAID','WATCH']
    severity: Literal['INFO','WARN','BLOCK']
    def to_dict(self) -> dict:
        return asdict(self)

@dataclass(frozen=True)
class AttentionHeatPoint:
    episode_id: str
    curiosity_score: float
    fatigue_score: float
    recommended_action: str
    def to_dict(self) -> dict:
        return asdict(self)

@dataclass(frozen=True)
class ProductionSceneMap:
    episode_id: str
    structural_scene_count: int
    production_scene_count: int
    mapping_policy: str
    raw_manuscript_required: bool = False
    def to_dict(self) -> dict:
        return asdict(self)

@dataclass(frozen=True)
class LongformProductionSuiteReport:
    status: str
    stage: str
    baseline_stage: str
    seasons: tuple[SeasonArc, ...] = field(default_factory=tuple)
    episodes: tuple[ProductionEpisode, ...] = field(default_factory=tuple)
    payoff_calendar: tuple[PayoffCalendarItem, ...] = field(default_factory=tuple)
    character_memory: tuple[CharacterMemoryPoint, ...] = field(default_factory=tuple)
    attention_heatmap: tuple[AttentionHeatPoint, ...] = field(default_factory=tuple)
    production_scene_maps: tuple[ProductionSceneMap, ...] = field(default_factory=tuple)
    provider_default_calls: int = 0
    live_provider_call_count_in_release_gate: int = 0
    raw_manuscript_provider_leakage: int = 0
    node2_raw_reveal_access: int = 0
    credential_leakage: int = 0
    full_text_export_default: bool = False
    issues: tuple[str, ...] = field(default_factory=tuple)
    def to_dict(self) -> dict:
        payload = asdict(self)
        for key in ('seasons','episodes','payoff_calendar','character_memory','attention_heatmap','production_scene_maps'):
            payload[key] = [item for item in payload[key]]
        return payload
