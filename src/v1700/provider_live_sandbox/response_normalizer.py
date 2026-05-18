from __future__ import annotations
import hashlib
from .contracts import ProviderLiveResult

def normalize_response(provider_id: str, model_id: str, mode: str, text: str, *, live_call_performed: bool = False, latency_ms: int = 0, status: str = "PASS", error: str | None = None) -> ProviderLiveResult:
    excerpt = text.replace("\n", " ")[:240]
    return ProviderLiveResult(
        result_id=hashlib.sha256(f"{provider_id}:{model_id}:{mode}:{text}".encode("utf-8")).hexdigest()[:16],
        provider_id=provider_id,
        model_id=model_id,
        mode=mode,
        status=status,  # type: ignore[arg-type]
        latency_ms=latency_ms,
        estimated_cost=None,
        response_sha256=hashlib.sha256(text.encode("utf-8")).hexdigest(),
        response_excerpt=excerpt,
        raw_response_stored=False,
        leakage_status="pass",
        live_call_performed=live_call_performed,
        error=error,
    )
