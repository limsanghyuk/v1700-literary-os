from __future__ import annotations

from pathlib import Path

from v1700.security_hardening.report import run_stage99_1_security_privacy_hardening


def run_stage99_security_gate(root: Path | None = None) -> dict:
    report = run_stage99_1_security_privacy_hardening(root)
    return {
        "status": report.get("status"),
        "stage": "99.1",
        "credential_leakage": report.get("credential_leakage", 0),
        "raw_manuscript_provider_leakage": report.get("raw_manuscript_provider_leakage", 0),
        "provider_live_call_count_in_release": report.get("provider_live_call_count_in_release", 0),
        "node2_raw_reveal_access": report.get("node2_raw_reveal_access", 0),
        "internal_marker_leakage": report.get("internal_marker_leakage", 0),
        "issues": report.get("issues", []),
    }
