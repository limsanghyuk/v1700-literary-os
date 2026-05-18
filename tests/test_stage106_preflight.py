from pathlib import Path
from v1700.stage106.orchestrator import run_stage106_0_author_profile_preflight

def test_stage106_preflight_passes():
    report = run_stage106_0_author_profile_preflight(Path(__file__).resolve().parents[1])
    assert report["status"] == "pass"
    assert report["provider_zero"] is True
