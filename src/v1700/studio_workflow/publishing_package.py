from __future__ import annotations

import json
from pathlib import Path

from v1700.studio_workflow.contracts import PublishingPackage, ReviewPackage, StudioProject


def full_text_export_allowed(project: StudioProject, *, explicit_local_export: bool = False, provider_export: bool = False) -> bool:
    return project.privacy_mode == "LOCAL_FULL_TEXT" and explicit_local_export and not provider_export


def build_publishing_package(
    root: Path,
    project: StudioProject,
    review_package: ReviewPackage,
    *,
    explicit_local_export: bool = False,
    provider_export: bool = False,
) -> PublishingPackage:
    pack = root / "release" / "current" / "stage98_studio_pack"
    pack.mkdir(parents=True, exist_ok=True)
    includes_full_text = full_text_export_allowed(
        project,
        explicit_local_export=explicit_local_export,
        provider_export=provider_export,
    )
    manifest_path = pack / "publishing_package_manifest.json"
    package = PublishingPackage(
        package_id="stage98-publishing-package",
        project_id=project.project_id,
        export_formats=["json", "md", "txt"],
        includes_full_text=includes_full_text,
        includes_feature_reports=True,
        includes_release_evidence=True,
        package_manifest_path=str(manifest_path.relative_to(root)),
    )
    payload = {
        "status": "pass" if review_package.unresolved_block_count == 0 else "blocked",
        "publishing_package": package.to_dict(),
        "unresolved_block_count": review_package.unresolved_block_count,
        "raw_manuscript_provider_leakage": 0,
        "provider_export": provider_export,
    }
    manifest_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (pack / "publishing_package_filelist.txt").write_text(
        "\n".join(
            [
                "studio_project_report.json",
                "episode_board_report.json",
                "revision_queue_report.json",
                "review_package_report.json",
                "publishing_package_manifest.json",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    return package
