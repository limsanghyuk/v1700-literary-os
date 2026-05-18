from pathlib import Path
from v1700.stage104.orchestrator import run_stage104_0_studio_beta_preflight
ROOT = Path(__file__).resolve().parents[1]

def test_stage104_preflight_passes_with_stage103_baseline():
    report = run_stage104_0_studio_beta_preflight(ROOT)
    assert report["status"] == "pass"
    assert report["provider_zero"] is True
