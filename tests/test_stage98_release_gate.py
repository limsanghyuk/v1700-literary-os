from pathlib import Path

from v1700.gates.release_gate import run_release_gate
from v1700.gates.stage98_release_gate import run_stage98_release_gate

ROOT = Path(__file__).resolve().parents[1]


def test_stage98_release_gate_inherits_stage97_2_and_integrates_main_gate():
    gate = run_stage98_release_gate(ROOT)
    assert gate["status"] == "pass"
    assert gate["stage97_2_release_gate"]["status"] == "pass"
    assert gate["main_release_gate_integration_status"] == "pass"


def test_main_release_gate_includes_stage98_when_active():
    result = run_release_gate()
    assert result["status"] == "pass"
    assert result["stage98_release_gate"]["status"] == "pass"
