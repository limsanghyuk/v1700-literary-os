from __future__ import annotations

from dataclasses import dataclass, field

from v1700.ir.rendered_prose import RenderedProseIR
from v1700.ir.scene_intent import SceneIntentIR


@dataclass(frozen=True)
class SequencePlan:
    sequence_id: str
    objective: str
    conflict: str
    emotional_shift: str
    reveal_boundary: str

    def to_dict(self) -> dict:
        return self.__dict__.copy()


@dataclass(frozen=True)
class EpisodePlan:
    episode_id: str
    title: str
    major_turn: str
    sequences: tuple[SequencePlan, ...]

    def to_dict(self) -> dict:
        return {
            "episode_id": self.episode_id,
            "title": self.title,
            "major_turn": self.major_turn,
            "sequences": [sequence.to_dict() for sequence in self.sequences],
        }


@dataclass(frozen=True)
class LongformPlan:
    prompt: str
    season_arc: str
    trilogy_proof: tuple[str, str, str]
    episodes: tuple[EpisodePlan, ...]

    def to_dict(self) -> dict:
        return {
            "prompt": self.prompt,
            "season_arc": self.season_arc,
            "trilogy_proof": list(self.trilogy_proof),
            "episodes": [episode.to_dict() for episode in self.episodes],
        }


@dataclass(frozen=True)
class LongformExecutionReport:
    status: str
    plan: LongformPlan
    scenes: tuple[SceneIntentIR, ...]
    rendered: tuple[RenderedProseIR, ...]
    drse: dict
    emotional_momentum: dict
    mise_en_scene: dict
    ledger: dict
    reveal_budget: dict
    refinement: dict
    issues: tuple[str, ...] = ()
    provider_default_calls: int = 0
    node2_raw_reveal_access_count: int = 0

    def to_dict(self) -> dict:
        return {
            "status": self.status,
            "plan": self.plan.to_dict(),
            "scenes": [scene.to_dict() for scene in self.scenes],
            "rendered": [item.to_dict() for item in self.rendered],
            "drse": self.drse,
            "emotional_momentum": self.emotional_momentum,
            "mise_en_scene": self.mise_en_scene,
            "ledger": self.ledger,
            "reveal_budget": self.reveal_budget,
            "refinement": self.refinement,
            "issues": list(self.issues),
            "provider_default_calls": self.provider_default_calls,
            "node2_raw_reveal_access_count": self.node2_raw_reveal_access_count,
        }
