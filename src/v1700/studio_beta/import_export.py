from __future__ import annotations

from pathlib import Path

from .contracts import StudioBetaExportManifest
from .persistence import persist_workspace_snapshot
from .report import write_summary


def build_studio_beta_export(root: Path) -> dict:
    pack = root / "release" / "current" / "stage104_studio_beta_pack"
    pack.mkdir(parents=True, exist_ok=True)
    snapshot_path = pack / "workspace_snapshot.json"
    persist_workspace_snapshot(snapshot_path)
    handoff_path = pack / "writer_handoff_beta.md"
    write_summary(handoff_path, "Stage104 Writer Handoff Beta", [
        "Open the sample project in local-first workspace mode.",
        "Review prose and scenario boards separately.",
        "Apply only writer-approved revisions.",
        "Export feature-only reports by default.",
    ])
    manifest = StudioBetaExportManifest(
        status="pass",
        export_id="stage104-beta-export-001",
        project_id="stage104_sample_project",
        includes_full_text=False,
        includes_feature_reports=True,
        includes_release_evidence=True,
        workspace_snapshot_path=snapshot_path.relative_to(root).as_posix(),
        writer_handoff_path=handoff_path.relative_to(root).as_posix(),
    )
    return manifest.to_dict()
