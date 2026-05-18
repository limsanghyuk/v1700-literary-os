from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

Status = Literal["pass", "warn", "blocked"]


def _round(value: float) -> float:
    return round(float(value), 6)


@dataclass(frozen=True)
class RepairOutcome:
    scene_id: str
    recommendation_id: str
    category: str
    severity: float
    success: bool
    blast_ratio: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "scene_id": self.scene_id,
            "recommendation_id": self.recommendation_id,
            "category": self.category,
            "severity": _round(self.severity),
            "success": self.success,
            "blast_ratio": _round(self.blast_ratio),
        }


@dataclass(frozen=True)
class CategoryStats:
    category: str
    total: int
    successes: int
    mean_severity: float
    mean_blast_ratio: float

    @property
    def failures(self) -> int:
        return max(0, self.total - self.successes)

    def success_rate(self) -> float:
        return _round(self.successes / max(1, self.total))

    def failure_rate(self) -> float:
        return _round(self.failures / max(1, self.total))

    def to_dict(self) -> dict[str, Any]:
        return {
            "category": self.category,
            "total": self.total,
            "successes": self.successes,
            "failures": self.failures,
            "success_rate": self.success_rate(),
            "failure_rate": self.failure_rate(),
            "mean_severity": _round(self.mean_severity),
            "mean_blast_ratio": _round(self.mean_blast_ratio),
        }


@dataclass(frozen=True)
class PatternLibrarySnapshot:
    total_outcomes: int
    categories: dict[str, dict[str, Any]]
    global_feature_vector: tuple[float, float, float, float]

    def to_dict(self) -> dict[str, Any]:
        return {
            "total_outcomes": self.total_outcomes,
            "categories": self.categories,
            "global_feature_vector": [_round(v) for v in self.global_feature_vector],
        }


@dataclass(frozen=True)
class DebtPrediction:
    category: str
    probability: float
    confidence: float
    horizon: int
    mode: Literal["heuristic_fallback", "frozen_fixture"] = "heuristic_fallback"

    def to_dict(self) -> dict[str, Any]:
        return {
            "category": self.category,
            "probability": _round(self.probability),
            "confidence": _round(self.confidence),
            "horizon": self.horizon,
            "mode": self.mode,
        }


@dataclass(frozen=True)
class PredictionReport:
    scene_id: str
    horizon: int
    predictions: tuple[DebtPrediction, ...]
    threshold: float = 0.60
    sklearn_available: bool = False
    runtime_training_enabled: bool = False

    @property
    def high_risk(self) -> tuple[str, ...]:
        return tuple(p.category for p in self.predictions if p.probability >= self.threshold)

    def max_probability(self) -> float:
        return max((p.probability for p in self.predictions), default=0.0)

    def any_high_risk(self) -> bool:
        return bool(self.high_risk)

    def to_dict(self) -> dict[str, Any]:
        return {
            "scene_id": self.scene_id,
            "horizon": self.horizon,
            "threshold": _round(self.threshold),
            "predictions": [p.to_dict() for p in self.predictions],
            "high_risk": list(self.high_risk),
            "max_probability": _round(self.max_probability()),
            "sklearn_available": self.sklearn_available,
            "runtime_training_enabled": self.runtime_training_enabled,
        }


@dataclass(frozen=True)
class PreemptiveResult:
    scene_id: str
    status: Status
    blocked: bool
    threshold: float
    horizon: int
    high_risk_categories: tuple[str, ...]
    max_probability: float
    prediction_report: PredictionReport
    authority_mode: Literal["secondary_predictive_gate", "primary_release_authority"] = "secondary_predictive_gate"
    issues: tuple[str, ...] = ()

    def block_reason(self) -> str:
        if not self.blocked:
            return ""
        return "high_risk_categories=" + ",".join(self.high_risk_categories)

    def to_dict(self) -> dict[str, Any]:
        return {
            "scene_id": self.scene_id,
            "status": self.status,
            "blocked": self.blocked,
            "threshold": _round(self.threshold),
            "horizon": self.horizon,
            "high_risk_categories": list(self.high_risk_categories),
            "max_probability": _round(self.max_probability),
            "authority_mode": self.authority_mode,
            "block_reason": self.block_reason(),
            "issues": list(self.issues),
            "prediction_report": self.prediction_report.to_dict(),
        }


@dataclass(frozen=True)
class PredictionRecord:
    scene_id: str
    category: str
    predicted_probability: float
    actual_occurred: bool
    threshold: float = 0.60

    @property
    def predicted_high(self) -> bool:
        return self.predicted_probability >= self.threshold

    def to_dict(self) -> dict[str, Any]:
        return {
            "scene_id": self.scene_id,
            "category": self.category,
            "predicted_probability": _round(self.predicted_probability),
            "predicted_high": self.predicted_high,
            "actual_occurred": self.actual_occurred,
            "threshold": _round(self.threshold),
        }


@dataclass(frozen=True)
class MetricsSnapshot:
    total: int
    tp: int
    fp: int
    fn: int
    tn: int

    def precision(self) -> float:
        return _round(self.tp / max(1, self.tp + self.fp))

    def recall(self) -> float:
        return _round(self.tp / max(1, self.tp + self.fn))

    def f1(self) -> float:
        p, r = self.precision(), self.recall()
        return _round(2 * p * r / max(1e-12, p + r)) if (p + r) else 0.0

    def accuracy(self) -> float:
        return _round((self.tp + self.tn) / max(1, self.total))

    def meets_precision_target(self, target: float = 0.70) -> bool:
        return self.precision() >= target

    def to_dict(self) -> dict[str, Any]:
        return {
            "total": self.total,
            "tp": self.tp,
            "fp": self.fp,
            "fn": self.fn,
            "tn": self.tn,
            "precision": self.precision(),
            "recall": self.recall(),
            "f1": self.f1(),
            "accuracy": self.accuracy(),
        }


@dataclass(frozen=True)
class FeedbackReport:
    status: Status
    metrics: MetricsSnapshot
    precision_target: float
    records: tuple[PredictionRecord, ...]
    runtime_retraining_triggered: bool = False
    issues: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "precision_target": _round(self.precision_target),
            "runtime_retraining_triggered": self.runtime_retraining_triggered,
            "metrics": self.metrics.to_dict(),
            "records": [r.to_dict() for r in self.records],
            "issues": list(self.issues),
        }


@dataclass(frozen=True)
class Gate29Result:
    status: Status
    approved: bool
    authority_mode: Literal["secondary_predictive_gate", "primary_release_authority"]
    checks: dict[str, dict[str, Any]]
    preemptive_result: PreemptiveResult
    feedback_report: FeedbackReport
    failed_gates: tuple[str, ...] = ()
    issues: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "approved": self.approved,
            "authority_mode": self.authority_mode,
            "failed_gates": list(self.failed_gates),
            "checks": self.checks,
            "issues": list(self.issues),
            "preemptive_result": self.preemptive_result.to_dict(),
            "feedback_report": self.feedback_report.to_dict(),
        }
