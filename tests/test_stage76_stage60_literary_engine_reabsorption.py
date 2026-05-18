from v1700.gates.stage76_release_gate import run_stage76_release_gate
from v1700.reabsorption import run_stage60_reabsorption_smoke


def test_stage76_reabsorbs_stage50_scale_and_stage56_57_quality():
    report = run_stage60_reabsorption_smoke()
    assert report["status"] == "pass"
    assert report["stage50_scale_plan"]["episode_count"] == 3
    assert report["stage50_scale_plan"]["sequence_count_total"] >= 29
    assert report["stage50_scale_plan"]["scene_count_total"] >= 532
    assert len(report["stage56_quality_gate"]["axis_scores"]) == 10
    assert report["stage57_refinement_loop"]["quality_delta"] >= 1.0
    assert report["stage57_refinement_loop"]["blocker_axis_count_after"] == 0


def test_stage76_release_gate():
    assert run_stage76_release_gate()["status"] == "pass"
