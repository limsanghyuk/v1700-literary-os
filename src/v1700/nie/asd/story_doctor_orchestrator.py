from __future__ import annotations

from collections.abc import Mapping

from v1700.nie.asd.arc_consistency_checker import ArcConsistencyChecker
from v1700.nie.asd.contracts import RepairRecommendation, StoryDoctorReport
from v1700.nie.asd.narrative_debt_detector import NarrativeDebtDetector


_DEBT_CATEGORY = {
    "unresolved_secret": "resolve_secret",
    "broken_foreshadow": "fix_foreshadow",
    "abandoned_thread": "revive_thread",
}

_ARC_CATEGORY = {
    "arc_not_tracked": "arc_tracking",
    "arc_post_death_edge": "arc_post_death",
    "arc_contradiction_overflow": "arc_contradiction",
    "arc_episode_inversion": "arc_inversion",
}


class StoryDoctorOrchestrator:
    """Builds prioritized ASD recommendations without mutating graph state."""

    BLAST_WEIGHT = 1.5
    HIGH_THRESHOLD = 0.70
    MEDIUM_THRESHOLD = 0.40

    def __init__(self) -> None:
        self.debt_detector = NarrativeDebtDetector()
        self.arc_checker = ArcConsistencyChecker()

    def diagnose(self, graph: Mapping) -> StoryDoctorReport:
        debt = self.debt_detector.detect(graph)
        arc = self.arc_checker.check(graph)
        recs: list[RepairRecommendation] = []
        for item in debt.items:
            recs.append(RepairRecommendation(
                recommendation_id=f"R-{len(recs)+1:03d}",
                category=_DEBT_CATEGORY.get(item.debt_type, "review_debt"),
                node_id=item.node_id,
                label=item.label,
                severity=item.severity,
                blast_ratio=item.blast_ratio,
                priority_score=self.priority(item.severity, item.blast_ratio),
                source="debt",
                related_ids=item.related_ids,
            ))
        for issue in arc.issues_found:
            recs.append(RepairRecommendation(
                recommendation_id=f"R-{len(recs)+1:03d}",
                category=_ARC_CATEGORY.get(issue.issue_type, "review_arc"),
                node_id=issue.character_id,
                label=issue.label,
                severity=issue.severity,
                blast_ratio=0.0,
                priority_score=self.priority(issue.severity, 0.0),
                source="arc",
                related_ids=issue.related_ids,
            ))
        recs.sort(key=lambda r: r.priority_score, reverse=True)
        high = tuple(r for r in recs if r.priority_score >= self.HIGH_THRESHOLD)
        medium = tuple(r for r in recs if self.MEDIUM_THRESHOLD <= r.priority_score < self.HIGH_THRESHOLD)
        low = tuple(r for r in recs if r.priority_score < self.MEDIUM_THRESHOLD)
        issues: list[str] = []
        provider_calls = 0
        mutation_allowed = False
        if provider_calls:
            issues.append("provider_calls_nonzero")
        if mutation_allowed:
            issues.append("mutation_enabled_in_stage123")
        return StoryDoctorReport(
            status="pass" if not issues else "blocked",
            debt_report=debt,
            arc_report=arc,
            recommendations=tuple(recs),
            high_priority=high,
            medium_priority=medium,
            low_priority=low,
            mutation_allowed=mutation_allowed,
            provider_calls=provider_calls,
            issues=tuple(issues),
        )

    def priority(self, severity: float, blast_ratio: float) -> float:
        return round(min(1.0, float(severity) * (1.0 + self.BLAST_WEIGHT * float(blast_ratio))), 6)
