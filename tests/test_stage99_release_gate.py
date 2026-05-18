from pathlib import Path

from v1700.gates.release_gate import run_release_gate
from v1700.gates.stage99_release_gate import run_stage99_release_gate

ROOT = Path(__file__).resolve().parents[1]


def test_stage99_release_gate_inherits_stage98_and_checks_hardening():
    gate = run_stage99_release_gate(ROOT)
    assert gate["status"] == "pass"
    assert gate["stage98_release_gate"]["status"] == "pass"
    assert gate["gitnexus_impact_status"] == "pass"
    assert gate["credential_leakage"] == 0
    assert gate["raw_manuscript_provider_leakage"] == 0
    assert gate["stage100_readiness_status"] == "pass"


def test_main_release_gate_includes_stage99_when_active():
    result = run_release_gate()
    assert result["status"] == "pass"
    assert result["stage99_release_gate"]["status"] == "pass"
