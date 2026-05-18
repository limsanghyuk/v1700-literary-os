from v1700.nie.nil import build_stage118_nil_orchestrator_report
from v1700.stage118.orchestrator import run_stage118
from v1700.gates.stage118_release_gate import run_stage118_release_gate


def test_nil_orchestrator_composes_required_components() -> None:
    report = build_stage118_nil_orchestrator_report()
    assert report["status"] == "pass"
    assert [component["name"] for component in report["components"]] == [
        "reward_bridge",
        "adaptive_momentum_weights",
        "character_influence_matrix",
        "domain_rag_fusion",
        "narrative_tension_curve",
    ]
    assert report["convergence"]["loop_closure_status"] == "pass"


def test_nil_invariants_are_zero() -> None:
    report = build_stage118_nil_orchestrator_report()
    assert all(value == 0 for value in report["invariant_counts"].values())
    assert report["physics_reward_bridge_llm_call_count"] == 0
    assert report["mae_live_provider_call_count"] == 0


def test_stage118_orchestrator_and_gate_on_repo_root() -> None:
    stage = run_stage118()
    assert stage["status"] == "pass"
    gate = run_stage118_release_gate()
    assert gate["status"] == "pass"
    assert gate["checks"]["nil_loop_closure_pass"]["status"] == "pass"
    assert gate["checks"]["nil_invariant_counts_zero_pass"]["status"] == "pass"
