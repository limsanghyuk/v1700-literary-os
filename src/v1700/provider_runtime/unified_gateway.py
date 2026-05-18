from __future__ import annotations

import time

from .context import ProviderCallContext
from .cost_ledger import ProviderCostLedger
from .health_monitor import ProviderHealthMonitor
from .release_policy import ReleaseProviderPolicy
from .response import ProviderResponse
from .task_router import ProviderTaskRouter


class UnifiedProviderGateway:
    """The single provider-call entrypoint for Stage97.2 and later stages."""

    def __init__(
        self,
        task_router: ProviderTaskRouter,
        health_monitor: ProviderHealthMonitor,
        cost_ledger: ProviderCostLedger | None = None,
        release_policy: ReleaseProviderPolicy | None = None,
        max_retries: int = 3,
    ):
        self.task_router = task_router
        self.health_monitor = health_monitor
        self.cost_ledger = cost_ledger
        self.release_policy = release_policy or ReleaseProviderPolicy()
        self.max_retries = max_retries
        self.live_provider_call_count = 0

    def call(self, prompt: str, context: ProviderCallContext) -> ProviderResponse:
        self.release_policy.validate_context(context)
        adapter = self.task_router.route(context)
        provider_id = adapter.get_provider_id()
        self.release_policy.validate_provider(provider_id, context)
        started = time.perf_counter()
        try:
            text = adapter.generate(prompt, context)
        except Exception as exc:
            self.health_monitor.mark_failed(provider_id, str(exc))
            raise
        latency_ms = (time.perf_counter() - started) * 1000.0
        if not context.release_mode and context.allow_live_provider_calls and provider_id not in {"fixture", "mock"}:
            self.live_provider_call_count += 1
        response = ProviderResponse(
            text=text,
            provider_id=provider_id,
            provider_kind="fixture" if provider_id in {"fixture", "mock"} else "runtime",
            latency_ms=latency_ms,
            estimated_cost_usd=0.0 if provider_id in {"fixture", "mock", "ollama", "lmstudio", "vllm"} else None,
        )
        if self.cost_ledger is not None:
            self.cost_ledger.record_call(response)
        return response

    def call_text(self, prompt: str, context: ProviderCallContext) -> str:
        return self.call(prompt, context).text
