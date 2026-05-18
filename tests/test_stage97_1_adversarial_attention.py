from pathlib import Path

from v1700.longform_adversarial.adversarial_orchestrator import run_stage97_1_adversarial_validation

ROOT = Path(__file__).resolve().parents[1]


def test_blocks_attention_fatigue_spike():
    report = run_stage97_1_adversarial_validation(ROOT)
    result = next(item for item in report["results"] if item["case_id"] == "ADV-ATT-001")
    assert result["actual_status"] == "BLOCK"
    assert result["block_reason"] == "attention_fatigue_risk_above_threshold"
    assert result["matched_expectation"] is True
