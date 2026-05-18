from __future__ import annotations

from .contracts import ErrorReportContract


def build_safe_error_report(error_id: str = "STAGE103-DEMO-ERROR") -> dict:
    result = ErrorReportContract(
        status="pass",
        error_id=error_id,
        severity="WARN",
        safe_message="A recoverable local workflow issue was captured with redacted context.",
        raw_prompt_included=False,
        credential_included=False,
        redaction_policy="drop_raw_prompt_drop_credentials_keep_stage_tool_and_gate_ids",
        issues=(),
    )
    return result.to_dict()
