from __future__ import annotations

from v1700.longform_adversarial.contracts import AdversarialCase


def build_attention_fatigue_cases() -> tuple[AdversarialCase, ...]:
    return (
        AdversarialCase(
            case_id="ADV-ATT-001",
            case_type="attention_fatigue",
            source_stage="97",
            mutation_type="mid_season_fatigue_spike",
            expected_status="BLOCK",
            expected_block_reason="attention_fatigue_risk_above_threshold",
            episode_count=16,
            payload_path="generated/adversarial/attention/mid_season_fatigue.json",
            invariants={"attention_fatigue_risk": 0.68},
            payload={"attention_fatigue_risk": 0.68, "low_reward_high_cost_count": 0},
        ),
        AdversarialCase(
            case_id="ADV-ATT-002",
            case_type="attention_fatigue",
            source_stage="97",
            mutation_type="high_cognitive_low_reward_accumulation",
            expected_status="BLOCK",
            expected_block_reason="low_reward_high_cost_episode_count_above_threshold",
            episode_count=16,
            payload_path="generated/adversarial/attention/high_cost_low_reward.json",
            invariants={"attention_fatigue_risk": 0.24},
            payload={"attention_fatigue_risk": 0.24, "low_reward_high_cost_count": 4},
        ),
    )
