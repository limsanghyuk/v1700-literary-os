from pathlib import Path

from v1700.longform_adversarial.adversarial_orchestrator import run_stage97_1_adversarial_validation

ROOT = Path(__file__).resolve().parents[1]


def test_blocks_weak_scene_ratio_above_threshold():
    report = run_stage97_1_adversarial_validation(ROOT)
    result = next(item for item in report["results"] if item["case_id"] == "ADV-SCN-001")
    assert result["actual_status"] == "BLOCK"
    assert result["triggered_gate"] == "scene_necessity"
    assert result["matched_expectation"] is True
