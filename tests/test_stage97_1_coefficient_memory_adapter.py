from pathlib import Path

from v1700.longform_adversarial.coefficient_memory_adapter import load_stage96_coefficient_bridge

ROOT = Path(__file__).resolve().parents[1]


def test_stage96_coefficient_memory_adapter_injects_local_thresholds():
    report = load_stage96_coefficient_bridge(ROOT)
    config = report["config"]
    assert report["status"] == "pass"
    assert config["privacy_mode"] == "LOCAL_ONLY"
    assert config["agency_floor"] >= 0.55
    assert config["payoff_default_threshold"] == 0.0
