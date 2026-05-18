from __future__ import annotations

from pathlib import Path

from v1700.gates.stage94_release_gate import run_stage94_release_gate
from v1700.narrative_physics.engine import run_stage95_narrative_physics_smoke

_STAGE95_CACHE: dict[str, dict] = {}


def _project_root() -> Path:
    return Path(__file__).resolve().parents[3]


def run_stage95_release_gate(root: Path | None = None) -> dict:
    root = root or _project_root()
    cache_key = str(root.resolve())
    if cache_key in _STAGE95_CACHE:
        return _STAGE95_CACHE[cache_key]

    stage94 = run_stage94_release_gate(root)
    physics = run_stage95_narrative_physics_smoke()
    checks = {
        "stage94_release_gate": stage94,
        "stage95_narrative_physics_smoke": physics,
    }
    issues = [name for name, report in checks.items() if report.get("status") != "pass"]
    if physics.get("provider_default_calls") != 0:
        issues.append("provider_default_calls_not_zero")
    if physics.get("live_provider_call_count") != 0:
        issues.append("live_provider_call_count_not_zero")
    if physics.get("node2_raw_reveal_access_count") != 0:
        issues.append("node2_raw_reveal_access_not_zero")
    surface = physics.get("surface_guard", {})
    if surface.get("reader_only_leakage_count") != 0:
        issues.append("reader_only_leakage_not_zero")
    if surface.get("internal_marker_leakage_count") != 0:
        issues.append("internal_marker_leakage_not_zero")
    if physics.get("branchpoint_survival", {}).get("status") != "pass":
        issues.append("branchpoint_survival_blocked")

    result = {
        "stage": "95",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "claim": "Stage95 introduces the V1700 Native Narrative Physics Engine before provider ensemble arbitration.",
        "checks": checks,
        "provider_default_calls": 0,
        "live_provider_call_count": 0,
        "node2_raw_reveal_access_count": physics.get("node2_raw_reveal_access_count", 0),
    }
    _STAGE95_CACHE[cache_key] = result
    return result
