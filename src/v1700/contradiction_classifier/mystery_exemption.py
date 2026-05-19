from __future__ import annotations

from typing import Any


def audit_mystery_exemptions(classifier_matrix: dict[str, Any]) -> dict[str, Any]:
    classifications = classifier_matrix.get("classifications", [])
    evidence_by_id = {item["case_id"]: item for item in classifier_matrix.get("evidence", [])}
    issues: list[str] = []
    for result in classifications:
        evidence = evidence_by_id.get(result["case_id"], {})
        if result["classification"] == "true_contradiction" and result["exemption_status"] != "not_exempted":
            issues.append(f"true_contradiction_exempted:{result['case_id']}")
        if result["classification"] == "intentional_mystery":
            if not evidence.get("reveal_lock_id"):
                issues.append(f"mystery_without_reveal_lock:{result['case_id']}")
            if not evidence.get("payoff_budget_reserved"):
                issues.append(f"mystery_without_payoff_budget:{result['case_id']}")
        if result["classification"] == "reveal_delay":
            if not evidence.get("scheduled_reveal_episode"):
                issues.append(f"reveal_delay_without_schedule:{result['case_id']}")
            if not evidence.get("payoff_budget_reserved"):
                issues.append(f"reveal_delay_without_payoff_budget:{result['case_id']}")
        if result.get("hard_block_allowed") or result.get("canon_auto_resolution_allowed") or result.get("auto_repair_allowed"):
            issues.append(f"unsafe_action_enabled:{result['case_id']}")
    return {
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "mystery_exemption_policy": "requires_reveal_lock_and_payoff_budget",
        "true_contradiction_policy": "writer_review_required_no_exemption",
        "safe_exemption_types": [
            "intentional_mystery",
            "character_misunderstanding",
            "reveal_delay",
        ],
        "unsafe_actions_enabled": 0 if not any(
            r.get("hard_block_allowed") or r.get("canon_auto_resolution_allowed") or r.get("auto_repair_allowed")
            for r in classifications
        ) else 1,
    }
