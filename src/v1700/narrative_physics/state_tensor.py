from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class NarrativeStateVector:
    episode_id: str
    scene_id: str
    act: str
    character_state: float
    belief_state: float
    emotional_state: float
    causal_state: float
    reveal_state: float
    institutional_pressure: float
    relationship_pressure: float
    scene_energy: float
    audience_curiosity: float
    motif_residue: float
    style_surface: float
    branchpoint_risk: float

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__.copy()


@dataclass(frozen=True)
class NarrativeStateTensor:
    episode_count: int
    scene_count: int
    dimensions: tuple[str, ...]
    vectors: tuple[NarrativeStateVector, ...]

    @property
    def matrix_shape(self) -> tuple[int, int, int]:
        return (self.episode_count, self.scene_count, len(self.dimensions))

    def to_dict(self) -> dict[str, Any]:
        return {
            "episode_count": self.episode_count,
            "scene_count": self.scene_count,
            "dimensions": list(self.dimensions),
            "matrix_shape": list(self.matrix_shape),
            "vectors": [vector.to_dict() for vector in self.vectors],
        }


class NarrativeStateTensorBuilder:
    dimensions = (
        "character_state",
        "belief_state",
        "emotional_state",
        "causal_state",
        "reveal_state",
        "institutional_pressure",
        "relationship_pressure",
        "scene_energy",
        "audience_curiosity",
        "motif_residue",
        "style_surface",
        "branchpoint_risk",
    )

    def build(self, season_evidence: dict[str, Any]) -> NarrativeStateTensor:
        episodes = season_evidence.get("episodes", [])
        vectors: list[NarrativeStateVector] = []
        max_scene_count = 0
        for episode_index, episode in enumerate(episodes, start=1):
            scenes = episode.get("scenes", [])
            max_scene_count = max(max_scene_count, len(scenes))
            for scene in scenes:
                vectors.append(self._vector(episode_index, episode, scene))
        return NarrativeStateTensor(
            episode_count=len(episodes),
            scene_count=max_scene_count,
            dimensions=self.dimensions,
            vectors=tuple(vectors),
        )

    def _vector(self, episode_index: int, episode: dict[str, Any], scene: dict[str, Any]) -> NarrativeStateVector:
        tension = float(episode.get("tension_level", 0.0))
        scene_index = int(scene.get("scene_index", 1))
        quality = float(scene.get("quality_score", 0.0))
        blocked = float(episode.get("blocked_direct_reveal_count", 0))
        knowledge_constraints = float(episode.get("knowledge_constraint_count", 0))
        return NarrativeStateVector(
            episode_id=str(episode.get("episode_id", "")),
            scene_id=str(scene.get("scene_id", "")),
            act=str(episode.get("act", "")),
            character_state=round(min(1.0, 0.42 + episode_index * 0.025), 3),
            belief_state=round(min(1.0, 0.35 + knowledge_constraints * 0.015), 3),
            emotional_state=round(min(1.0, tension), 3),
            causal_state=round(min(1.0, float(episode.get("causal_input_count", 0)) * 0.25), 3),
            reveal_state=round(max(0.0, 1.0 - blocked * 0.08), 3),
            institutional_pressure=round(min(1.0, 0.30 + episode_index * 0.035), 3),
            relationship_pressure=round(min(1.0, 0.25 + (scene_index % 5) * 0.07), 3),
            scene_energy=round(min(1.0, quality / 10.0), 3),
            audience_curiosity=round(min(1.0, 0.45 + scene_index * 0.035), 3),
            motif_residue=round(min(1.0, 0.20 + float(episode.get("callback_edge_count", 0)) * 0.08), 3),
            style_surface=round(min(1.0, 0.70 + (quality - 8.0) * 0.08), 3),
            branchpoint_risk=round(max(0.0, 0.20 - (quality - 8.0) * 0.03), 3),
        )
