from __future__ import annotations

from typing import Any

from .contracts import NarrativeStateTensor, TensorMeasurementReport

DIMENSIONS: tuple[str, ...] = (
    "causality_integrity",
    "temporal_continuity",
    "reveal_budget_integrity",
    "character_agency",
    "emotional_momentum",
    "voice_stability",
    "attention_economy",
    "canon_isolation",
)


def measure_stage132_classifier_output(classifier_matrix: dict[str, Any]) -> TensorMeasurementReport:
    classifications = classifier_matrix.get("classifications", [])
    tensors = tuple(_measure_case(item) for item in classifications)
    issues: list[str] = []
    if len(DIMENSIONS) != 8:
        issues.append("dimension_count_not_8")
    if not tensors:
        issues.append("missing_tensor_cases")
    if any(item.mutation_allowed for item in tensors):
        issues.append("mutation_enabled")
    if any(item.provider_call_required for item in tensors):
        issues.append("provider_call_required")
    if not any(item.writer_review_required for item in tensors):
        issues.append("writer_review_route_missing")
    if not any(item.classification == "intentional_mystery" and item.status == "PASS" for item in tensors):
        issues.append("mystery_exemption_measurement_missing")
    average_vector = _average_vector(tensors)
    return TensorMeasurementReport(
        stage="133",
        baseline_stage="132",
        status="pass" if not issues else "blocked",
        dimensions=DIMENSIONS,
        tensors=tensors,
        average_vector=average_vector,
        issues=tuple(issues),
    )


def _measure_case(classification: dict[str, Any]) -> NarrativeStateTensor:
    kind = str(classification.get("classification", "unknown"))
    review = bool(classification.get("requires_writer_approval"))
    dimensions = _base_vector()
    if kind == "true_contradiction":
        dimensions.update(
            {
                "causality_integrity": 0.58,
                "reveal_budget_integrity": 0.62,
                "canon_isolation": 0.52,
                "attention_economy": 0.72,
            }
        )
        status = "REVIEW_REQUIRED"
    elif kind == "intentional_mystery":
        dimensions.update(
            {
                "reveal_budget_integrity": 0.94,
                "attention_economy": 0.91,
                "canon_isolation": 0.88,
            }
        )
        status = "PASS"
    elif kind == "character_misunderstanding":
        dimensions.update(
            {
                "canon_isolation": 0.90,
                "character_agency": 0.87,
                "voice_stability": 0.88,
            }
        )
        status = "PASS"
    elif kind == "reveal_delay":
        dimensions.update(
            {
                "temporal_continuity": 0.86,
                "reveal_budget_integrity": 0.89,
                "attention_economy": 0.88,
            }
        )
        status = "PASS"
    elif kind == "no_conflict":
        dimensions.update(
            {
                "causality_integrity": 0.96,
                "temporal_continuity": 0.95,
                "canon_isolation": 0.96,
            }
        )
        status = "PASS"
    else:
        dimensions.update({"causality_integrity": 0.68, "canon_isolation": 0.66})
        status = "WATCH"
    lowest_dimension, lowest_score = min(dimensions.items(), key=lambda item: item[1])
    return NarrativeStateTensor(
        case_id=str(classification.get("case_id", "")),
        classification=kind,
        dimensions=dimensions,
        status=status,
        lowest_dimension=lowest_dimension,
        lowest_score=round(lowest_score, 3),
        writer_review_required=review,
    )


def _base_vector() -> dict[str, float]:
    return {
        "causality_integrity": 0.84,
        "temporal_continuity": 0.84,
        "reveal_budget_integrity": 0.84,
        "character_agency": 0.84,
        "emotional_momentum": 0.84,
        "voice_stability": 0.84,
        "attention_economy": 0.84,
        "canon_isolation": 0.84,
    }


def _average_vector(tensors: tuple[NarrativeStateTensor, ...]) -> dict[str, float]:
    if not tensors:
        return {name: 0.0 for name in DIMENSIONS}
    return {
        name: round(sum(item.dimensions[name] for item in tensors) / len(tensors), 3)
        for name in DIMENSIONS
    }
