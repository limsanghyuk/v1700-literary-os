from __future__ import annotations

from typing import Any

from .fixtures import project_cim_fixtures


def run_project_local_cim_builder() -> dict[str, Any]:
    snapshots = project_cim_fixtures()
    issues: list[str] = []
    for snapshot in snapshots:
        if snapshot.cross_project_influence_write != 0:
            issues.append(f"cross_project_write:{snapshot.project_id}")
        if snapshot.raw_manuscript_exported:
            issues.append(f"raw_manuscript_exported:{snapshot.project_id}")
    return {
        "status": "pass" if not issues else "blocked",
        "title": "Project-local CIM snapshot builder",
        "project_local_only": True,
        "project_count": len(snapshots),
        "snapshots": [s.to_dict() for s in snapshots],
        "cross_project_influence_write": 0,
        "raw_manuscript_exported": False,
        "issues": issues,
    }
