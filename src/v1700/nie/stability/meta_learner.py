from __future__ import annotations

from v1700.nie.stability.contracts import MetaLearnerReport


class MetaLearnerSkeleton:
    """Proposal-only MetaLearner adapter.

    Stage122 deliberately absorbs the interface and audit trail only. Runtime
    model learning is blocked until later stages provide frozen datasets and
    adversarial evidence.
    """

    def propose(self, proposals: list[dict]) -> MetaLearnerReport:
        issues: list[str] = []
        runtime_training = False
        provider_calls = 0
        applied_count = 0
        if runtime_training:
            issues.append("runtime_training_performed")
        if provider_calls:
            issues.append("provider_calls_nonzero")
        return MetaLearnerReport(
            status="pass" if not issues else "blocked",
            mode="proposal_only",
            proposal_count=len(proposals),
            applied_count=applied_count,
            provider_calls=provider_calls,
            runtime_training_performed=runtime_training,
            issues=issues,
        )
