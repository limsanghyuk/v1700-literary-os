from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Stage116Contract:
    stage: str = "116"
    baseline_stage: str = "115"
    title: str = "Domain-Specific RAG Fusion"
    query_intent_classifier_required: bool = True
    drama_lexicon_boost_required: bool = True
    adaptive_bm25_dense_weights_required: bool = True
    llm_query_classification_allowed: bool = False
    embedding_provider_calls_allowed_in_release_gate: bool = False
    rrf_k: int = 60
    next_development_order: tuple[str, ...] = ("Stage117", "Stage118", "Stage119", "Stage120")

    def to_dict(self) -> dict[str, Any]:
        return {
            "stage": self.stage,
            "baseline_stage": self.baseline_stage,
            "title": self.title,
            "query_intent_classifier_required": self.query_intent_classifier_required,
            "drama_lexicon_boost_required": self.drama_lexicon_boost_required,
            "adaptive_bm25_dense_weights_required": self.adaptive_bm25_dense_weights_required,
            "llm_query_classification_allowed": self.llm_query_classification_allowed,
            "embedding_provider_calls_allowed_in_release_gate": self.embedding_provider_calls_allowed_in_release_gate,
            "rrf_k": self.rrf_k,
            "next_development_order": list(self.next_development_order),
        }
