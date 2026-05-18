from __future__ import annotations

from pathlib import Path

from v1700.nie.gate25.gate25_nie_v1 import build_gate25_nie_v1_report
from v1700.stage120.orchestrator import run_stage120
from v1700.gates.stage120_release_gate import run_stage120_release_gate


def test_stage120_gate25_report_passes() -> None:
    root = Path(__file__).resolve().parents[1]
    report = build_gate25_nie_v1_report(root)
    assert report["status"] == "pass"
    assert report["gate25_checks"]["provider_zero_pass"] is True
    assert report["gate25_checks"]["nie_adversarial_pack_pass"] is True
    assert report["physics_reward_bridge_llm_call_count"] == 0


def test_stage120_orchestrator_and_release_gate_pass() -> None:
    root = Path(__file__).resolve().parents[1]
    stage = run_stage120(root)
    assert stage["status"] == "pass"
    gate = run_stage120_release_gate(root)
    assert gate["status"] == "pass"
    assert gate["checks"]["release_pack_pass"]["status"] == "pass"
