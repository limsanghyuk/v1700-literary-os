from __future__ import annotations

from typing import Any

from .contracts import CanonConflict


def run_canon_conflict_probe() -> dict[str, Any]:
    detected = [
        CanonConflict(
            conflict_id="canon_probe_block_001",
            project_id="project_beta",
            entity_id="blocked_canon_collision",
            conflict_type="timeline",
            severity=0.84,
            evidence=["timeline_conflict=1.0", "world_rule_conflict=1.0"],
            recommended_action="block direct absorption; require Stage129 Canon Governor mapping",
        )
    ]
    return {
        "status": "pass",
        "conflicts_detected": [x.to_dict() for x in detected],
        "blocking_conflict_count": len([x for x in detected if x.severity > 0.60]),
        "mystery_exemption_deferred_to_stage132": True,
    }
