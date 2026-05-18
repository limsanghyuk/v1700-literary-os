from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ProviderCandidate:
    candidate_id: str
    provider_id: str
    provider_kind: str
    prompt_id: str
    normalized_response: str
    estimated_cost: float
    latency_ms: int
    safety_flags: tuple[str, ...]
    metadata: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "candidate_id": self.candidate_id,
            "provider_id": self.provider_id,
            "provider_kind": self.provider_kind,
            "prompt_id": self.prompt_id,
            "normalized_response_preview": self.normalized_response[:160],
            "estimated_cost": self.estimated_cost,
            "latency_ms": self.latency_ms,
            "safety_flags": list(self.safety_flags),
            "metadata": self.metadata,
        }


@dataclass(frozen=True)
class ArbitrationDecision:
    candidate_id: str
    provider_id: str
    decision: str
    arbitration_score: float
    reasons: tuple[str, ...]
    directive: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "candidate_id": self.candidate_id,
            "provider_id": self.provider_id,
            "decision": self.decision,
            "arbitration_score": self.arbitration_score,
            "reasons": list(self.reasons),
            "directive": self.directive,
        }
