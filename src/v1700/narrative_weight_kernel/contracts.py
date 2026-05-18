from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

BoardPieceRole = Literal["king", "queen", "rook", "bishop", "knight", "pawn", "shadow"]
RelationKind = Literal[
    "ally",
    "rival",
    "mentor",
    "antagonist",
    "family",
    "lover",
    "debt",
    "secret_keeper",
    "witness",
]
FeedbackMetric = Literal[
    "agency",
    "desire_pressure",
    "wound_pressure",
    "relation_tension",
    "event_causality",
    "knowledge_asymmetry",
    "reveal_pressure",
    "emotional_momentum",
    "scene_energy",
    "motif_residue",
    "reader_attention",
    "style_boundary",
    "safety_boundary",
]


@dataclass(frozen=True)
class NarrativeWeightVector:
    """Explainable narrative weights used by the symbolic Literary OS layer.

    This is deliberately not a neural-network parameter tensor.  It is an auditable
    coefficient vector that lets gates, reports, and deterministic tests explain
    why one character, event, or relation receives more narrative pressure than
    another.
    """

    agency: float = 1.0
    desire_pressure: float = 1.0
    wound_pressure: float = 1.0
    relation_tension: float = 1.0
    event_causality: float = 1.0
    knowledge_asymmetry: float = 1.0
    reveal_pressure: float = 1.0
    emotional_momentum: float = 1.0
    scene_energy: float = 1.0
    motif_residue: float = 1.0
    reader_attention: float = 1.0
    style_boundary: float = 1.0
    safety_boundary: float = 1.25

    def to_dict(self) -> dict[str, float]:
        return {key: float(value) for key, value in self.__dict__.items()}

    @classmethod
    def from_mapping(cls, values: dict[str, Any]) -> "NarrativeWeightVector":
        allowed = cls().__dict__.keys()
        return cls(**{key: float(value) for key, value in values.items() if key in allowed})

    def bounded_update(self, deltas: dict[str, float], *, max_delta: float = 0.08) -> "NarrativeWeightVector":
        values = self.to_dict()
        for key, delta in deltas.items():
            if key not in values:
                continue
            clipped = max(-max_delta, min(max_delta, float(delta)))
            values[key] = round(max(0.05, min(3.0, values[key] + clipped)), 4)
        return NarrativeWeightVector.from_mapping(values)


@dataclass(frozen=True)
class CharacterSeed:
    character_id: str
    display_name: str
    board_piece: BoardPieceRole
    dramatic_role: str
    desire: str
    wound: str
    secret: str = ""
    relation_to_protagonist: str = ""
    agency_bias: float = 0.5
    knowledge_access: float = 0.5
    motif_refs: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "character_id": self.character_id,
            "display_name": self.display_name,
            "board_piece": self.board_piece,
            "dramatic_role": self.dramatic_role,
            "desire": self.desire,
            "wound": self.wound,
            "secret": self.secret,
            "relation_to_protagonist": self.relation_to_protagonist,
            "agency_bias": self.agency_bias,
            "knowledge_access": self.knowledge_access,
            "motif_refs": list(self.motif_refs),
        }


@dataclass(frozen=True)
class EventSeed:
    event_id: str
    summary: str
    episode_index: int
    function: str
    involved_characters: tuple[str, ...]
    causal_importance: float = 0.5
    reveal_refs: tuple[str, ...] = ()
    pressure: float = 0.5

    def to_dict(self) -> dict[str, Any]:
        return {
            "event_id": self.event_id,
            "summary": self.summary,
            "episode_index": self.episode_index,
            "function": self.function,
            "involved_characters": list(self.involved_characters),
            "causal_importance": self.causal_importance,
            "reveal_refs": list(self.reveal_refs),
            "pressure": self.pressure,
        }


@dataclass(frozen=True)
class CharacterProfileScore:
    character_id: str
    board_piece: BoardPieceRole
    axis_scores: dict[str, float]
    weighted_score: float
    explanation: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "character_id": self.character_id,
            "board_piece": self.board_piece,
            "axis_scores": dict(self.axis_scores),
            "weighted_score": self.weighted_score,
            "explanation": list(self.explanation),
        }


@dataclass(frozen=True)
class CharacterEventRelationScore:
    character_id: str
    event_id: str
    relation_kind: RelationKind
    axis_scores: dict[str, float]
    weighted_score: float
    learning_tags: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "character_id": self.character_id,
            "event_id": self.event_id,
            "relation_kind": self.relation_kind,
            "axis_scores": dict(self.axis_scores),
            "weighted_score": self.weighted_score,
            "learning_tags": list(self.learning_tags),
        }


@dataclass(frozen=True)
class FeedbackSignal:
    metric: FeedbackMetric
    observed: float
    target: float
    confidence: float = 1.0
    source: str = "manual"

    def error(self) -> float:
        return float(self.target) - float(self.observed)

    def to_dict(self) -> dict[str, Any]:
        return {
            "metric": self.metric,
            "observed": self.observed,
            "target": self.target,
            "confidence": self.confidence,
            "source": self.source,
            "error": round(self.error(), 4),
        }


@dataclass(frozen=True)
class KernelLearningReport:
    status: Literal["pass", "blocked"]
    baseline_weights: NarrativeWeightVector
    learned_weights: NarrativeWeightVector
    feedback_signals: tuple[FeedbackSignal, ...]
    update_log: tuple[dict[str, Any], ...]
    drift_guard: dict[str, Any]
    issues: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "baseline_weights": self.baseline_weights.to_dict(),
            "learned_weights": self.learned_weights.to_dict(),
            "feedback_signals": [signal.to_dict() for signal in self.feedback_signals],
            "update_log": list(self.update_log),
            "drift_guard": self.drift_guard,
            "issues": list(self.issues),
        }


@dataclass(frozen=True)
class WeightKernelReport:
    stage: str
    status: Literal["pass", "blocked"]
    character_scores: tuple[CharacterProfileScore, ...]
    relation_scores: tuple[CharacterEventRelationScore, ...]
    learning_report: KernelLearningReport
    invariants: dict[str, Any] = field(default_factory=dict)
    issues: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "stage": self.stage,
            "status": self.status,
            "character_scores": [score.to_dict() for score in self.character_scores],
            "relation_scores": [score.to_dict() for score in self.relation_scores],
            "learning_report": self.learning_report.to_dict(),
            "invariants": dict(self.invariants),
            "issues": list(self.issues),
        }
