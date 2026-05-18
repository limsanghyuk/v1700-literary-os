from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ProviderEvaluationPrompt:
    prompt_id: str
    task: str
    system: str
    prompt: str
    branchpoint_requirements: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "prompt_id": self.prompt_id,
            "task": self.task,
            "system_present": bool(self.system),
            "prompt_preview": self.prompt[:160],
            "branchpoint_requirements": list(self.branchpoint_requirements),
        }


@dataclass(frozen=True)
class ProviderEvaluationScore:
    provider_id: str
    provider_kind: str
    prompt_id: str
    request_id: str
    normalized_schema_pass: bool
    latency_ms: int
    input_tokens: int
    output_tokens: int
    estimated_cost_units: float
    safety_score: float
    literary_quality_score: float
    branchpoint_compliance_score: float
    live_call_performed: bool
    issues: tuple[str, ...] = ()

    @property
    def total_score(self) -> float:
        return round(
            self.safety_score * 0.25
            + self.literary_quality_score * 0.30
            + self.branchpoint_compliance_score * 0.30
            + max(0.0, 10.0 - self.estimated_cost_units) * 0.10
            + max(0.0, 10.0 - self.latency_ms / 1000.0) * 0.05,
            2,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "provider_id": self.provider_id,
            "provider_kind": self.provider_kind,
            "prompt_id": self.prompt_id,
            "request_id": self.request_id,
            "normalized_schema_pass": self.normalized_schema_pass,
            "latency_ms": self.latency_ms,
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "estimated_cost_units": self.estimated_cost_units,
            "safety_score": self.safety_score,
            "literary_quality_score": self.literary_quality_score,
            "branchpoint_compliance_score": self.branchpoint_compliance_score,
            "total_score": self.total_score,
            "live_call_performed": self.live_call_performed,
            "issues": list(self.issues),
        }


@dataclass(frozen=True)
class ProviderEvaluationProfile:
    provider_id: str
    provider_kind: str
    average_score: float
    average_latency_ms: int
    estimated_cost_units: float
    strengths: tuple[str, ...]
    weaknesses: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "provider_id": self.provider_id,
            "provider_kind": self.provider_kind,
            "average_score": self.average_score,
            "average_latency_ms": self.average_latency_ms,
            "estimated_cost_units": self.estimated_cost_units,
            "strengths": list(self.strengths),
            "weaknesses": list(self.weaknesses),
        }


@dataclass(frozen=True)
class ProviderEvaluationReport:
    stage: str
    status: str
    mode: str
    prompt_count: int
    provider_count: int
    evaluation_count: int
    scores: tuple[ProviderEvaluationScore, ...]
    provider_profiles: tuple[ProviderEvaluationProfile, ...]
    best_provider_id: str
    live_call_count: int
    provider_default_calls: int
    node2_raw_reveal_access_count: int
    credential_secret_value_leaked: bool
    normalized_schema_fail_count: int
    issues: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "stage": self.stage,
            "status": self.status,
            "mode": self.mode,
            "prompt_count": self.prompt_count,
            "provider_count": self.provider_count,
            "evaluation_count": self.evaluation_count,
            "scores": [score.to_dict() for score in self.scores],
            "provider_profiles": [profile.to_dict() for profile in self.provider_profiles],
            "best_provider_id": self.best_provider_id,
            "live_call_count": self.live_call_count,
            "provider_default_calls": self.provider_default_calls,
            "node2_raw_reveal_access_count": self.node2_raw_reveal_access_count,
            "credential_secret_value_leaked": self.credential_secret_value_leaked,
            "normalized_schema_fail_count": self.normalized_schema_fail_count,
            "issues": list(self.issues),
        }
