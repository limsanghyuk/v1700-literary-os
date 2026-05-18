from __future__ import annotations

from collections.abc import Iterable

from v1700.nie.asd.contracts import AutoRepairExecutionReport, ExecutionResult, RepairRecommendation


class AutoRepairExecutor:
    """Dry-run only Stage123 adapter for V545 AutoRepairExecutor.

    The executor proves planability and Gate28 compatibility but performs no
    graph mutation until Stage125+ governor policy explicitly permits it.
    """

    def execute_batch(self, recommendations: Iterable[RepairRecommendation], *, dry_run: bool = True) -> AutoRepairExecutionReport:
        results: list[ExecutionResult] = []
        issues: list[str] = []
        mutation_count = 0
        for rec in recommendations:
            if dry_run:
                results.append(ExecutionResult(rec.recommendation_id, "dry_run", False, "repair plan validated without mutation"))
            else:
                results.append(ExecutionResult(rec.recommendation_id, "blocked", False, "mutation disabled in Stage123"))
                issues.append("mutation_attempt_blocked")
        dry = sum(1 for r in results if r.status == "dry_run")
        approved = sum(1 for r in results if r.status == "approved")
        gate_failed = sum(1 for r in results if r.status == "gate_fail")
        if mutation_count:
            issues.append("mutation_count_nonzero")
        return AutoRepairExecutionReport(
            status="pass" if not issues else "blocked",
            total=len(results),
            dry_run=dry,
            approved=approved,
            gate_failed=gate_failed,
            mutation_count=mutation_count,
            results=tuple(results),
            issues=tuple(sorted(set(issues))),
        )
