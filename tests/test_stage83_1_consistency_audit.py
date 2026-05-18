
from v1700.gates.stage83_1_release_gate import run_stage83_1_release_gate
from v1700.lineage.stage83_1_consistency_audit import (
    build_branchpoint_model_registry_v2,
    build_commercial_readiness_gap_manifest_v2,
    build_core_logic_survival_matrix_v3,
    build_organic_relation_graph_manifest_v2,
    run_stage83_1_consistency_audit,
)


def test_stage83_1_registry_includes_stage80_to_stage83_branchpoints():
    registry = build_branchpoint_model_registry_v2()
    ids = {bp["branchpoint_id"] for bp in registry["branchpoints"]}
    assert "BP_STAGE80_KOREAN_DRAMA_COMPOSITION_HIERARCHY" in ids
    assert "BP_STAGE81_ACTUAL_TEXT_QUALITY_ENDURANCE" in ids
    assert "BP_STAGE82_BLIND_CRITIC_BENCHMARK" in ids
    assert "BP_STAGE83_COMMERCIAL_LONGFORM_RELEASE_CANDIDATE" in ids


def test_stage83_1_core_logic_matrix_v3_has_no_p0_non_live_entries():
    matrix = build_core_logic_survival_matrix_v3()
    assert matrix["status"] == "pass"
    assert matrix["p0_non_live_logic_ids"] == []
    logic_ids = {entry["logic_id"] for entry in matrix["entries"]}
    assert "korean_drama_composition_hierarchy" in logic_ids
    assert "three_episode_actual_rendering" in logic_ids


def test_stage83_1_commercial_gaps_resolve_stage82_83_pending_statuses():
    gaps = build_commercial_readiness_gap_manifest_v2()
    assert gaps["status"] == "commercial_release_candidate_ready"
    statuses = {item["gap_id"]: item["status"] for item in gaps["items"]}
    assert statuses["external_blind_critic_benchmark"] == "RESOLVED_STAGE82"
    assert statuses["commercial_release_candidate"] == "RESOLVED_STAGE83"
    assert not any(status.startswith("PENDING_STAGE82") or status.startswith("PENDING_STAGE83") for status in statuses.values())


def test_stage83_1_organic_relation_graph_v2_is_current_and_safe():
    graph = build_organic_relation_graph_manifest_v2()
    assert graph["status"] == "pass"
    assert graph["none_edge_count"] == 0
    assert not any("None --" in edge or "--> None" in edge for edge in graph["edge_texts"])
    assert any(rel["target"] == "src/v1700/drama_composition/engine.py" for rel in graph["relations"])
    assert any(rel["source"] == "GraphNexus" and rel["target"] == "BranchpointLogicGraph" for rel in graph["relations"])


def test_stage83_1_consistency_audit_and_release_gate_pass():
    audit = run_stage83_1_consistency_audit()
    assert audit["status"] == "pass"
    assert audit["pending_stage82_83_gap_ids"] == []
    assert audit["provider_default_calls"] == 0
    assert audit["node2_raw_reveal_access_count"] == 0
    gate = run_stage83_1_release_gate()
    assert gate["status"] == "pass"
