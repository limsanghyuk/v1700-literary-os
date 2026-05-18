from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ProviderResponse:
    text: str
    provider_id: str
    provider_kind: str
    tokens_used: int = 0
    latency_ms: float = 0.0
    estimated_cost_usd: float | None = None
    fallback_used: bool = False
    safety_flags: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)
