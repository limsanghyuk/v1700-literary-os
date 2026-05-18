from v1700.gates.stage78_release_gate import run_stage78_release_gate
from v1700.drama_execution import run_drama_execution_smoke


def test_stage78_drama_execution_controls_temporal_pressure_and_branching():
    report = run_drama_execution_smoke()
    assert report["status"] == "pass"
    assert report["temporal_continuity"]["status"] == "pass"
    assert report["emotional_pressure_valve"]["controlled_release"] is True
    assert report["branch_commit_rollback"]["status"] == "pass"
    assert any(branch["rolled_back"] for branch in report["branch_commit_rollback"]["branches"])


def test_stage78_release_gate():
    assert run_stage78_release_gate()["status"] == "pass"
