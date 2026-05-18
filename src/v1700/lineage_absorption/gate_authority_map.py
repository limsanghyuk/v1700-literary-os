from __future__ import annotations

from typing import Any

from v1700.stage121.fixtures import GATE_AUTHORITY_MAP


def build_gate_authority_map() -> dict[str, Any]:
    entries = [entry.to_dict() for entry in GATE_AUTHORITY_MAP]
    primary = [entry for entry in entries if entry["release_mode"] == "PRIMARY"]
    return {
        "status": "pass" if len(primary) == 1 and primary[0]["gate_id"] == "Gate25" else "blocked",
        "entry_count": len(entries),
        "entries": entries,
        "primary_gate": primary[0]["gate_id"] if primary else None,
        "secondary_or_advisory": [e["gate_id"] for e in entries if e["release_mode"] in {"SECONDARY", "ADVISORY"}],
        "future_governor_blocked_until_stage125": any(e["gate_id"] == "Gate25/28/29 Governor" and e["release_mode"] == "BLOCKED" for e in entries),
    }
