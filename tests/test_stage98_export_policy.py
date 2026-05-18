from pathlib import Path

from v1700.studio_workflow.project_ingest import ingest_studio_project
from v1700.studio_workflow.publishing_package import full_text_export_allowed

ROOT = Path(__file__).resolve().parents[1]


def test_stage98_full_text_export_requires_local_mode_and_explicit_non_provider_export():
    feature_only = ingest_studio_project(ROOT)
    local = ingest_studio_project(ROOT, privacy_mode="LOCAL_FULL_TEXT")
    assert full_text_export_allowed(feature_only, explicit_local_export=True, provider_export=False) is False
    assert full_text_export_allowed(local, explicit_local_export=False, provider_export=False) is False
    assert full_text_export_allowed(local, explicit_local_export=True, provider_export=True) is False
    assert full_text_export_allowed(local, explicit_local_export=True, provider_export=False) is True
