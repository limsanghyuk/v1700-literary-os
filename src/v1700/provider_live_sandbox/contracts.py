from __future__ import annotations
from dataclasses import asdict, dataclass, field
from typing import Literal

@dataclass(frozen=True)
class ProviderSandboxConfig:
    sandbox_enabled: bool = False
    allow_live_provider_calls: bool = False
    release_gate_affected: bool = False
    raw_manuscript_allowed: bool = False
    provider_ids: tuple[str, ...] = ('openai','anthropic','gemini','ollama')
    model_aliases: dict[str, str] = field(default_factory=dict)
    max_live_calls: int = 12
    max_prompt_chars: int = 6000
    store_raw_response: bool = False
    def to_dict(self) -> dict: return asdict(self)

@dataclass(frozen=True)
class ModelIdProbeResult:
    provider_id: str
    requested_alias: str
    resolved_model_id: str | None
    probe_status: Literal['PASS','WARN','BLOCK','SKIPPED']
    reason: str
    live_call_performed: bool = False
    def to_dict(self) -> dict: return asdict(self)

@dataclass(frozen=True)
class ProviderPromptPacket:
    packet_id: str
    provider_id: str
    mode: Literal['PROSE','SCENARIO','LONGFORM_STRUCTURE','REVISION']
    payload_kind: Literal['FEATURE_ONLY','FIXTURE_SUMMARY','REDACTED_EXCERPT']
    prompt_sha256: str
    raw_manuscript_included: bool
    credential_included: bool
    max_output_tokens: int = 512
    def to_dict(self) -> dict: return asdict(self)

@dataclass(frozen=True)
class ProviderLiveResult:
    result_id: str
    provider_id: str
    model_id: str
    mode: str
    status: Literal['PASS','WARN','BLOCK','ERROR']
    latency_ms: int
    estimated_cost: float | None
    response_sha256: str
    response_excerpt: str
    raw_response_stored: bool
    leakage_status: str
    live_call_performed: bool = False
    error: str | None = None
    def to_dict(self) -> dict: return asdict(self)

@dataclass(frozen=True)
class ProviderBenchmarkScore:
    result_id: str
    provider_id: str
    model_id: str
    mode: Literal['PROSE','SCENARIO','LONGFORM_STRUCTURE','REVISION']
    score_total: float
    score_breakdown: dict[str, float]
    v1700_improvement_delta: float | None
    reviewer_notes: tuple[str, ...] = ()
    def to_dict(self) -> dict: return asdict(self)
