from __future__ import annotations

from typing import Any

from v1700.nie.characters.character_influence_matrix import CharacterInfluenceMatrix
from v1700.nie.characters.contracts import InfluenceObservation


def build_stage115_fixture_observations() -> tuple[InfluenceObservation, ...]:
    scene = "stage115_fixture_scene_001"
    return (
        InfluenceObservation("minjun", "sujin", 0.72, "protagonist protects confidante", scene),
        InfluenceObservation("sujin", "minjun", 0.41, "confidante restores protagonist resolve", scene),
        InfluenceObservation("chairman", "minjun", -0.82, "antagonist applies succession pressure", scene),
        InfluenceObservation("minjun", "chairman", -0.36, "protagonist resists authority", scene),
        InfluenceObservation("haewon", "sujin", -0.64, "rival withholds critical evidence", scene),
        InfluenceObservation("sujin", "haewon", -0.22, "confidante confronts rival", scene),
        InfluenceObservation("detective", "minjun", 0.31, "outsider validates hidden clue", scene),
        InfluenceObservation("haewon", "detective", -0.58, "secret keeper misleads investigator", scene),
        InfluenceObservation("detective", "chairman", -0.44, "investigator threatens concealed power", scene),
        InfluenceObservation("chairman", "haewon", 0.39, "antagonist rewards secret keeper", scene),
    )


def build_stage115_cim_report() -> dict[str, Any]:
    characters = ("minjun", "sujin", "haewon", "chairman", "detective")
    matrix = CharacterInfluenceMatrix(characters)
    observations = build_stage115_fixture_observations()
    matrix.update(observations)
    data = matrix.to_dict()
    role_tiers = data["centrality"]["role_tiers"]
    issues: list[str] = []
    if data["asymmetric_pair_count"] < 4:
        issues.append("insufficient_asymmetric_pairs")
    if data["triangle_count"] < 4:
        issues.append("insufficient_triangle_coverage")
    if data["high_tension_triangle_count"] < 1:
        issues.append("no_high_tension_triangle_detected")
    if "jang" not in set(role_tiers.values()):
        issues.append("no_jang_role_tier_assigned")
    if not all(char in role_tiers for char in characters):
        issues.append("role_tier_missing_character")
    return {
        "stage": "115",
        "baseline_stage": "114",
        "title": "CharacterInfluenceMatrix + Structural Balance",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "scene_id": "stage115_fixture_scene_001",
        "observations": [obs.to_dict() for obs in observations],
        "character_influence_matrix": data,
        "provider_call_count": 0,
        "physics_reward_bridge_llm_call_count": 0,
        "node2_raw_reveal_access": 0,
        "raw_manuscript_provider_leakage": 0,
        "credential_leakage": 0,
        "branchpoint_lineage_preserved": not issues,
    }
