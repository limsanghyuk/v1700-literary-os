from __future__ import annotations

from .engine import run_quality_endurance_smoke


class QualityEnduranceGate:
    def validate(self) -> dict:
        report = run_quality_endurance_smoke()
        issues: list[str] = []
        if report.get("status") != "pass":
            issues.append("quality_endurance_report_blocked")
        if report.get("scene_count", 0) < 30:
            issues.append("actual_scene_rendering_below_30")
        if report.get("average_after", 0.0) < 8.0:
            issues.append("quality_average_after_below_8")
        if report.get("average_delta", 0.0) < 0.5:
            issues.append("refinement_delta_below_0_5")
        if report.get("blocker_count_after", 1) != 0:
            issues.append("quality_blockers_remain_after_refinement")
        if report.get("reveal_leakage_count", 1) != 0:
            issues.append("reveal_leakage_detected")
        return {
            "status": "pass" if not issues else "blocked",
            "issues": issues,
            "quality_endurance_report": report,
        }
