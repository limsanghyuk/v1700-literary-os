from __future__ import annotations


def build_safe_error_boundary_report() -> dict:
    return {
        "status": "pass",
        "redaction_policy": "drop_raw_text_drop_credentials_keep_stage_and_safe_error_code",
        "raw_manuscript_included": False,
        "credential_included": False,
        "provider_payload_included": False,
        "safe_error_code": "STAGE104_SAFE_BETA_WARNING",
    }
