from __future__ import annotations

import json
from pathlib import Path


def replay_provider_live_call_boundary(root: Path) -> dict:
    reports = [
        root / "release" / "current" / "stage97_2_provider_runtime_report.json",
        root / "release" / "current" / "stage98_studio_workflow_report.json",
        root / "release" / "current" / "stage98_release_gate_report.json",
    ]
    live_calls = 0
    default_calls = 0
    inspected: list[str] = []
    for path in reports:
        if not path.exists():
            continue
        payload = json.loads(path.read_text(encoding="utf-8"))
        inspected.append(path.relative_to(root).as_posix())
        live_calls += int(payload.get("live_provider_call_count", payload.get("provider_live_call_count_in_release", 0)) or 0)
        default_calls += int(payload.get("provider_default_calls", 0) or 0)
    return {
        "status": "pass" if live_calls == 0 and default_calls == 0 else "blocked",
        "provider_live_call_count_in_release": live_calls,
        "provider_default_calls": default_calls,
        "release_mode_provider": "fixture/mock only",
        "inspected_reports": inspected,
    }
