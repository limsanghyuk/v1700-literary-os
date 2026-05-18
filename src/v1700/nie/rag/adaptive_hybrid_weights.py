from __future__ import annotations

from collections.abc import Sequence

from v1700.nie.rag.contracts import AdaptiveHybridPolicy, QueryIntentResult


class AdaptiveHybridWeights:
    """Apply Stage116 query-intent weights to a hybrid retrieval policy."""

    def policy_for(self, result: QueryIntentResult) -> AdaptiveHybridPolicy:
        return AdaptiveHybridPolicy(
            intent=result.intent,
            bm25_weight=result.bm25_weight,
            dense_weight=result.dense_weight,
            k=result.k,
            rrf_k=60,
        )

    def weighted_rrf_score(self, bm25_rank: int | None, dense_rank: int | None, policy: AdaptiveHybridPolicy) -> float:
        score = 0.0
        if bm25_rank is not None:
            score += policy.bm25_weight / (policy.rrf_k + bm25_rank)
        if dense_rank is not None:
            score += policy.dense_weight / (policy.rrf_k + dense_rank)
        return round(score, 9)

    def fuse(self, bm25_ids: Sequence[str], dense_ids: Sequence[str], policy: AdaptiveHybridPolicy) -> list[dict]:
        ids = list(dict.fromkeys([*bm25_ids, *dense_ids]))
        fused: list[dict] = []
        for doc_id in ids:
            bm25_rank = bm25_ids.index(doc_id) + 1 if doc_id in bm25_ids else None
            dense_rank = dense_ids.index(doc_id) + 1 if doc_id in dense_ids else None
            fused.append({
                "doc_id": doc_id,
                "bm25_rank": bm25_rank,
                "dense_rank": dense_rank,
                "score": self.weighted_rrf_score(bm25_rank, dense_rank, policy),
            })
        return sorted(fused, key=lambda row: (-row["score"], row["doc_id"]))[: policy.k]
