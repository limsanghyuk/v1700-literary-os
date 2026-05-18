from __future__ import annotations

from collections import defaultdict

from v1700.nie.rag.contracts import QueryIntentResult
from v1700.nie.rag.drama_lexicon import DramaLexicon


class QueryIntentClassifier:
    """Deterministic drama-domain query classifier for Stage116.

    ADR-006/016 compatible: classification is lexical/statistical and never calls
    an LLM. The output tunes BM25/Dense weights and retrieval depth for Korean
    drama queries.
    """

    CHARACTER_THRESHOLD = 0.40
    EMOTIONAL_THRESHOLD = 0.35

    def __init__(self, drama_lexicon: DramaLexicon | None = None) -> None:
        self.drama_lexicon = drama_lexicon or DramaLexicon()
        self.llm_call_count = 0

    def classify(self, query: str) -> QueryIntentResult:
        tokens = self.drama_lexicon.tokenize(query)
        n = len(tokens) or 1
        matched: dict[str, list[str]] = defaultdict(list)
        counts = {
            "proper_noun": 0,
            "emotion": 0,
            "plot": 0,
            "episode": 0,
        }
        for token in tokens:
            category = self.drama_lexicon.category(token)
            if category == "CHARACTER_NAMES":
                counts["proper_noun"] += 1
                matched["CHARACTER_NAMES"].append(token)
            elif category == "EMOTION_WORDS":
                counts["emotion"] += 1
                matched["EMOTION_WORDS"].append(token)
            elif category == "EPISODE_TERMS":
                counts["episode"] += 1
                matched["EPISODE_TERMS"].append(token)
            elif category == "DRAMA_KEYWORDS":
                counts["plot"] += 1
                matched["DRAMA_KEYWORDS"].append(token)

        proper_noun_ratio = counts["proper_noun"] / n
        emotion_ratio = counts["emotion"] / n
        plot_ratio = counts["plot"] / n
        episode_ratio = counts["episode"] / n

        # A short drama query naming one or more characters should remain a
        # CHARACTER query even when Korean spacing makes the ratio slightly
        # brittle. This is deterministic and keeps ADR-016's lexical intent.
        character_signal = proper_noun_ratio > self.CHARACTER_THRESHOLD or (counts["proper_noun"] >= 1 and n <= 4)
        emotional_signal = emotion_ratio > self.EMOTIONAL_THRESHOLD or (counts["emotion"] >= 1 and n <= 4)

        if character_signal:
            intent = "CHARACTER"
            bm25_weight, dense_weight, k = 0.70, 0.30, 40
            confidence = max(proper_noun_ratio, 0.70)
        elif emotional_signal:
            intent = "EMOTIONAL"
            bm25_weight, dense_weight, k = 0.30, 0.70, 60
            confidence = max(emotion_ratio, 0.68)
        else:
            intent = "PLOT_EVENT"
            bm25_weight, dense_weight, k = 0.50, 0.50, 50
            confidence = max(plot_ratio + episode_ratio, 0.55)

        return QueryIntentResult(
            query=query,
            intent=intent,  # type: ignore[arg-type]
            bm25_weight=bm25_weight,
            dense_weight=dense_weight,
            k=k,
            confidence=min(float(confidence), 1.0),
            proper_noun_ratio=proper_noun_ratio,
            emotion_ratio=emotion_ratio,
            plot_ratio=plot_ratio,
            episode_ratio=episode_ratio,
            token_count=len(tokens),
            matched_terms={key: sorted(set(value)) for key, value in matched.items()},
            llm_call_count=self.llm_call_count,
        )
