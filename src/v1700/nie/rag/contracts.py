from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

QueryIntent = Literal["CHARACTER", "EMOTIONAL", "PLOT_EVENT"]


@dataclass(frozen=True)
class QueryIntentResult:
    query: str
    intent: QueryIntent
    bm25_weight: float
    dense_weight: float
    k: int
    confidence: float
    proper_noun_ratio: float
    emotion_ratio: float
    plot_ratio: float
    episode_ratio: float
    token_count: int
    matched_terms: dict[str, list[str]] = field(default_factory=dict)
    llm_call_count: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "query": self.query,
            "intent": self.intent,
            "bm25_weight": round(float(self.bm25_weight), 6),
            "dense_weight": round(float(self.dense_weight), 6),
            "k": int(self.k),
            "confidence": round(float(self.confidence), 6),
            "proper_noun_ratio": round(float(self.proper_noun_ratio), 6),
            "emotion_ratio": round(float(self.emotion_ratio), 6),
            "plot_ratio": round(float(self.plot_ratio), 6),
            "episode_ratio": round(float(self.episode_ratio), 6),
            "token_count": int(self.token_count),
            "matched_terms": self.matched_terms,
            "llm_call_count": int(self.llm_call_count),
        }


@dataclass(frozen=True)
class DramaLexiconBoost:
    term: str
    category: str
    boost: float

    def to_dict(self) -> dict[str, Any]:
        return {"term": self.term, "category": self.category, "boost": round(float(self.boost), 6)}


@dataclass(frozen=True)
class AdaptiveHybridPolicy:
    intent: QueryIntent
    bm25_weight: float
    dense_weight: float
    k: int
    rrf_k: int = 60

    def to_dict(self) -> dict[str, Any]:
        return {
            "intent": self.intent,
            "bm25_weight": round(float(self.bm25_weight), 6),
            "dense_weight": round(float(self.dense_weight), 6),
            "k": int(self.k),
            "rrf_k": int(self.rrf_k),
        }
