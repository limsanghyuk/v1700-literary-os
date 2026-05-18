from __future__ import annotations

from pathlib import Path

from .handoff_export import write_beta_handoff
from .local_telemetry import build_local_telemetry_report


def build_beta_handoff_report(root: Path) -> dict:
    handoff = write_beta_handoff(root)
    telemetry = build_local_telemetry_report()
    issues = []
    if handoff.get("status") != "pass":
        issues.append("handoff_write_failed")
    if telemetry.get("status") != "pass":
        issues.append("local_telemetry_blocked")
    return {
        "stage": "104.5",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "handoff": handoff,
        "local_telemetry": telemetry,
        "raw_manuscript_provider_leakage": 0,
        "credential_leakage": 0,
    }
