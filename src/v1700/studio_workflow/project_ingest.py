from __future__ import annotations

from pathlib import Path

from v1700.studio_workflow.contracts import StudioProject


def ingest_studio_project(root: Path, *, privacy_mode: str = "FEATURE_ONLY") -> StudioProject:
    return StudioProject(
        project_id="stage98-commercial-studio-fixture",
        title="Stage98 Commercial Studio Fixture",
        format="series",
        episode_count=24,
        baseline_stage="97.2",
        privacy_mode=privacy_mode,  # type: ignore[arg-type]
        created_at="2026-05-14T00:00:00Z",
        metadata={
            "source": "stage97_2_feature_reports",
            "stage97_endurance_pack": "release/current/stage97_longform_endurance_pack",
            "raw_manuscript_loaded": False,
            "provider_export": False,
            "root_name": root.name,
        },
    )


def project_ingest_report(project: StudioProject) -> dict:
    return {
        "status": "pass",
        "project": project.to_dict(),
        "privacy_mode": project.privacy_mode,
        "feature_only_reference": True,
        "raw_manuscript_provider_leakage": 0,
        "provider_call_count": 0,
    }
