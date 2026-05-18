from __future__ import annotations

from dataclasses import dataclass
from statistics import mean
from typing import Any


@dataclass(frozen=True)
class ScaleupSceneEvidence:
    episode_id: str
    scene_id: str
    sequence_index: int
    scene_index: int
    act: str
    causal_anchor: str
    reveal_policy: str
    knowledge_mode: str
    surface_only: bool
    quality_score: float
    afterimage_marker: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "episode_id": self.episode_id,
            "scene_id": self.scene_id,
            "sequence_index": self.sequence_index,
            "scene_index": self.scene_index,
            "act": self.act,
            "causal_anchor": self.causal_anchor,
            "reveal_policy": self.reveal_policy,
            "knowledge_mode": self.knowledge_mode,
            "surface_only": self.surface_only,
            "quality_score": self.quality_score,
            "afterimage_marker": self.afterimage_marker,
        }


@dataclass(frozen=True)
class ScaleupEpisodeEvidence:
    episode_id: str
    act: str
    tension_level: float
    emotional_target: str
    scene_count: int
    causal_input_count: int
    foreshadow_edge_count: int
    callback_edge_count: int
    emotional_escalation_edge_count: int
    reveal_policy_count: int
    blocked_direct_reveal_count: int
    knowledge_constraint_count: int
    average_quality_score: float
    scenes: tuple[ScaleupSceneEvidence, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "episode_id": self.episode_id,
            "act": self.act,
            "tension_level": self.tension_level,
            "emotional_target": self.emotional_target,
            "scene_count": self.scene_count,
            "causal_input_count": self.causal_input_count,
            "foreshadow_edge_count": self.foreshadow_edge_count,
            "callback_edge_count": self.callback_edge_count,
            "emotional_escalation_edge_count": self.emotional_escalation_edge_count,
            "reveal_policy_count": self.reveal_policy_count,
            "blocked_direct_reveal_count": self.blocked_direct_reveal_count,
            "knowledge_constraint_count": self.knowledge_constraint_count,
            "average_quality_score": self.average_quality_score,
            "scenes": [scene.to_dict() for scene in self.scenes],
        }


@dataclass(frozen=True)
class ScaleupSeasonEvidence:
    episode_count: int
    scenes_per_episode: int
    status: str
    issues: tuple[str, ...]
    total_scene_count: int
    act_coverage: tuple[str, ...]
    edge_counts: dict[str, int]
    blocked_direct_reveal_count: int
    knowledge_constraint_count: int
    average_quality_score: float
    min_quality_score: float
    provider_default_calls: int
    node2_raw_reveal_access_count: int
    episodes: tuple[ScaleupEpisodeEvidence, ...]

    @property
    def full_episode_scaleup_ready(self) -> bool:
        return self.status == "pass" and self.episode_count >= 8 and self.total_scene_count >= 80

    def to_dict(self) -> dict[str, Any]:
        return {
            "episode_count": self.episode_count,
            "scenes_per_episode": self.scenes_per_episode,
            "status": self.status,
            "issues": list(self.issues),
            "total_scene_count": self.total_scene_count,
            "act_coverage": list(self.act_coverage),
            "edge_counts": dict(self.edge_counts),
            "blocked_direct_reveal_count": self.blocked_direct_reveal_count,
            "knowledge_constraint_count": self.knowledge_constraint_count,
            "average_quality_score": self.average_quality_score,
            "min_quality_score": self.min_quality_score,
            "provider_default_calls": self.provider_default_calls,
            "node2_raw_reveal_access_count": self.node2_raw_reveal_access_count,
            "full_episode_scaleup_ready": self.full_episode_scaleup_ready,
            "episodes": [episode.to_dict() for episode in self.episodes],
        }


def score_average(items: tuple[ScaleupSceneEvidence, ...]) -> float:
    return round(mean(scene.quality_score for scene in items), 2) if items else 0.0
