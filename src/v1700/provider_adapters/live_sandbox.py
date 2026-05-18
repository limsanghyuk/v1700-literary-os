from __future__ import annotations

import os
from typing import Any

from v1700.provider_adapters.config import build_default_multi_provider_configs
from v1700.provider_adapters.credential_audit import audit_provider_credentials
from v1700.provider_adapters.contracts import LiveProviderSandboxReport, ProviderRequest
from v1700.provider_adapters.normalization import run_stage93_response_normalization_probe
from v1700.provider_adapters.router import MultiProviderAdapterRouter


def run_stage93_live_provider_sandbox(*, execution_allowed: bool | None = None) -> LiveProviderSandboxReport:
    """Build a safe local-provider sandbox transcript without making release-time calls.

    Developers can set V1700_ALLOW_PROVIDER_CALLS=1 and V1700_STAGE93_EXECUTE_LIVE_PROVIDER=1
    on a personal computer to exercise real providers in a separate, non-release workflow.
    This release probe intentionally records the opt-in boundary and normalized transcript
    while keeping live_call_count at 0.
    """

    allow_flag = os.getenv("V1700_ALLOW_PROVIDER_CALLS", "0") == "1"
    execute_flag = os.getenv("V1700_STAGE93_EXECUTE_LIVE_PROVIDER", "0") == "1"
    execution_allowed = allow_flag and execute_flag if execution_allowed is None else execution_allowed

    configs = build_default_multi_provider_configs(allow_live_call=execution_allowed)
    router = MultiProviderAdapterRouter(configs)
    request = ProviderRequest(
        request_id="stage93-live-provider-sandbox",
        task="live_provider_opt_in_sandbox",
        system="You are in a V1700 provider sandbox. Do not reveal raw planning state.",
        prompt="Return one sentence confirming sandbox readiness.",
        metadata={"stage": "93", "live_opt_in": execution_allowed},
    )
    dry_or_guarded = router.dry_run_all(request)
    credential_audit = audit_provider_credentials(configs)
    normalization_report = run_stage93_response_normalization_probe()
    transcript: list[dict[str, Any]] = []
    for response in dry_or_guarded:
        transcript.append(
            {
                "provider_id": response.provider_id,
                "provider_kind": response.provider_kind,
                "status": response.status,
                "live_call_performed": response.live_call_performed,
                "content_sha256": response.content_sha256,
                "issues": list(response.issues),
            }
        )
    issues: list[str] = []
    if len(transcript) != 4:
        issues.append("sandbox_provider_count_not_4")
    if any(item["live_call_performed"] for item in transcript):
        issues.append("sandbox_performed_live_call_during_release_probe")
    if credential_audit.status != "pass":
        issues.append("credential_audit_blocked")
    if normalization_report.status != "pass":
        issues.append("normalization_report_blocked")
    mode = "live_opt_in_guarded" if execution_allowed else "dry_run_release_safe"
    return LiveProviderSandboxReport(
        stage="93",
        status="pass" if not issues else "blocked",
        mode=mode,
        opt_in_required=True,
        execution_allowed=execution_allowed,
        configured_provider_count=len(configs),
        credential_audit=credential_audit,
        normalization_report=normalization_report,
        sandbox_transcript=tuple(transcript),
        live_call_count=0,
        provider_default_calls=0,
        node2_raw_reveal_access_count=0,
        issues=tuple(issues),
    )
