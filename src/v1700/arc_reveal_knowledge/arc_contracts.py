from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ArcAct(str, Enum):
    GI = "gi"
    SEUNG = "seung"
    JEON = "jeon"
    GYEOL = "gyeol"


class ArcPlotEdgeType(str, Enum):
    CAUSAL = "causal"
    FORESHADOW = "foreshadow"
    CALLBACK = "callback"
    EMOTIONAL_ESCALATION = "emotional_escalation"


@dataclass(frozen=True)
class ArcPlotNode:
    episode_id: str
    episode_index: int
    act: ArcAct
    tension_level: float
    emotional_target: str
    causal_inputs: tuple[str, ...] = ()
    forbidden_reveals: tuple[str, ...] = ()
    required_callbacks: tuple[str, ...] = ()

    def to_dict(self) -> dict:
        return {
            "episode_id": self.episode_id,
            "episode_index": self.episode_index,
            "act": self.act.value,
            "tension_level": self.tension_level,
            "emotional_target": self.emotional_target,
            "causal_inputs": list(self.causal_inputs),
            "forbidden_reveals": list(self.forbidden_reveals),
            "required_callbacks": list(self.required_callbacks),
        }


@dataclass(frozen=True)
class ArcPlotEdge:
    source_episode_id: str
    target_episode_id: str
    edge_type: ArcPlotEdgeType
    reason: str

    def to_dict(self) -> dict:
        return {
            "source_episode_id": self.source_episode_id,
            "target_episode_id": self.target_episode_id,
            "edge_type": self.edge_type.value,
            "reason": self.reason,
        }
