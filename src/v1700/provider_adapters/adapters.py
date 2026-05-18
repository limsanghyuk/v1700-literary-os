from __future__ import annotations

import os
from abc import ABC, abstractmethod
from typing import Any

from v1700.provider_adapters.contracts import ProviderAdapterConfig, ProviderHealthCheck, ProviderRequest, ProviderResponse


class BaseProviderAdapter(ABC):
    def __init__(self, config: ProviderAdapterConfig) -> None:
        self.config = config

    def health_check(self) -> ProviderHealthCheck:
        issues: list[str] = []
        if self.config.requires_secret and not os.getenv(self.config.api_key_env or ""):
            issues.append("secret_env_not_present_but_not_required_for_dry_run")
        status = "configured_dry_run" if not self.config.allow_live_call else "configured_live_opt_in"
        return ProviderHealthCheck(
            provider_id=self.config.provider_id,
            provider_kind=self.config.provider_kind,
            status=status,
            configured=True,
            live_call_performed=False,
            endpoint=self.config.endpoint,
            model=self.config.model,
            api_key_env=self.config.api_key_env,
            issues=tuple(issues),
        )

    def generate(self, request: ProviderRequest) -> ProviderResponse:
        payload = self.build_payload(request)
        if not self.config.allow_live_call:
            return ProviderResponse(
                provider_id=self.config.provider_id,
                provider_kind=self.config.provider_kind,
                request_id=request.request_id,
                status="dry_run_ready",
                content=f"[{self.config.provider_id}] dry-run adapter ready for task={request.task}; no provider call performed.",
                live_call_performed=False,
                payload_preview=self._preview_payload(payload),
                issues=("live_call_disabled_by_default",),
            )
        # Stage92 intentionally keeps live call implementation behind the same
        # provider-zero guard. A future local developer can implement the actual
        # HTTP call per provider after explicitly enabling V1700_ALLOW_PROVIDER_CALLS=1.
        return ProviderResponse(
            provider_id=self.config.provider_id,
            provider_kind=self.config.provider_kind,
            request_id=request.request_id,
            status="live_call_guarded_not_executed",
            content=f"[{self.config.provider_id}] live opt-in detected, but Stage92 gate performs no external call.",
            live_call_performed=False,
            payload_preview=self._preview_payload(payload),
            issues=("stage92_release_gate_never_performs_live_provider_calls",),
        )

    @abstractmethod
    def build_payload(self, request: ProviderRequest) -> dict[str, Any]:
        raise NotImplementedError

    def _preview_payload(self, payload: dict[str, Any]) -> dict[str, Any]:
        preview = dict(payload)
        for key in ("prompt", "input", "messages", "contents"):
            if key in preview:
                preview[key] = "<redacted-for-release-evidence>"
        return preview


class OllamaAdapter(BaseProviderAdapter):
    def build_payload(self, request: ProviderRequest) -> dict[str, Any]:
        messages = []
        if request.system:
            messages.append({"role": "system", "content": request.system})
        messages.append({"role": "user", "content": request.prompt})
        return {
            "endpoint": self.config.endpoint,
            "model": self.config.model,
            "messages": messages,
            "stream": False,
            "options": {"temperature": request.temperature, "num_predict": request.max_tokens},
        }


class GPTAdapter(BaseProviderAdapter):
    def build_payload(self, request: ProviderRequest) -> dict[str, Any]:
        text = request.prompt if not request.system else f"{request.system}\n\n{request.prompt}"
        return {
            "endpoint": self.config.endpoint,
            "model": self.config.model,
            "input": text,
            "temperature": request.temperature,
            "max_output_tokens": request.max_tokens,
        }


class ClaudeAdapter(BaseProviderAdapter):
    def build_payload(self, request: ProviderRequest) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "endpoint": self.config.endpoint,
            "model": self.config.model,
            "max_tokens": request.max_tokens,
            "temperature": request.temperature,
            "messages": [{"role": "user", "content": request.prompt}],
        }
        if request.system:
            payload["system"] = request.system
        return payload


class GeminiAdapter(BaseProviderAdapter):
    def build_payload(self, request: ProviderRequest) -> dict[str, Any]:
        content = request.prompt if not request.system else f"{request.system}\n\n{request.prompt}"
        return {
            "endpoint": self.config.endpoint,
            "model": self.config.model,
            "contents": [{"role": "user", "parts": [{"text": content}]}],
            "generationConfig": {"temperature": request.temperature, "maxOutputTokens": request.max_tokens},
        }


def build_adapter(config: ProviderAdapterConfig) -> BaseProviderAdapter:
    if config.provider_kind == "ollama":
        return OllamaAdapter(config)
    if config.provider_kind == "gpt":
        return GPTAdapter(config)
    if config.provider_kind == "claude":
        return ClaudeAdapter(config)
    if config.provider_kind == "gemini":
        return GeminiAdapter(config)
    raise ValueError(f"unsupported provider_kind: {config.provider_kind}")
