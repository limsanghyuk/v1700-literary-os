from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Literal


@dataclass
class Stage100ReleaseCandidate:
    stage: str
    baseline_stage: str
    rc_version: str
    gitnexus_preflight_status: str
    branchpoint_survival_status: str
    dual_mode_evaluation_status: str
    provider_certification_status: str
    release_gate_status: str
    stage100_readiness_status: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class DualModeEvaluationResult:
    seed_id: str
    mode: Literal["PROSE", "SCENARIO"]
    candidate_id: str
    engine_profile: str
    score_total: float
    score_breakdown: dict[str, float]
    reviewer_notes: list[str]
    release_relevance: Literal["INFO", "WARN", "BLOCK"] = "INFO"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ProviderCertificationResult:
    provider_id: str
    provider_kind: Literal["gpt", "claude", "gemini", "ollama", "fixture", "mock"]
    contract_status: Literal["PASS", "WARN", "BLOCK"]
    live_call_count_in_release: int
    response_normalization_status: str
    cost_ledger_status: str
    raw_manuscript_leakage: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class GitNexusRCPreflightReport:
    index_freshness_status: str
    list_repos_status: str
    query_context_impact_status: str
    detect_changes_status: str
    concept_impact_status: str
    survival_matrix_status: str
    symbol_to_branchpoint_trace_status: str
    shape_check_status: str
    release_gate_integration_status: str
    repo_doctor_status: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

