from pathlib import Path

from v1700.studio_workflow.project_ingest import ingest_studio_project, project_ingest_report

ROOT = Path(__file__).resolve().parents[1]


def test_stage98_project_ingest_uses_feature_only_privacy():
    project = ingest_studio_project(ROOT)
    report = project_ingest_report(project)
    assert project.baseline_stage == "97.2"
    assert project.privacy_mode == "FEATURE_ONLY"
    assert report["raw_manuscript_provider_leakage"] == 0
    assert report["provider_call_count"] == 0
