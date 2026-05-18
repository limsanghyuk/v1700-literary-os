from __future__ import annotations

from v1700.longform_adversarial.contracts import AdversarialCase


def build_weak_scene_cases() -> tuple[AdversarialCase, ...]:
    return (
        AdversarialCase(
            case_id="ADV-SCN-001",
            case_type="weak_scene",
            source_stage="97",
            mutation_type="changed_dimensions_below_floor",
            expected_status="BLOCK",
            expected_block_reason="weak_scene_ratio_above_threshold",
            episode_count=16,
            payload_path="generated/adversarial/scene/weak_scene_ratio.json",
            invariants={"scene_necessity_floor": 0.92},
            payload={"weak_scene_ratio": 0.19, "atmosphere_scene_without_function": False},
        ),
        AdversarialCase(
            case_id="ADV-SCN-002",
            case_type="weak_scene",
            source_stage="97",
            mutation_type="atmosphere_scene_function_missing",
            expected_status="BLOCK",
            expected_block_reason="atmosphere_scene_function_label_missing",
            episode_count=16,
            payload_path="generated/adversarial/scene/atmosphere_unlabeled.json",
            invariants={"scene_necessity_floor": 0.92},
            payload={"weak_scene_ratio": 0.0, "atmosphere_scene_without_function": True},
        ),
    )
