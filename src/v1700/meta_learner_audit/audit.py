from __future__ import annotations

from typing import Any

from .contracts import MetaLearnerAuditCase, MetaLearnerAuditReport

AUDIT_MODE = "META_LEARNER_AUDIT_ONLY_NO_TRAINING"


def audit_stage133_tensor_report(stage133_report: dict[str, Any]) -> MetaLearnerAuditReport:
    tensor = stage133_report.get("parts", {}).get("tensor_measurement", {})
    cases = tuple(_audit_case(item) for item in tensor.get("tensors", []))
    issues: list[str] = []
    if not cases:
        issues.append("missing_stage133_tensor_cases")
    if any(case.training_allowed for case in cases):
        issues.append("training_enabled")
    if any(case.mutation_allowed for case in cases):
        issues.append("mutation_enabled")
    if any(case.active_learning_allowed for case in cases):
        issues.append("active_learning_enabled")
    if any(case.provider_call_required for case in cases):
        issues.append("provider_call_required")
    if not any(case.recommendation == "RECOMMEND_REVIEW" for case in cases):
        issues.append("review_recommendation_missing")
    aggregate = {
        "case_count": len(cases),
        "observe_count": sum(1 for case in cases if case.recommendation == "OBSERVE"),
        "review_recommendation_count": sum(1 for case in cases if case.recommendation == "RECOMMEND_REVIEW"),
        "weight_candidate_count": sum(1 for case in cases if case.recommendation == "RECOMMEND_WEIGHT_CANDIDATE"),
        "training_allowed_count": sum(1 for case in cases if case.training_allowed),
        "mutation_allowed_count": sum(1 for case in cases if case.mutation_allowed),
        "active_learning_allowed_count": sum(1 for case in cases if case.active_learning_allowed),
    }
    return MetaLearnerAuditReport(
        stage="134",
        baseline_stage="133",
        status="pass" if not issues else "blocked",
        mode=AUDIT_MODE,
        cases=cases,
        issues=tuple(issues),
        aggregate=aggregate,
    )


def _audit_case(tensor_case: dict[str, Any]) -> MetaLearnerAuditCase:
    classification = str(tensor_case.get("classification", "unknown"))
    tensor_status = str(tensor_case.get("status", "WATCH"))
    lowest_dimension = str(tensor_case.get("lowest_dimension", ""))
    lowest_score = float(tensor_case.get("lowest_score", 0.0))
    writer_review_required = bool(tensor_case.get("writer_review_required")) or tensor_status == "REVIEW_REQUIRED"
    if tensor_status == "REVIEW_REQUIRED" or classification == "true_contradiction":
        recommendation = "RECOMMEND_REVIEW"
        rationale = "true contradiction remains human-review only; no auto-repair or training is permitted"
        writer_review_required = True
    elif lowest_score < 0.80:
        recommendation = "RECOMMEND_WEIGHT_CANDIDATE"
        rationale = "low tensor dimension observed; record an audit candidate without changing weights"
    else:
        recommendation = "OBSERVE"
        rationale = "tensor state is stable; observe only"
    return MetaLearnerAuditCase(
        case_id=str(tensor_case.get("case_id", "")),
        source_classification=classification,
        tensor_status=tensor_status,
        lowest_dimension=lowest_dimension,
        lowest_score=round(lowest_score, 3),
        recommendation=recommendation,  # type: ignore[arg-type]
        rationale=rationale,
        writer_review_required=writer_review_required,
    )
