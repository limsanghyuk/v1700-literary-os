from __future__ import annotations

from .context import ProviderCallContext
from .fixture_provider import FixtureProvider
from .health_monitor import ProviderHealthMonitor
from .interface import ProviderBridgeInterface


class ProviderTaskRouter:
    """Pure deterministic provider routing.

    LLM-0 invariant: route() must never call generate() or any live provider API.
    """

    THRESHOLDS = {
        "local": (0.00, 0.40),
        "speed": (0.40, 0.75),
        "quality": (0.75, 1.01),
    }
    FALLBACK_CHAIN = ["local", "speed", "quality", "fixture"]
    HINT_TO_TIER = {
        "cost": "local",
        "local": "local",
        "offline": "fixture",
        "speed": "speed",
        "quality": "quality",
        "fixture": "fixture",
        "mock": "fixture",
    }

    def __init__(self, providers: dict[str, ProviderBridgeInterface], health_monitor: ProviderHealthMonitor):
        self.providers = dict(providers)
        self.health_monitor = health_monitor
        self.route_decisions: list[dict] = []

    def route(self, context: ProviderCallContext) -> ProviderBridgeInterface:
        if context.release_mode:
            provider = self._get_provider("fixture")
            self._record(context, provider.get_provider_id(), "release_mode_fixture")
            return provider
        if context.normalized_hint():
            provider = self._route_by_hint(context)
            self._record(context, provider.get_provider_id(), "provider_hint")
            return provider
        provider = self._route_by_fitness(context)
        self._record(context, provider.get_provider_id(), "fitness")
        return provider

    def _route_by_hint(self, context: ProviderCallContext) -> ProviderBridgeInterface:
        tier = self.HINT_TO_TIER.get(context.normalized_hint(), "fixture")
        return self._get_healthy_provider(tier) or self._fallback_provider()

    def _route_by_fitness(self, context: ProviderCallContext) -> ProviderBridgeInterface:
        fitness = context.clamp_fitness()
        for tier, (lo, hi) in self.THRESHOLDS.items():
            if lo <= fitness < hi:
                return self._get_healthy_provider(tier) or self._fallback_provider()
        return self._fallback_provider()

    def _get_healthy_provider(self, tier: str) -> ProviderBridgeInterface | None:
        preferred = [pid for pid, provider in self.providers.items() if self._tier_for_provider(pid) == tier and self.health_monitor.is_healthy(pid)]
        if preferred:
            return self.providers[preferred[0]]
        for fallback_tier in self.FALLBACK_CHAIN:
            if fallback_tier == tier:
                continue
            for pid, provider in self.providers.items():
                if self._tier_for_provider(pid) == fallback_tier and self.health_monitor.is_healthy(pid):
                    return provider
        return None

    def _fallback_provider(self) -> ProviderBridgeInterface:
        return self.providers.get("fixture") or FixtureProvider()

    def _get_provider(self, provider_id: str) -> ProviderBridgeInterface:
        return self.providers.get(provider_id) or self._fallback_provider()

    @staticmethod
    def _tier_for_provider(provider_id: str) -> str:
        if provider_id in {"fixture", "mock"}:
            return "fixture"
        if provider_id in {"ollama", "lmstudio", "vllm"}:
            return "local"
        if provider_id in {"gemini", "claude-haiku", "haiku"}:
            return "speed"
        return "quality"

    def _record(self, context: ProviderCallContext, provider_id: str, reason: str) -> None:
        self.route_decisions.append({
            "stage": context.stage,
            "provider_id": provider_id,
            "reason": reason,
            "narrative_fitness": context.narrative_fitness,
            "provider_hint": context.provider_hint,
            "release_mode": context.release_mode,
        })
