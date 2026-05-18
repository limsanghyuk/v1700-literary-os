from pathlib import Path
from v1700.stage109.orchestrator import run_stage109
from v1700.gates.stage109_release_gate import run_stage109_release_gate


def test_stage109_orchestrator_passes_repo_root():
    root = Path(__file__).resolve().parents[1]
    result = run_stage109(root)
    assert result["status"] == "pass"
    assert result["plugins_enabled_by_default"] == 0
    assert result["plugin_raw_manuscript_access_count"] == 0


def test_stage109_release_gate_passes_repo_root():
    root = Path(__file__).resolve().parents[1]
    result = run_stage109_release_gate(root)
    assert result["status"] == "pass"
    assert result["live_provider_call_count_in_release_gate"] == 0
    assert result["raw_manuscript_provider_leakage"] == 0
