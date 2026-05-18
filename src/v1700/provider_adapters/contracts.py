from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Any, Mapping

PROVIDER_KINDS: tuple[str, ...] = ("ollama", "gpt", "claude", "gemini")


@dataclass(frozen=True)
class ProviderAdapterConfig:
    """Configuration for one optional local developer provider adapter.

    The config is intentionally inert by default: `allow_live_call` must be true
    before a concrete adapter may perform network I/O. This preserves V1700's
    provider_default_calls = 0 invariant while letting a developer wire Ollama,
    GPT, Claude, and Gemini on a personal workstation.
    """

    provider_id: str
    provider_kind: str
    model: str
    endpoint: str
    api_key_env: str | None = None
    enabled: bool = True
    allow_live_call: bool = False
    timeout_seconds: float = 30.0
    priority: int = 100
    notes: str = ""

    def __post_init__(self) -> None:
        if self.provider_kind not in PROVIDER_KINDS:
            raise ValueError(f"unsupported provider_kind: {self.provider_kind}")
        if self.timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be positive")
        if not self.provider_id:
            raise ValueError("provider_id is required")
        if not self.model:
            raise ValueError("model is required")
        if not self.endpoint:
            raise ValueError("endpoint is required")

    @property
    def requires_secret(self) -> bool:
        return bool(self.api_key_env)

    def to_dict(self) -> dict[str, Any]:
        return {
            "provider_id": self.provider_id,
            "provider_kind": self.provider_kind,
            "model": self.model,
            "endpoint": self.endpoint,
            "api_key_env": self.api_key_env,
            "enabled": self.enabled,
            "allow_live_call": self.allow_live_call,
            "timeout_seconds": self.timeout_seconds,
            "priority": self.priority,
            "requires_secret": self.requires_secret,
            "notes": self.notes,
        }


@dataclass(frozen=True)
class ProviderRequest:
    request_id: str
    task: str
    prompt: str
    system: str = ""
    temperature: float = 0.2
    max_tokens: int = 1024
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def redacted_prompt_hash(self) -> str:
        return hashlib.sha256(self.prompt.encode("utf-8")).hexdigest().upper()

    def to_dict(self, *, include_prompt: bool = False) -> dict[str, Any]:
        payload = {
            "request_id": self.request_id,
            "task": self.task,
            "system_present": bool(self.system),
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "prompt_sha256": self.redacted_prompt_hash(),
            "metadata": dict(self.metadata),
        }
        if include_prompt:
            payload["prompt"] = self.prompt
            payload["system"] = self.system
        return payload


@dataclass(frozen=True)
class ProviderResponse:
    provider_id: str
    provider_kind: str
    request_id: str
    status: str
    content: str
    live_call_performed: bool
    payload_preview: dict[str, Any]
    issues: tuple[str, ...] = ()

    @property
    def content_sha256(self) -> str:
        return hashlib.sha256(self.content.encode("utf-8")).hexdigest().upper()

    def to_dict(self) -> dict[str, Any]:
        return {
            "provider_id": self.provider_id,
            "provider_kind": self.provider_kind,
            "request_id": self.request_id,
            "status": self.status,
            "content_sha256": self.content_sha256,
            "content_preview": self.content[:160],
            "live_call_performed": self.live_call_performed,
            "payload_preview": self.payload_preview,
            "issues": list(self.issues),
        }


@dataclass(frozen=True)
class ProviderHealthCheck:
    provider_id: str
    provider_kind: str
    status: str
    configured: bool
    live_call_performed: bool
    endpoint: str
    model: str
    api_key_env: str | None
    issues: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "provider_id": self.provider_id,
            "provider_kind": self.provider_kind,
            "status": self.status,
            "configured": self.configured,
            "live_call_performed": self.live_call_performed,
            "endpoint": self.endpoint,
            "model": self.model,
            "api_key_env": self.api_key_env,
            "issues": list(self.issues),
        }


@dataclass(frozen=True)
class MultiAdapterSmokeReport:
    stage: str
    status: str
    configured_provider_count: int
    enabled_provider_count: int
    provider_kinds: tuple[str, ...]
    route_order: tuple[str, ...]
    health_checks: tuple[ProviderHealthCheck, ...]
    dry_run_responses: tuple[ProviderResponse, ...]
    provider_default_calls: int
    node2_raw_reveal_access_count: int
    live_call_count: int
    issues: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "stage": self.stage,
            "status": self.status,
            "configured_provider_count": self.configured_provider_count,
            "enabled_provider_count": self.enabled_provider_count,
            "provider_kinds": list(self.provider_kinds),
            "route_order": list(self.route_order),
            "health_checks": [item.to_dict() for item in self.health_checks],
            "dry_run_responses": [item.to_dict() for item in self.dry_run_responses],
            "provider_default_calls": self.provider_default_calls,
            "node2_raw_reveal_access_count": self.node2_raw_reveal_access_count,
            "live_call_count": self.live_call_count,
            "issues": list(self.issues),
        }


