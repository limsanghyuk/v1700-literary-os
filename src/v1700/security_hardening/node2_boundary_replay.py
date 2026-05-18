from __future__ import annotations

import json
from pathlib import Path


def replay_node2_boundary(root: Path) -> dict:
    candidates = [
        root / "release" / "current" / "stage72_node2_prose_compiler_report.json",
        root / "release" / "current" / "stage98_studio_workflow_report.json",
        root / "release" / "current" / "stage98_release_gate_report.json",
    ]
    raw_access = 0
    inspected: list[str] = []
    for path in candidates:
        if not path.exists():
            continue
        payload = json.loads(path.read_text(encoding="utf-8"))
        inspected.append(path.relative_to(root).as_posix())
        raw_access += int(payload.get("node2_raw_reveal_access", 0) or 0)
    return {
        "status": "pass" if raw_access == 0 else "blocked",
        "node2_raw_reveal_access": raw_access,
        "surface_only_node2": raw_access == 0,
        "inspected_reports": inspected,
    }
