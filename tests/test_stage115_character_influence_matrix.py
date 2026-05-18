from pathlib import Path

from v1700.gates.stage115_release_gate import run_stage115_release_gate
from v1700.nie.characters.character_influence_matrix import CharacterInfluenceMatrix
from v1700.nie.characters.cim_report import build_stage115_cim_report, build_stage115_fixture_observations
from v1700.nie.characters.structural_balance import compute_triangle_tension
from v1700.stage115.orchestrator import run_stage115


def test_cim_builds_asymmetric_matrix_and_high_tension_triangle() -> None:
    matrix = CharacterInfluenceMatrix(("minjun", "sujin", "haewon", "chairman", "detective"))
    matrix.update(build_stage115_fixture_observations())
    assert matrix.get_influence("minjun", "sujin") != matrix.get_influence("sujin", "minjun")
    assert matrix.asymmetric_pair_count() >= 4
    assert len(matrix.all_triangles()) >= 4
    assert matrix.high_tension_triangles()


def test_structural_balance_returns_blocking_tension_for_unbalanced_triangle() -> None:
    tri = compute_triangle_tension("A", "B", "C", 0.8, 0.7, -0.5)
    assert tri.balance == -1
    assert tri.tension == 2


def test_cim_centrality_assigns_janggi_role_tiers() -> None:
    report = build_stage115_cim_report()
    assert report["status"] == "pass"
    centrality = report["character_influence_matrix"]["centrality"]
    assert abs(sum(centrality["pagerank"].values()) - 1.0) < 0.0001
    assert "jang" in set(centrality["role_tiers"].values())
    assert set(centrality["role_tiers"]) == set(report["character_influence_matrix"]["characters"])


def test_stage115_orchestrator_and_release_gate_pass() -> None:
    root = Path(__file__).resolve().parents[1]
    stage = run_stage115(root)
    assert stage["status"] == "pass"
    gate = run_stage115_release_gate(root)
    assert gate["status"] == "pass"
    assert gate["checks"]["cim_asymmetric_matrix_pass"]["status"] == "pass"
    assert gate["checks"]["role_tier_assignment_pass"]["status"] == "pass"
