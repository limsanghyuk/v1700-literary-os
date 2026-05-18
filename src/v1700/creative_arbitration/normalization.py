from __future__ import annotations


def normalize_candidate_payload(candidate: dict) -> dict:
    normalized = dict(candidate)
    normalized["normalized"] = True
    normalized["raw_manuscript_removed"] = not bool(candidate.get("contains_raw_manuscript"))
    normalized["response_schema"] = "CreativeCandidate/v1"
    return normalized


def build_response_normalization_matrix(candidates: list[dict]) -> dict:
    normalized = [normalize_candidate_payload(candidate) for candidate in candidates]
    issues = [item["candidate_id"] for item in normalized if not item.get("raw_manuscript_removed")]
    return {
        "stage": "105.2-normalization",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "response_schema": "CreativeCandidate/v1",
        "normalized_count": len(normalized),
        "normalized_candidates": normalized,
    }
