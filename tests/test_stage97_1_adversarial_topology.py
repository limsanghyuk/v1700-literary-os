from pathlib import Path

from v1700.longform_adversarial.adversarial_orchestrator import run_stage97_1_adversarial_validation

ROOT = Path(__file__).resolve().parents[1]


def _result(report: dict, case_id: str) -> dict:
    return next(item for item in report["results"] if item["case_id"] == case_id)


def test_blocks_orphan_microplot():
    report = run_stage97_1_adversarial_validation(ROOT)
    result = _result(report, "ADV-TOP-001")
    assert result["actual_status"] == "BLOCK"
    assert result["block_reason"] == "orphan_microplot_detected"
    assert result["matched_expectation"] is True
