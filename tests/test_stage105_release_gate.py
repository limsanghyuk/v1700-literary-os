from pathlib import Path
from v1700.gates.stage105_release_gate import run_stage105_release_gate


def test_stage105_release_gate_passes():
    root = Path(__file__).resolve().parents[1]
    report = run_stage105_release_gate(root)
    assert report["status"] == "pass"
    assert report["provider_default_calls"] == 0
    assert report["live_provider_call_count_in_release_gate"] == 0
    assert report["raw_manuscript_provider_leakage"] == 0
