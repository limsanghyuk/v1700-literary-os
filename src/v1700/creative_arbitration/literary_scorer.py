from __future__ import annotations


def score_candidates(candidates: list[dict]) -> dict:
    weighted = []
    for candidate in candidates:
        base = float(candidate.get("score", 0.0))
        task = candidate.get("task")
        mode = candidate.get("mode")
        bonus = 0.15 if task in {"DIALOGUE", "VISUAL", "STRUCTURE"} else 0.0
        if mode == "HYBRID":
            bonus += 0.05
        weighted.append({**candidate, "weighted_score": round(base + bonus, 3)})
    return {
        "stage": "105.3-scoring",
        "status": "pass",
        "scoring_policy": "role_weighted_feature_only",
        "weighted_candidates": weighted,
    }
