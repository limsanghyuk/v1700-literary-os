from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

Status = Literal["pass", "warn", "blocked"]


@dataclass(frozen=True)
class DebtItem:
    debt_id: str
    debt_type: str
    node_id: str
    label: str
    severity: float
    blast_ratio: float = 0.0
    related_ids: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "debt_id": self.debt_id,
            "debt_type": self.debt_type,
            "node_id": self.node_id,
            "label": self.label,
            "severity": round(self.severity, 6),
            "blast_ratio": round(self.blast_ratio, 6),
            "related_ids": list(self.related_ids),
        }


@dataclass(frozen=True)
class NarrativeDebtReport:
    status: Status
    items: tuple[DebtItem, ...] = ()
    overall_debt_score: float = 0.0
    issues: tuple[str, ...] = ()

    @property
    def total_debts(self) -> int:
        return len(self.items)

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "total_debts": self.total_debts,
            "overall_debt_score": round(self.overall_debt_score, 6),
            "items": [item.to_dict() for item in self.items],
            "issues": list(self.issues),
        }


@dataclass(frozen=True)
class ArcIssue:
    issue_id: str
    issue_type: str
    character_id: str
    label: str
    severity: float
    related_ids: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "issue_id": self.issue_id,
            "issue_type": self.issue_type,
            "character_id": self.character_id,
            "label": self.label,
            "severity": round(self.severity, 6),
            "related_ids": list(self.related_ids),
        }


@dataclass(frozen=True)
class ArcConsistencyReport:
    status: Status
    issues_found: tuple[ArcIssue, ...] = ()
    overall_score: float = 0.0
    issues: tuple[str, ...] = ()

    @property
    def total_issues(self) -> int:
        return len(self.issues_found)

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "total_issues": self.total_issues,
            "overall_score": round(self.overall_score, 6),
            "issues_found": [issue.to_dict() for issue in self.issues_found],
            "issues": list(self.issues),
        }


@dataclass(frozen=True)
class RepairRecommendation:
    recommendation_id: str
    category: str
    node_id: str
    label: str
    severity: float
    blast_ratio: float
    priority_score: float
    source: str
    related_ids: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "recommendation_id": self.recommendation_id,
            "category": self.category,
            "node_id": self.node_id,
            "label": self.label,
            "severity": round(self.severity, 6),
            "blast_ratio": round(self.blast_ratio, 6),
            "priority_score": round(self.priority_score, 6),
            "source": self.source,
            "related_ids": list(self.related_ids),
        }


@dataclass(frozen=True)
class StoryDoctorReport:
    status: Status
    debt_report: NarrativeDebtReport
    arc_report: ArcConsistencyReport
    recommendations: tuple[RepairRecommendation, ...]
    high_priority: tuple[RepairRecommendation, ...]
    medium_priority: tuple[RepairRecommendation, ...]
    low_priority: tuple[RepairRecommendation, ...]
    mutation_allowed: bool = False
    provider_calls: int = 0
    issues: tuple[str, ...] = ()

    @property
    def total_issues(self) -> int:
        return self.debt_report.total_debts + self.arc_report.total_issues

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "total_issues": self.total_issues,
            "mutation_allowed": self.mutation_allowed,
            "provider_calls": self.provider_calls,
            "debt_report": self.debt_report.to_dict(),
            "arc_report": self.arc_report.to_dict(),
            "recommendations": [rec.to_dict() for rec in self.recommendations],
            "high_priority": [rec.to_dict() for rec in self.high_priority],
            "medium_priority": [rec.to_dict() for rec in self.medium_priority],
            "low_priority": [rec.to_dict() for rec in self.low_priority],
            "issues": list(self.issues),
        }


@dataclass(frozen=True)
class ExecutionResult:
    recommendation_id: str
    status: Literal["dry_run", "approved", "gate_fail", "blocked"]
    mutation_performed: bool = False
    message: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "recommendation_id": self.recommendation_id,
            "status": self.status,
            "mutation_performed": self.mutation_performed,
            "message": self.message,
        }


@dataclass(frozen=True)
class AutoRepairExecutionReport:
    status: Status
    total: int
    dry_run: int
    approved: int
    gate_failed: int
    mutation_count: int
    results: tuple[ExecutionResult, ...] = ()
    issues: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "total": self.total,
            "dry_run": self.dry_run,
            "approved": self.approved,
            "gate_failed": self.gate_failed,
            "mutation_count": self.mutation_count,
            "results": [result.to_dict() for result in self.results],
            "issues": list(self.issues),
        }


@dataclass(frozen=True)
class Gate28Result:
    status: Status
    approved: bool
    checks: dict[str, dict[str, Any]]
    combined_quality: float
    failed_gates: tuple[str, ...] = ()
    authority_mode: Literal["secondary_quality_gate", "primary_release_authority"] = "secondary_quality_gate"
    issues: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "approved": self.approved,
            "authority_mode": self.authority_mode,
            "combined_quality": round(self.combined_quality, 6),
            "failed_gates": list(self.failed_gates),
            "checks": self.checks,
            "issues": list(self.issues),
        }
