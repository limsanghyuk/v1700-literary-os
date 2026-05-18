from pathlib import Path

from v1700.gates.release_gate import run_release_gate
from v1700.gates.stage97_2_release_gate import run_stage97_2_release_gate
from v1700.stage97_2.orchestrator import run_stage97_2_provider_runtime_smoke

ROOT = Path(__file__).resolve().parents[1]


def test_stage97_2_provider_runtime_smoke_preserves_provider_zero():
    report = run_stage97_2_provider_runtime_smoke(ROOT)
    assert report["status"] == "pass"
    assert report["task_router_llm0_status"] == "pass"
    assert report["live_provider_call_count"] == 0
    assert report["raw_manuscript_provider_leakage"] == 0


def test_stage97_2_release_gate_inherits_stage97_1():
    gate = run_stage97_2_release_gate(ROOT)
    assert gate["status"] == "pass"
    assert gate["checks"]["stage97_1_baseline_gate"]["status"] == "pass"
    assert gate["provider_default_calls"] == 0


def test_main_release_gate_includes_stage97_2_when_active():
    result = run_release_gate()
    assert result["status"] == "pass"
    assert result["stage97_2_release_gate"]["status"] == "pass"
