from v1700.quality_endurance import QualityEnduranceEngine, QualityEnduranceGate


def test_quality_endurance_renders_30_actual_scenes_and_improves_quality():
    report = QualityEnduranceEngine().run("제도와 추방과 귀환의 한국 드라마", scene_limit=30)
    assert report.status == "pass"
    assert report.scene_count == 30
    assert report.average_after >= 8.0
    assert report.average_delta >= 0.5
    assert report.blocker_count_after == 0
    assert report.reveal_leakage_count == 0


def test_quality_endurance_gate_passes():
    result = QualityEnduranceGate().validate()
    assert result["status"] == "pass"
    assert result["quality_endurance_report"]["scene_count"] >= 30
