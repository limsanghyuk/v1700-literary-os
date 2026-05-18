from pathlib import Path
from v1700.stage104.orchestrator import run_stage104_4_sample_project_beta
ROOT = Path(__file__).resolve().parents[1]

def test_sample_project_beta_runs_feature_only_export():
    report = run_stage104_4_sample_project_beta(ROOT)
    assert report["status"] == "pass"
    assert report["export_manifest"]["includes_full_text"] is False
