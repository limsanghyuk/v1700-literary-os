from pathlib import Path

from v1700.studio_workflow.studio_orchestrator import run_stage98_studio_workflow

ROOT = Path(__file__).resolve().parents[1]


def test_stage98_studio_orchestrator_writes_feature_only_reports():
    report = run_stage98_studio_workflow(ROOT)
    assert report["status"] == "pass"
    assert report["provider_call_count"] == 0
    assert report["raw_manuscript_provider_leakage"] == 0
    assert report["full_text_exported"] is False
    assert (ROOT / "release/current/stage98_studio_workflow_report.json").exists()
