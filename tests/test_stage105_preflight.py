from pathlib import Path
from v1700.stage105.orchestrator import run_stage105_0_creative_arbitration_preflight


def test_stage105_preflight_passes_repo_root():
    root = Path(__file__).resolve().parents[1]
    report = run_stage105_0_creative_arbitration_preflight(root)
    assert report["status"] == "pass"
    assert report["provider_zero"] is True
    assert report["branchpoint_survival_status"] == "pass"
