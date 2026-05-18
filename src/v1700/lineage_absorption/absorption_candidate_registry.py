from __future__ import annotations

from typing import Any

from v1700.stage121.fixtures import ABSORPTION_CANDIDATES


def build_absorption_candidate_registry() -> dict[str, Any]:
    candidates = [c.to_dict() for c in ABSORPTION_CANDIDATES]
    return {
        "status": "pass",
        "candidate_count": len(candidates),
        "candidates": candidates,
        "target_stages": sorted({c["target_stage"] for c in candidates}),
        "direct_trunk_mutations_allowed": False,
    }
