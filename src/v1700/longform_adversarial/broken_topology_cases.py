from __future__ import annotations

from v1700.longform_adversarial.contracts import AdversarialCase


def build_broken_topology_cases() -> tuple[AdversarialCase, ...]:
    return (
        AdversarialCase(
            case_id="ADV-TOP-001",
            case_type="broken_topology",
            source_stage="97",
            mutation_type="orphan_microplot",
            expected_status="BLOCK",
            expected_block_reason="orphan_microplot_detected",
            episode_count=16,
            payload_path="generated/adversarial/topology/orphan_microplot.json",
            invariants={"branchpoint_lineage_preserved": True},
            payload={"orphan_microplot_count": 1, "episode_function_coverage": 1.0},
        ),
        AdversarialCase(
            case_id="ADV-TOP-002",
            case_type="broken_topology",
            source_stage="97",
            mutation_type="episode_function_coverage_missing",
            expected_status="BLOCK",
            expected_block_reason="episode_function_coverage_incomplete",
            episode_count=16,
            payload_path="generated/adversarial/topology/missing_episode_function.json",
            invariants={"branchpoint_lineage_preserved": True},
            payload={"orphan_microplot_count": 0, "episode_function_coverage": 0.938},
        ),
    )
