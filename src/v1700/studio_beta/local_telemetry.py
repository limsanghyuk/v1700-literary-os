from __future__ import annotations

from .beta_event_log import build_beta_event_log
from .contracts import LocalTelemetryReport
from .safe_error_boundary import build_safe_error_boundary_report


def build_local_telemetry_report() -> dict:
    event_log = build_beta_event_log()
    error = build_safe_error_boundary_report()
    issues = []
    if event_log.get("raw_manuscript_included"):
        issues.append("telemetry_raw_text_leakage")
    if error.get("credential_included") or error.get("provider_payload_included"):
        issues.append("telemetry_sensitive_payload_leakage")
    result = LocalTelemetryReport(
        status="pass" if not issues else "blocked",
        event_count=event_log.get("event_count", 0),
        raw_manuscript_included=False,
        credential_included=False,
        provider_payload_included=False,
        local_only=True,
        issues=tuple(issues),
    )
    payload = result.to_dict()
    payload["event_log"] = event_log
    payload["safe_error_boundary"] = error
    return payload
