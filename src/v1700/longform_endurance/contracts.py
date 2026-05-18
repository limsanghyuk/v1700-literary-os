from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class EnduranceEpisode:
    episode_id: str
    act: str
    position: int
    microplot_count: int
    scene_count: int
    reveal_load: float
    emotional_load: float
    conflict_load: float
    relationship_load: float
    motif_load: float
    exposition_load: float
    agency_load: float
    attention_load: float

    @property
    def total_load(self) -> float:
        return round(
            self.reveal_load
            + self.emotional_load
            + self.conflict_load
            + self.relationship_load
            + self.motif_load
            + self.exposition_load
            + self.agency_load
            + self.attention_load,
            3,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "episode_id": self.episode_id,
            "act": self.act,
            "position": self.position,
            "microplot_count": self.microplot_count,
            "scene_count": self.scene_count,
            "reveal_load": self.reveal_load,
            "emotional_load": self.emotional_load,
            "conflict_load": self.conflict_load,
            "relationship_load": self.relationship_load,
            "motif_load": self.motif_load,
            "exposition_load": self.exposition_load,
            "agency_load": self.agency_load,
            "attention_load": self.attention_load,
            "total_load": self.total_load,
        }


@dataclass(frozen=True)
class FractalPlotUnit:
    unit_id: str
    unit_type: str
    setup: bool
    pressure: bool
    collision: bool
    reversal: bool
    residue: bool
    parent_unit_id: str
    child_unit_ids: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "unit_id": self.unit_id,
            "unit_type": self.unit_type,
            "setup": self.setup,
            "pressure": self.pressure,
            "collision": self.collision,
            "reversal": self.reversal,
            "residue": self.residue,
            "parent_unit_id": self.parent_unit_id,
            "child_unit_ids": list(self.child_unit_ids),
        }
