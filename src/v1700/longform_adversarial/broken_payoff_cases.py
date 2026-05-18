from __future__ import annotations

from v1700.longform_adversarial.contracts import AdversarialCase


def build_broken_payoff_cases() -> tuple[AdversarialCase, ...]:
    return (
        AdversarialCase(
            case_id="ADV-PAY-001",
            case_type="broken_payoff",
            source_stage="97",
            mutation_type="critical_payoff_debt_default",
            expected_status="BLOCK",
            expected_block_reason="critical_payoff_debt_defaulted",
            episode_count=16,
            payload_path="generated/adversarial/payoff/defaulted_critical_debt.json",
            invariants={"critical_payoff_debt_default": 1},
            payload={"critical_debt_default_count": 1, "finale_new_critical_debt_count": 0},
        ),
        AdversarialCase(
            case_id="ADV-PAY-002",
            case_type="broken_payoff",
            source_stage="97",
            mutation_type="finale_new_critical_debt",
            expected_status="BLOCK",
            expected_block_reason="finale_new_critical_debt_created",
            episode_count=16,
            payload_path="generated/adversarial/payoff/finale_new_critical_debt.json",
            invariants={"critical_payoff_debt_default": 0},
            payload={"critical_debt_default_count": 0, "finale_new_critical_debt_count": 1},
        ),
    )
