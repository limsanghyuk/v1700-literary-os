from __future__ import annotations

from pathlib import Path

from v1700.longform import run_longform_execution_smoke


def run_longform_execution_gate(root: Path | None = None) -> dict:
    report = run_longform_execution_smoke()
    issues = list(report.get("issues", []))
    if report.get("status") != "pass":
        issues.append("longform_smoke_blocked")
    if len(report.get("plan", {}).get("episodes", [])) != 3:
        issues.append("three_episode_structure_missing")
    if not report.get("rendered"):
        issues.append("rendered_scene_missing")
    if report.get("provider_default_calls") != 0:
        issues.append("provider_default_calls_nonzero")
    if report.get("node2_raw_reveal_access_count") != 0:
        issues.append("node2_raw_reveal_access_nonzero")
    return {
        "stage": "74",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "longform_smoke": report,
        "provider_default_calls": report.get("provider_default_calls", 0),
        "node2_raw_reveal_access_count": report.get("node2_raw_reveal_access_count", 0),
    }
