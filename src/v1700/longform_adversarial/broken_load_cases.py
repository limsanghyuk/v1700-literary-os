from __future__ import annotations

from v1700.longform_adversarial.contracts import AdversarialCase


def build_broken_load_cases() -> tuple[AdversarialCase, ...]:
    return (
        AdversarialCase(
            case_id="ADV-LOD-001",
            case_type="broken_load",
            source_stage="97",
            mutation_type="mid_season_sag",
            expected_status="BLOCK",
            expected_block_reason="mid_season_sag_risk_above_threshold",
            episode_count=16,
            payload_path="generated/adversarial/load/mid_season_sag.json",
            invariants={"branchpoint_lineage_preserved": True},
            payload={"mid_season_sag_risk": 0.31, "overloaded_episode_count": 0},
        ),
    )
