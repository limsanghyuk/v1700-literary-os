from __future__ import annotations

from v1700.longform_adversarial.contracts import AdversarialCase


def build_style_drift_violation_cases() -> tuple[AdversarialCase, ...]:
    return (
        AdversarialCase(
            case_id="ADV-VOC-001",
            case_type="style_drift_violation",
            source_stage="97",
            mutation_type="unexplained_style_drift",
            expected_status="BLOCK",
            expected_block_reason="unexplained_style_drift_above_tolerance",
            episode_count=16,
            payload_path="generated/adversarial/voice/unexplained_style_drift.json",
            invariants={"permitted_style_evolution": False},
            payload={"style_drift": 0.37, "permitted_style_evolution": False, "character_voice_collapse": False},
        ),
        AdversarialCase(
            case_id="ADV-VOC-002",
            case_type="style_drift_violation",
            source_stage="97",
            mutation_type="character_voice_collapse",
            expected_status="BLOCK",
            expected_block_reason="character_voice_collapse_detected",
            episode_count=16,
            payload_path="generated/adversarial/voice/character_voice_collapse.json",
            invariants={"permitted_style_evolution": False},
            payload={"style_drift": 0.12, "permitted_style_evolution": False, "character_voice_collapse": True},
        ),
    )