def stable_json_checksum(payload: Mapping[str, Any]) -> str:
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest().upper()


@dataclass(frozen=True)
class ProviderCredentialStatus:
    provider_id: str
    provider_kind: str
    requires_secret: bool
    api_key_env: str | None
    env_present: bool
    redacted_fingerprint: str | None
    status: str
    issues: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "provider_id": self.provider_id,
            "provider_kind": self.provider_kind,
            "requires_secret": self.requires_secret,
            "api_key_env": self.api_key_env,
            "env_present": self.env_present,
            "redacted_fingerprint": self.redacted_fingerprint,
            "status": self.status,
            "issues": list(self.issues),
        }


@dataclass(frozen=True)
class CredentialAuditReport:
    stage: str
    status: str
    credential_statuses: tuple[ProviderCredentialStatus, ...]
    secret_value_leaked: bool
    plain_secret_preview_count: int
    provider_default_calls: int
    node2_raw_reveal_access_count: int
    issues: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "stage": self.stage,
            "status": self.status,
            "credential_statuses": [item.to_dict() for item in self.credential_statuses],
            "secret_value_leaked": self.secret_value_leaked,
            "plain_secret_preview_count": self.plain_secret_preview_count,
            "provider_default_calls": self.provider_default_calls,
            "node2_raw_reveal_access_count": self.node2_raw_reveal_access_count,
            "issues": list(self.issues),
        }


@dataclass(frozen=True)
class NormalizedProviderResponse:
    provider_id: str
    provider_kind: str
    request_id: str
    normalized_status: str
    text: str
    finish_reason: str
    input_tokens: int
    output_tokens: int
    live_call_performed: bool
    safety_labels: tuple[str, ...] = ()
    issues: tuple[str, ...] = ()

    @property
    def text_sha256(self) -> str:
        return hashlib.sha256(self.text.encode("utf-8")).hexdigest().upper()

    def to_dict(self) -> dict[str, Any]:
        return {
            "provider_id": self.provider_id,
            "provider_kind": self.provider_kind,
            "request_id": self.request_id,
            "normalized_status": self.normalized_status,
            "text_sha256": self.text_sha256,
            "text_preview": self.text[:160],
            "finish_reason": self.finish_reason,
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "live_call_performed": self.live_call_performed,
            "safety_labels": list(self.safety_labels),
            "issues": list(self.issues),
        }


@dataclass(frozen=True)
class ProviderNormalizationReport:
    stage: str
    status: str
    normalized_responses: tuple[NormalizedProviderResponse, ...]
    normalized_provider_count: int
    live_call_count: int
    provider_default_calls: int
    node2_raw_reveal_access_count: int
    issues: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "stage": self.stage,
            "status": self.status,
            "normalized_responses": [item.to_dict() for item in self.normalized_responses],
            "normalized_provider_count": self.normalized_provider_count,
            "live_call_count": self.live_call_count,
            "provider_default_calls": self.provider_default_calls,
            "node2_raw_reveal_access_count": self.node2_raw_reveal_access_count,
            "issues": list(self.issues),
        }


@dataclass(frozen=True)
class LiveProviderSandboxReport:
    stage: str
    status: str
    mode: str
    opt_in_required: bool
    execution_allowed: bool
    configured_provider_count: int
    credential_audit: CredentialAuditReport
    normalization_report: ProviderNormalizationReport
    sandbox_transcript: tuple[dict[str, Any], ...]
    live_call_count: int
    provider_default_calls: int
    node2_raw_reveal_access_count: int
    issues: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "stage": self.stage,
            "status": self.status,
            "mode": self.mode,
            "opt_in_required": self.opt_in_required,
            "execution_allowed": self.execution_allowed,
            "configured_provider_count": self.configured_provider_count,
            "credential_audit": self.credential_audit.to_dict(),
            "normalization_report": self.normalization_report.to_dict(),
            "sandbox_transcript": list(self.sandbox_transcript),
            "live_call_count": self.live_call_count,
            "provider_default_calls": self.provider_default_calls,
            "node2_raw_reveal_access_count": self.node2_raw_reveal_access_count,
            "issues": list(self.issues),
        }
