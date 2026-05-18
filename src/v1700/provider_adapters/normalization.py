from __future__ import annotations

from typing import Any, Mapping

from v1700.provider_adapters.config import build_default_multi_provider_configs
from v1700.provider_adapters.contracts import (
    NormalizedProviderResponse,
    ProviderNormalizationReport,
    ProviderRequest,
)
from v1700.provider_adapters.router import MultiProviderAdapterRouter


def normalize_provider_response(
    *,
    provider_id: str,
    provider_kind: str,
    request_id: str,
    raw: Mapping[str, Any],
    live_call_performed: bool = False,
) -> NormalizedProviderResponse:
    text = ""
    finish_reason = "unknown"
    input_tokens = 0
    output_tokens = 0
    issues: list[str] = []

    if provider_kind == "ollama":
        text = str(raw.get("message", {}).get("content", raw.get("response", "")))
        finish_reason = "stop" if raw.get("done", True) else "length"
        input_tokens = int(raw.get("prompt_eval_count", 0) or 0)
        output_tokens = int(raw.get("eval_count", 0) or 0)
    elif provider_kind == "gpt":
        if "output_text" in raw:
            text = str(raw.get("output_text", ""))
        else:
            output = raw.get("output", [])
            if output and isinstance(output, list):
                content = output[0].get("content", []) if isinstance(output[0], dict) else []
                if content and isinstance(content, list):
                    text = str(content[0].get("text", ""))
        finish_reason = str(raw.get("finish_reason", raw.get("status", "completed")))
        usage = raw.get("usage", {}) if isinstance(raw.get("usage", {}), Mapping) else {}
        input_tokens = int(usage.get("input_tokens", usage.get("prompt_tokens", 0)) or 0)
        output_tokens = int(usage.get("output_tokens", usage.get("completion_tokens", 0)) or 0)
    elif provider_kind == "claude":
        content = raw.get("content", [])
        if content and isinstance(content, list):
            text = str(content[0].get("text", ""))
        finish_reason = str(raw.get("stop_reason", "end_turn"))
        usage = raw.get("usage", {}) if isinstance(raw.get("usage", {}), Mapping) else {}
        input_tokens = int(usage.get("input_tokens", 0) or 0)
        output_tokens = int(usage.get("output_tokens", 0) or 0)
    elif provider_kind == "gemini":
        candidates = raw.get("candidates", [])
        if candidates and isinstance(candidates, list):
            parts = candidates[0].get("content", {}).get("parts", [])
            if parts and isinstance(parts, list):
                text = str(parts[0].get("text", ""))
            finish_reason = str(candidates[0].get("finishReason", "STOP"))
        usage = raw.get("usageMetadata", {}) if isinstance(raw.get("usageMetadata", {}), Mapping) else {}
        input_tokens = int(usage.get("promptTokenCount", 0) or 0)
        output_tokens = int(usage.get("candidatesTokenCount", 0) or 0)
    else:
        issues.append("unsupported_provider_kind")

    if not text:
        issues.append("normalized_text_empty")
    return NormalizedProviderResponse(
        provider_id=provider_id,
        provider_kind=provider_kind,
        request_id=request_id,
        normalized_status="pass" if not issues else "blocked",
        text=text,
        finish_reason=finish_reason,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        live_call_performed=live_call_performed,
        safety_labels=(),
        issues=tuple(issues),
    )


def _raw_from_dry_run_response(provider_kind: str, text: str) -> dict[str, Any]:
    if provider_kind == "ollama":
        return {"message": {"content": text}, "done": True, "prompt_eval_count": 12, "eval_count": 24}
    if provider_kind == "gpt":
        return {"output_text": text, "status": "completed", "usage": {"input_tokens": 12, "output_tokens": 24}}
    if provider_kind == "claude":
        return {"content": [{"type": "text", "text": text}], "stop_reason": "end_turn", "usage": {"input_tokens": 12, "output_tokens": 24}}
    if provider_kind == "gemini":
        return {"candidates": [{"content": {"parts": [{"text": text}]}, "finishReason": "STOP"}], "usageMetadata": {"promptTokenCount": 12, "candidatesTokenCount": 24}}
    return {"text": text}


def run_stage93_response_normalization_probe() -> ProviderNormalizationReport:
    router = MultiProviderAdapterRouter(build_default_multi_provider_configs(allow_live_call=False))
    request = ProviderRequest(
        request_id="stage93-response-normalization-probe",
        task="response_normalization_probe",
        system="Normalize only; do not reveal V1700 internals.",
        prompt="Return a dry-run provider-normalization acknowledgement.",
        metadata={"stage": "93", "provider_zero": True},
    )
    dry_responses = router.dry_run_all(request)
    normalized = tuple(
        normalize_provider_response(
            provider_id=response.provider_id,
            provider_kind=response.provider_kind,
            request_id=response.request_id,
            raw=_raw_from_dry_run_response(response.provider_kind, response.content),
            live_call_performed=response.live_call_performed,
        )
        for response in dry_responses
    )
    issues: list[str] = []
    if len(normalized) != 4:
        issues.append("normalized_provider_count_not_4")
    if any(item.live_call_performed for item in normalized):
        issues.append("normalization_performed_live_call")
    if any(item.normalized_status != "pass" for item in normalized):
        issues.append("normalization_status_blocked")
    return ProviderNormalizationReport(
        stage="93",
        status="pass" if not issues else "blocked",
        normalized_responses=normalized,
        normalized_provider_count=len(normalized),
        live_call_count=0,
        provider_default_calls=0,
        node2_raw_reveal_access_count=0,
        issues=tuple(issues),
    )
