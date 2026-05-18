from __future__ import annotations

from statistics import mean

from v1700.narrative_weight_kernel.contracts import (
    FeedbackSignal,
    KernelLearningReport,
    NarrativeWeightVector,
)

MAX_SINGLE_KERNEL_UPDATE_DELTA = 0.08
MAX_MEAN_KERNEL_DRIFT = 0.12
PROTECTED_NON_DECREASING = ("safety_boundary", "style_boundary")
FEEDBACK_TO_WEIGHT = {
    "agency": "agency",
    "desire_pressure": "desire_pressure",
    "wound_pressure": "wound_pressure",
    "relation_tension": "relation_tension",
    "event_causality": "event_causality",
    "knowledge_asymmetry": "knowledge_asymmetry",
    "reveal_pressure": "reveal_pressure",
    "emotional_momentum": "emotional_momentum",
    "scene_energy": "scene_energy",
    "motif_residue": "motif_residue",
    "reader_attention": "reader_attention",
    "style_boundary": "style_boundary",
    "safety_boundary": "safety_boundary",
}


def learn_kernel_weights(
    baseline: NarrativeWeightVector | None = None,
    feedback: tuple[FeedbackSignal, ...] = (),
    *,
    learning_rate: float = 0.12,
) -> KernelLearningReport:
    """Apply bounded, auditable self-calibration from observed narrative feedback.

    This is not opaque model training.  It converts failed or weak narrative axes
    into small coefficient nudges, then records every update and rejects excessive
    drift.  The result is suitable for release evidence and regression tests.
    """

    baseline = baseline or NarrativeWeightVector()
    grouped: dict[str, list[FeedbackSignal]] = {}
    for signal in feedback:
        weight_name = FEEDBACK_TO_WEIGHT.get(signal.metric)
        if not weight_name:
            continue
        grouped.setdefault(weight_name, []).append(signal)

    deltas: dict[str, float] = {}
    update_log: list[dict] = []
    for weight_name, signals in sorted(grouped.items()):
        raw_delta = mean(signal.error() * max(0.0, min(1.0, signal.confidence)) for signal in signals) * learning_rate
        clipped = max(-MAX_SINGLE_KERNEL_UPDATE_DELTA, min(MAX_SINGLE_KERNEL_UPDATE_DELTA, raw_delta))
        deltas[weight_name] = clipped
        update_log.append(
            {
                "weight": weight_name,
                "signal_count": len(signals),
                "raw_delta": round(raw_delta, 4),
                "applied_delta": round(clipped, 4),
                "sources": sorted({signal.source for signal in signals}),
            }
        )

    learned = baseline.bounded_update(deltas, max_delta=MAX_SINGLE_KERNEL_UPDATE_DELTA)
    drift_guard = _kernel_drift_guard(baseline, learned)
    issues = tuple(drift_guard["issues"])
    return KernelLearningReport(
        status="pass" if not issues else "blocked",
        baseline_weights=baseline,
        learned_weights=learned,
        feedback_signals=feedback,
        update_log=tuple(update_log),
        drift_guard=drift_guard,
        issues=issues,
    )


def _kernel_drift_guard(baseline: NarrativeWeightVector, learned: NarrativeWeightVector) -> dict:
    baseline_values = baseline.to_dict()
    learned_values = learned.to_dict()
    deltas = {key: round(learned_values[key] - baseline_values[key], 4) for key in baseline_values}
    issues: list[str] = []
    max_delta = max(abs(delta) for delta in deltas.values()) if deltas else 0.0
    mean_drift = round(sum(abs(delta) for delta in deltas.values()) / len(deltas), 4) if deltas else 0.0
    if max_delta > MAX_SINGLE_KERNEL_UPDATE_DELTA:
        issues.append("kernel_max_single_update_delta_exceeded")
    if mean_drift > MAX_MEAN_KERNEL_DRIFT:
        issues.append("kernel_mean_drift_exceeded")
    for key in PROTECTED_NON_DECREASING:
        if learned_values[key] < baseline_values[key]:
            issues.append(f"{key}_decreased")
    return {
        "status": "pass" if not issues else "blocked",
        "max_single_update_delta": round(max_delta, 4),
        "mean_drift": mean_drift,
        "protected_non_decreasing": list(PROTECTED_NON_DECREASING),
        "deltas": deltas,
        "issues": issues,
    }
