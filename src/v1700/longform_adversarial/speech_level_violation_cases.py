from __future__ import annotations

from v1700.longform_adversarial.contracts import AdversarialCase


def build_speech_level_violation_cases() -> tuple[AdversarialCase, ...]:
    return (
        AdversarialCase(
            case_id="ADV-DLG-001",
            case_type="speech_level_violation",
            source_stage="97",
            mutation_type="unmotivated_honorific_shift",
            expected_status="BLOCK",
            expected_block_reason="speech_level_inconsistency_above_threshold",
            episode_count=16,
            payload_path="generated/adversarial/dialogue/unmotivated_honorific_shift.json",
            invariants={"korean_dialogue_pragmatics": True},
            payload={"speech_level_inconsistency_count": 4, "explanatory_dialogue_ratio": 0.12},
        ),
        AdversarialCase(
            case_id="ADV-DLG-002",
            case_type="speech_level_violation",
            source_stage="97",
            mutation_type="explanatory_dialogue_overload",
            expected_status="BLOCK",
            expected_block_reason="explanatory_dialogue_ratio_above_threshold",
            episode_count=16,
            payload_path="generated/adversarial/dialogue/explanatory_dialogue_overload.json",
            invariants={"korean_dialogue_pragmatics": True},
            payload={"speech_level_inconsistency_count": 0, "explanatory_dialogue_ratio": 0.41},
        ),
    )
