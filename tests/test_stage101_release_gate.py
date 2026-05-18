from pathlib import Path

from v1700.gates.release_gate import run_release_gate
from v1700.gates.stage101_release_gate import run_stage101_release_gate

ROOT = Path(__file__).resolve().parents[1]


def test_stage101_release_gate_promotes_stage100_without_untraced_v430_merge():
    gate = run_stage101_release_gate(ROOT)
    assert gate["status"] == "pass"
    assert gate["stage100_release_gate"]["status"] == "pass"
    assert gate["v430_untraced_merge"] is False
    assert gate["checks"]["scenario_room_contract_pass"]["status"] == "pass"
    assert gate["checks"]["prop_reveal_cue_pass"]["status"] == "pass"


def test_main_release_gate_includes_stage101_when_active():
    result = run_release_gate()
    assert result["status"] == "pass"
    assert result["stage101_release_gate"]["status"] == "pass"

