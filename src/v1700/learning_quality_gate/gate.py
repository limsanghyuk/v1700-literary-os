from __future__ import annotations

from typing import Any

from .contracts import CandidateRegistry, LearningCandidate

LEARNING_QUALITY_MODE = "LEARNING_QUALITY_GATE_CANDIDATE_ONLY"


def build_candidate_registry(stage134_report: dict[str, Any]) -> CandidateRegistry:
    audit = stage134_report.get("parts", {}).get("meta_learner_audit", {})
    cases = audit.get("cases", [])
    if not cases and "aggregate" in audit:
        cases = _fallback_cases_from_aggregate(audit)
    candidates = tuple(_candidate_from_case(case) for case in cases)
    issues: list[str] = []
    if not candidates:
        issues.append("missing_stage134_audit_cases")
    if any(candidate.learning_allowed for candidate in candidates):
        issues.append("learning_enabled")
    if any(candidate.training_triggered for candidate in candidates):
        issues.append("training_triggered")
    if any(candidate.mutation_allowed for candidate in candidates):
        issues.append("mutation_allowed")
    if any(candidate.provider_call_required for candidate in candidates):
        issues.append("provider_call_required")
    if not any(candidate.decision == "REVIEW_ONLY" for candidate in candidates):
        issues.append("review_only_route_missing")
    counters = {
        "candidate_count": len(candidates),
        "accepted_candidate_count": sum(1 for c in candidates if c.decision == "ACCEPT_CANDIDATE"),
        "rejected_candidate_count": sum(1 for c in candidates if c.decision == "REJECT_CANDIDATE"),
        "review_only_count": sum(1 for c in candidates if c.decision == "REVIEW_ONLY"),
        "learning_allowed_count": sum(1 for c in candidates if c.learning_allowed),
        "training_triggered_count": sum(1 for c in candidates if c.training_triggered),
        "mutation_allowed_count": sum(1 for c in candidates if c.mutation_allowed),
    }
    return CandidateRegistry(
        stage="135",
        baseline_stage="134",
        status="pass" if not issues else "blocked",
        candidates=candidates,
        issues=tuple(issues),
        counters=counters,
    )


def _candidate_from_case(case: dict[str, Any]) -> LearningCandidate:
    recommendation = str(case.get("recommendation", "OBSERVE"))
    writer_review = bool(case.get("writer_review_required"))
    if recommendation == "RECOMMEND_REVIEW" or writer_review:
        decision = "REVIEW_ONLY"
        reason = "human review is required; the case is not eligible for learning ingestion"
        gate_verified = True
    elif recommendation == "RECOMMEND_WEIGHT_CANDIDATE":
        decision = "ACCEPT_CANDIDATE"
        reason = "candidate is recorded for future offline weighting only; no training trigger is allowed"
        gate_verified = True
    else:
        decision = "REJECT_CANDIDATE"
        reason = "stable observation is not useful as a learning candidate"
        gate_verified = True
    return LearningCandidate(
        case_id=str(case.get("case_id", "unknown")),
        source_stage="stage134",
        source_recommendation=recommendation,
        decision=decision,  # type: ignore[arg-type]
        reason=reason,
        gate_verified=gate_verified,
        writer_review_required=writer_review or decision == "REVIEW_ONLY",
    )


def _fallback_cases_from_aggregate(audit: dict[str, Any]) -> list[dict[str, Any]]:
    aggregate = audit.get("aggregate", {})
    review_count = int(aggregate.get("review_recommendation_count", 0))
    observe_count = int(aggregate.get("observe_count", 0))
    weight_count = int(aggregate.get("weight_candidate_count", 0))
    cases: list[dict[str, Any]] = []
    cases.extend({"case_id": f"STAGE134-REVIEW-{i+1}", "recommendation": "RECOMMEND_REVIEW", "writer_review_required": True} for i in range(review_count))
    cases.extend({"case_id": f"STAGE134-WEIGHT-{i+1}", "recommendation": "RECOMMEND_WEIGHT_CANDIDATE", "writer_review_required": False} for i in range(weight_count))
    cases.extend({"case_id": f"STAGE134-OBSERVE-{i+1}", "recommendation": "OBSERVE", "writer_review_required": False} for i in range(observe_count))
    return cases
