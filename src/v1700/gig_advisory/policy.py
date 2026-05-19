from __future__ import annotations

from typing import Any

from .contracts import Gate26AdvisoryPolicy


def build_gate26_advisory_policy(classifier: dict[str, Any]) -> dict[str, Any]:
    policy = Gate26AdvisoryPolicy(
        stage="131",
        baseline_stage="130",
        mode="GIG_GATE26_ADVISORY_ONLY",
        hard_block_enabled=False,
        auto_repair_enabled=False,
        canon_auto_resolution_enabled=False,
        writer_approval_required_for_true_contradiction=True,
        provider_default_calls=0,
        live_provider_call_count_in_release_gate=0,
    )
    issues: list[str] = []
    if classifier.get("status") != "pass":
        issues.append("classifier_blocked")
    if policy.hard_block_enabled:
        issues.append("gate26_hard_block_enabled")
    if policy.auto_repair_enabled:
        issues.append("auto_repair_enabled")
    if policy.canon_auto_resolution_enabled:
        issues.append("canon_auto_resolution_enabled")
    if policy.provider_default_calls != 0 or policy.live_provider_call_count_in_release_gate != 0:
        issues.append("provider_calls_nonzero")
    return {
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "policy": policy.to_dict(),
        "advisory_only": True,
        "hard_block_enabled": False,
        "auto_repair_mutation_count": 0,
        "canon_auto_resolution_count": 0,
        "writer_approval_guard": True,
    }
