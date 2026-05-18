from __future__ import annotations

from v1700.nie.predictive.contracts import FeedbackReport, Gate29Result, PreemptiveResult


class Gate29:
    """Secondary predictive debt gate adapted from V555 PNE.

    Gate29 is absorbed in Stage124 as a predictive advisory/block gate, not as a
    primary release authority. It evaluates whether the PreemptiveGate behaves
    deterministically and whether the feedback precision target is met.
    """

    BLOCK_THRESHOLD = 0.60
    PRECISION_TARGET = 0.70

    def evaluate(self, preemptive: PreemptiveResult, feedback: FeedbackReport) -> Gate29Result:
        checks = {
            "G29-1": {"metric": "threshold", "expected": self.BLOCK_THRESHOLD, "actual": preemptive.threshold, "passed": abs(preemptive.threshold - self.BLOCK_THRESHOLD) < 1e-9},
            "G29-2": {"metric": "runtime_training_enabled", "expected": False, "actual": preemptive.prediction_report.runtime_training_enabled, "passed": preemptive.prediction_report.runtime_training_enabled is False},
            "G29-3": {"metric": "authority_mode", "expected": "secondary_predictive_gate", "actual": preemptive.authority_mode, "passed": preemptive.authority_mode == "secondary_predictive_gate"},
            "G29-4": {"metric": "feedback_precision", "threshold": self.PRECISION_TARGET, "actual": feedback.metrics.precision(), "passed": feedback.metrics.meets_precision_target(self.PRECISION_TARGET)},
        }
        failed = tuple(gate for gate, check in checks.items() if not check["passed"])
        issues: list[str] = []
        if feedback.runtime_retraining_triggered:
            issues.append("runtime_retraining_triggered")
        if preemptive.authority_mode == "primary_release_authority":
            issues.append("gate29_primary_authority_enabled_too_early")
        status = "pass" if not failed and not issues and not preemptive.blocked else "blocked"
        # A high-risk scene is expected to be blocked by the secondary gate. That
        # is not a release failure when checked as the negative case by Stage124.
        return Gate29Result(
            status=status,
            approved=status == "pass",
            authority_mode="secondary_predictive_gate",
            checks=checks,
            preemptive_result=preemptive,
            feedback_report=feedback,
            failed_gates=failed,
            issues=tuple(issues),
        )
