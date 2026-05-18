from __future__ import annotations

from dataclasses import dataclass, field
import math
import re
from statistics import mean


_TOKEN_RE = re.compile(r"[A-Za-z0-9가-힣_]+")


def _tokens(text: str) -> set[str]:
    return {token.lower() for token in _TOKEN_RE.findall(text or "") if token.strip()}


def _jaccard(a: str, b: str) -> float:
    left = _tokens(a)
    right = _tokens(b)
    if not left or not right:
        return 0.0
    return len(left & right) / len(left | right)


@dataclass(frozen=True)
class DRSEWeights:
    """Dynamic Relational Scoring Engine weights.

    The formula keeps the developer's original principle: relation importance is
    computed outside the LLM by Python, then only the strongest safe directives
    are projected to the renderer.
    """

    causality: float = 1.50
    emotion: float = 1.20
    residue: float = 2.00
    legacy: float = 1.10
    motif: float = 0.90
    scene_goal: float = 1.00


@dataclass(frozen=True)
class DRSEInputNode:
    node_id: str
    node_type: str
    content: str
    relations: tuple[str, ...] = ()
    tags: tuple[str, ...] = ()
    base_weight: float = 1.0

    def searchable_text(self) -> str:
        return " ".join((self.node_id, self.node_type, self.content, " ".join(self.relations), " ".join(self.tags)))


@dataclass(frozen=True)
class DRSENodeScore:
    node_id: str
    node_type: str
    final_score: float
    components: dict[str, float] = field(default_factory=dict)
    safe_directive: str = ""

    def to_dict(self) -> dict:
        return {
            "node_id": self.node_id,
            "node_type": self.node_type,
            "final_score": round(self.final_score, 4),
            "components": {key: round(value, 4) for key, value in self.components.items()},
            "safe_directive": self.safe_directive,
        }


@dataclass(frozen=True)
class DRSEContext:
    scene_goal: str
    scores: tuple[DRSENodeScore, ...]
    dominant_pattern: str
    average_score: float
    provider_default_calls: int = 0

    def top_scores(self, limit: int = 3) -> tuple[DRSENodeScore, ...]:
        return self.scores[:limit]

    def to_surface_directives(self, limit: int = 3) -> tuple[str, ...]:
        return tuple(score.safe_directive for score in self.top_scores(limit) if score.safe_directive)

    def to_dict(self) -> dict:
        return {
            "scene_goal": self.scene_goal,
            "dominant_pattern": self.dominant_pattern,
            "average_score": round(self.average_score, 4),
            "scores": [score.to_dict() for score in self.scores],
            "surface_directives": list(self.to_surface_directives()),
            "provider_default_calls": self.provider_default_calls,
        }


class DRSEEngine:
    """Deterministic literary relation scorer.

    DRSE restores the older mathematical intent of the project:
    Causality, emotion, residue, legacy and motif pressure are scored by Python,
    not guessed by a provider model.
    """

    def __init__(self, weights: DRSEWeights | None = None) -> None:
        self.weights = weights or DRSEWeights()

    def score(self, scene_goal: str, nodes: tuple[DRSEInputNode, ...] | list[DRSEInputNode]) -> DRSEContext:
        scored = tuple(sorted((self._score_node(scene_goal, node) for node in nodes), key=lambda item: item.final_score, reverse=True))
        dominant = scored[0].node_type if scored else "NONE"
        avg = mean(score.final_score for score in scored) if scored else 0.0
        return DRSEContext(scene_goal=scene_goal, scores=scored, dominant_pattern=dominant, average_score=avg)

    def _score_node(self, scene_goal: str, node: DRSEInputNode) -> DRSENodeScore:
        text = node.searchable_text()
        relevance = _jaccard(scene_goal, text)
        relation_text = " ".join((*node.relations, *node.tags, node.node_type)).lower()
        causality = self._marker(relation_text, ("causal", "cause", "effect", "인과", "사건", "결과")) * self.weights.causality
        emotion = self._marker(relation_text, ("emotion", "feeling", "감정", "관계", "tension", "sympathy", "dread")) * self.weights.emotion
        residue = self._marker(relation_text, ("residue", "foreshadow", "reveal", "복선", "잔향", "비밀")) * self.weights.residue
        legacy = self._marker(relation_text, ("legacy", "stage", "law", "world", "유산", "설정", "법칙")) * self.weights.legacy
        motif = self._marker(relation_text, ("motif", "object", "image", "미장센", "감각", "상징")) * self.weights.motif
        components = {
            "scene_goal_similarity": relevance * self.weights.scene_goal,
            "causality": causality,
            "emotion": emotion,
            "residue": residue,
            "legacy": legacy,
            "motif": motif,
            "base_weight": max(0.0, node.base_weight),
        }
        final = max(0.0, math.fsum(components.values()) / 7.0)
        return DRSENodeScore(
            node_id=node.node_id,
            node_type=node.node_type,
            final_score=final,
            components=components,
            safe_directive=self._safe_directive(node, final),
        )

    @staticmethod
    def _marker(text: str, markers: tuple[str, ...]) -> float:
        return 1.0 if any(marker in text for marker in markers) else 0.0

    @staticmethod
    def _safe_directive(node: DRSEInputNode, score: float) -> str:
        label = node.node_type.replace("_", " ").lower()
        if score >= 0.75:
            return f"{label} 압력이 높다. 직접 설명하지 말고 행동·사물·간격으로 표면화한다."
        if score >= 0.35:
            return f"{label} 단서를 낮은 강도의 표면 힌트로 유지한다."
        return f"{label} 정보는 배경 압력으로만 둔다."
