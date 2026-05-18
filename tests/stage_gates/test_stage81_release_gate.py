from v1700.gates.stage81_release_gate import run_stage81_release_gate


def test_stage81_release_gate_passes_and_reports_actual_quality_endurance():
    result = run_stage81_release_gate()
    assert result["status"] == "pass"
    assert result["actual_rendered_scene_count"] >= 30
    assert result["average_quality_after"] >= 8.0
    assert result["average_quality_delta"] >= 0.5
    assert result["provider_default_calls"] == 0
    assert result["node2_raw_reveal_access_count"] == 0
