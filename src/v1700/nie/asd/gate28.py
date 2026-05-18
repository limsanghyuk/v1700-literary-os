from __future__ import annotations

from v1700.nie.asd.contracts import Gate28Result, StoryDoctorReport


class Gate28:
    """Secondary StoryQualityGate adapted from V545 ASD.

    Thresholds:
    G28-1 debt_score <= 0.50
    G28-2 arc_score <= 0.40
    G28-3 high_priority_cnt <= 5
    G28-4 combined_quality <= 0.45
    combined_quality = min(debt_score * 0.55 + arc_score * 0.45, 1.0)
    """

    DEBT_THRESHOLD = 0.50
    ARC_THRESHOLD = 0.40
    HIGH_PRIORITY_THRESHOLD = 5
    COMBINED_THRESHOLD = 0.45

    def evaluate(self, report: StoryDoctorReport) -> Gate28Result:
        debt_score = float(report.debt_report.overall_debt_score)
        arc_score = float(report.arc_report.overall_score)
        high_count = len(report.high_priority)
        combined = min(debt_score * 0.55 + arc_score * 0.45, 1.0)
        checks = {
            "G28-1": {"metric": "debt_score", "threshold": self.DEBT_THRESHOLD, "actual": round(debt_score, 6), "passed": debt_score <= self.DEBT_THRESHOLD},
            "G28-2": {"metric": "arc_score", "threshold": self.ARC_THRESHOLD, "actual": round(arc_score, 6), "passed": arc_score <= self.ARC_THRESHOLD},
            "G28-3": {"metric": "high_priority_cnt", "threshold": self.HIGH_PRIORITY_THRESHOLD, "actual": high_count, "passed": high_count <= self.HIGH_PRIORITY_THRESHOLD},
            "G28-4": {"metric": "combined_quality", "threshold": self.COMBINED_THRESHOLD, "actual": round(combined, 6), "passed": combined <= self.COMBINED_THRESHOLD},
        }
        failed = tuple(gate for gate, check in checks.items() if not check["passed"])
        issues: list[str] = []
        if report.provider_calls != 0:
            issues.append("story_doctor_provider_calls_nonzero")
        if report.mutation_allowed:
            issues.append("story_doctor_mutation_allowed")
        status = "pass" if not failed and not issues else "blocked"
        return Gate28Result(
            status=status,
            approved=status == "pass",
            checks=checks,
            combined_quality=combined,
            failed_gates=failed,
            authority_mode="secondary_quality_gate",
            issues=tuple(issues),
        )
