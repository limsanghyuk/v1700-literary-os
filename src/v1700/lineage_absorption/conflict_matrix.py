from __future__ import annotations

from typing import Any

from v1700.stage121.fixtures import CONFLICT_MATRIX


def build_conflict_matrix() -> dict[str, Any]:
    conflicts = [entry.to_dict() for entry in CONFLICT_MATRIX]
    blockers = [c for c in conflicts if c["severity"] == "blocker"]
    high = [c for c in conflicts if c["severity"] == "high"]
    return {
        "status": "pass",
        "conflict_count": len(conflicts),
        "blocker_count": len(blockers),
        "high_count": len(high),
        "conflicts": conflicts,
        "direct_merge_blocked": bool(blockers),
        "resolution_required_before_absorption": [c["conflict_id"] for c in conflicts if c["severity"] in {"blocker", "high"}],
    }
