from pathlib import Path

from v1700.gates.stage103_release_gate import run_stage103_release_gate
from v1700.stage103.orchestrator import run_stage103


def test_stage103_orchestrator_preserves_boundaries():
    root = Path(__file__).resolve().parents[1]
    result = run_stage103(root)
    assert result["status"] == "pass"
    assert result["provider_default_calls"] == 0
    assert result["live_provider_call_count_in_release_gate"] == 0
    assert result["raw_manuscript_provider_leakage"] == 0
    assert result["node2_raw_reveal_access"] == 0


def test_stage103_release_gate_passes():
    root = Path(__file__).resolve().parents[1]
    result = run_stage103_release_gate(root)
    assert result["status"] == "pass"
    assert result["checks"]["install_replay_pass"]["status"] == "pass"
    assert result["checks"]["runtime_profile_separation_pass"]["status"] == "pass"
    assert result["checks"]["raw_manuscript_leakage_pass"]["status"] == "pass"
