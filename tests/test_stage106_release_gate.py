from pathlib import Path
from v1700.gates.stage106_release_gate import run_stage106_release_gate

def test_stage106_release_gate_passes():
    report = run_stage106_release_gate(Path(__file__).resolve().parents[1])
    assert report["status"] == "pass"
    assert report["provider_default_calls"] == 0
    assert report["live_provider_call_count_in_release_gate"] == 0
    assert report["raw_manuscript_provider_leakage"] == 0
