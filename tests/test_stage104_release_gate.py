from pathlib import Path
from v1700.gates.stage104_release_gate import run_stage104_release_gate
ROOT = Path(__file__).resolve().parents[1]

def test_stage104_release_gate_passes():
    report = run_stage104_release_gate(ROOT)
    assert report["status"] == "pass"
    assert report["provider_default_calls"] == 0
    assert report["raw_manuscript_provider_leakage"] == 0
