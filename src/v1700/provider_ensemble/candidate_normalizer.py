from __future__ import annotations

from v1700.provider_ensemble.contracts import ProviderCandidate


def normalize_candidates(candidates: tuple[ProviderCandidate, ...]) -> tuple[ProviderCandidate, ...]:
    normalized = []
    for candidate in candidates:
        normalized.append(
            ProviderCandidate(
                candidate_id=candidate.candidate_id,
                provider_id=candidate.provider_id,
                provider_kind=candidate.provider_kind,
                prompt_id=candidate.prompt_id,
                normalized_response=" ".join(candidate.normalized_response.split()),
                estimated_cost=candidate.estimated_cost,
                latency_ms=candidate.latency_ms,
                safety_flags=candidate.safety_flags,
                metadata={**candidate.metadata, "normalized_schema_pass": True},
            )
        )
    return tuple(normalized)
