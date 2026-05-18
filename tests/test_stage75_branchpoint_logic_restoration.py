from v1700.gates.stage75_release_gate import run_stage75_release_gate
from v1700.lineage import build_branchpoint_registry, build_core_logic_survival_matrix, build_missing_required_logic_manifest, build_organic_relation_graph


def test_stage75_registers_p0_branchpoints():
    ids = {bp.branchpoint_id for bp in build_branchpoint_registry()}
    assert "BP_STAGE25_NODE2_REWRITE_ENGINE" in ids
    assert "BP_STAGE39_DRAMA_EXECUTION_ENGINE" in ids
    assert "BP_STAGE50_THREE_EPISODE_ENGINE" in ids
    assert "BP_STAGE56_QUALITY_GATE" in ids
    assert "BP_STAGE57_REFINEMENT_LOOP" in ids
    assert "BP_STAGE60_FINAL_USER_RC" in ids
    assert "BP_V328_DRSE_STACK" in ids


def test_stage75_survival_matrix_truthfully_reports_missing_or_partial():
    matrix = build_core_logic_survival_matrix()
    assert any(e.logic_id == "sequence_scale_planning" for e in matrix)
    missing = build_missing_required_logic_manifest()
    assert missing["missing_or_partial_count"] >= 1
    assert missing["status"] == "known_blockers_registered"


def test_stage75_organic_relation_graph_links_logic_to_gates():
    relations = build_organic_relation_graph()
    assert any(r.relation == "REQUIRES_GATE" and r.target == "stage76_release_gate" for r in relations)
    assert any(r.relation == "BLOCKS_FULL_LITERARY_CLAIM_UNTIL_REABSORBED" for r in relations)


def test_stage75_release_gate_passes_truthfully():
    report = run_stage75_release_gate()
    assert report["status"] == "pass"
    assert report["missing_required_logic_manifest"]["missing_or_partial_count"] >= 1
