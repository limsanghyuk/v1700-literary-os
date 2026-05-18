from pathlib import Path

from v1700.stage101.orchestrator import run_stage101_1_scenario_room_contract

ROOT = Path(__file__).resolve().parents[1]


def test_stage101_scenario_room_contract_preserves_boundaries():
    report = run_stage101_1_scenario_room_contract(ROOT)
    assert report["status"] == "pass"
    assert report["scenario_room_contract_status"] == "pass"
    assert report["provider_call_count"] == 0
    assert report["node2_raw_reveal_access"] == 0
    assert report["raw_manuscript_provider_leakage"] == 0

