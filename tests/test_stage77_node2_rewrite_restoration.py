from v1700.gates.stage77_release_gate import run_stage77_release_gate
from v1700.nodes.node2_prose_renderer.rewrite_orchestrator import run_node2_rewrite_restoration_smoke


def test_stage77_node2_rewrite_has_candidates_and_reader_chain_eval():
    report = run_node2_rewrite_restoration_smoke()
    assert report["status"] == "pass"
    assert report["rewrite"]["candidate_count"] >= 3
    assert report["rewrite"]["authority_guard"]["raw_reveal_access"] == 0
    assert report["reader_chain_evaluation"]["scores"]["anti_llm"] >= 8.0
    assert report["reader_chain_evaluation"]["scores"]["reveal_break"] == 10.0


def test_stage77_release_gate():
    assert run_stage77_release_gate()["status"] == "pass"
