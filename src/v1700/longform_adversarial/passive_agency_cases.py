from __future__ import annotations

from v1700.longform_adversarial.contracts import AdversarialCase


def build_passive_agency_cases() -> tuple[AdversarialCase, ...]:
    return (
        AdversarialCase(
            case_id="ADV-AGY-001",
            case_type="passive_agency",
            source_stage="97",
            mutation_type="protagonist_passive_episode_chain",
            expected_status="BLOCK",
            expected_block_reason="passive_protagonist_arc_detected",
            episode_count=16,
            payload_path="generated/adversarial/agency/passive_protagonist.json",
            invariants={"protagonist_agency_floor": 0.31},
            payload={"protagonist_agency_floor": 0.31, "passive_episode_count": 5, "antagonist_agency_only": False},
        ),
        AdversarialCase(
            case_id="ADV-AGY-002",
            case_type="passive_agency",
            source_stage="97",
            mutation_type="antagonist_only_agency_rise",
            expected_status="BLOCK",
            expected_block_reason="protagonist_agency_collapse_against_antagonist",
            episode_count=16,
            payload_path="generated/adversarial/agency/antagonist_only_agency.json",
            invariants={"protagonist_agency_floor": 0.39},
            payload={"protagonist_agency_floor": 0.39, "passive_episode_count": 3, "antagonist_agency_only": True},
        ),
    )
