from __future__ import annotations

from pathlib import Path

from .report import write_json
from .workspace_state import build_workspace_state_report


def persist_workspace_snapshot(path: Path) -> dict:
    payload = build_workspace_state_report()
    write_json(path, payload)
    return {"status": "pass", "snapshot_path": path.as_posix(), "contains_raw_manuscript": False}
