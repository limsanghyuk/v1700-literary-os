from __future__ import annotations

from v1700.provider_adapters.adapters import BaseProviderAdapter, build_adapter
from v1700.provider_adapters.config import build_default_multi_provider_configs, sorted_enabled_configs
from v1700.provider_adapters.contracts import MultiAdapterSmokeReport, ProviderAdapterConfig, ProviderRequest


class MultiProviderAdapterRouter:
    """Provider router for local developer machines.

    It registers Ollama, GPT, Claude, and Gemini adapters but defaults to dry-run
    release evidence. This is deliberate: Stage92 configures the providers while
    preserving V1700's provider_default_calls = 0 contract.
    """

    def __init__(self, configs: tuple[ProviderAdapterConfig, ...] | None = None) -> None:
        self.configs = configs or build_default_multi_provider_configs()
        self.enabled_configs = sorted_enabled_configs(self.configs)
        self.adapters: tuple[BaseProviderAdapter, ...] = tuple(build_adapter(config) for config in self.enabled_configs)

    @property
    def provider_kinds(self) -> tuple[str, ...]:
        return tuple(config.provider_kind for config in self.configs)

    @property
    def route_order(self) -> tuple[str, ...]:
        return tuple(config.provider_id for config in self.enabled_configs)

    def adapter_for(self, provider_kind: str) -> BaseProviderAdapter:
        for adapter in self.adapters:
            if adapter.config.provider_kind == provider_kind:
                return adapter
        raise KeyError(provider_kind)

    def health_checks(self):
        return tuple(adapter.health_check() for adapter in self.adapters)

    def dry_run_all(self, request: ProviderRequest):
        return tuple(adapter.generate(request) for adapter in self.adapters)

    def smoke_report(self) -> MultiAdapterSmokeReport:
        request = ProviderRequest(
            request_id="stage92-multi-provider-smoke",
            task="studio_adapter_probe",
            system="You are a provider adapter probe. Do not reveal V1700 internals.",
            prompt="Render a one-line dry-run readiness acknowledgement for the Writer Studio adapter.",
            metadata={"stage": "92", "node2_surface_only": True},
        )
        health = self.health_checks()
        responses = self.dry_run_all(request)
        issues: list[str] = []
        required = {"ollama", "gpt", "claude", "gemini"}
        configured = set(self.provider_kinds)
        if configured != required:
            issues.append(f"provider_kind_set_mismatch:{sorted(configured)}")
        if len(self.enabled_configs) != 4:
            issues.append("enabled_provider_count_not_4")
        if any(item.live_call_performed for item in health):
            issues.append("health_check_performed_live_call")
        if any(item.live_call_performed for item in responses):
            issues.append("dry_run_performed_live_call")
        if any(response.status not in {"dry_run_ready", "live_call_guarded_not_executed"} for response in responses):
            issues.append("unexpected_provider_response_status")
        return MultiAdapterSmokeReport(
            stage="92",
            status="pass" if not issues else "blocked",
            configured_provider_count=len(self.configs),
            enabled_provider_count=len(self.enabled_configs),
            provider_kinds=tuple(sorted(configured)),
            route_order=self.route_order,
            health_checks=health,
            dry_run_responses=responses,
            provider_default_calls=0,
            node2_raw_reveal_access_count=0,
            live_call_count=0,
            issues=tuple(issues),
        )


def run_stage92_multi_adapter_smoke() -> dict:
    return MultiProviderAdapterRouter().smoke_report().to_dict()
