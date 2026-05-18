from __future__ import annotations

from dataclasses import dataclass

from .context import ProviderCallContext


class ProviderReleasePolicyError(RuntimeError):
    pass


@dataclass(frozen=True)
class ReleaseProviderPolicy:
    allowed_release_providers: tuple[str, ...] = ("fixture", "mock")

    def validate_context(self, context: ProviderCallContext) -> None:
        if context.release_mode and context.allow_live_provider_calls:
            raise ProviderReleasePolicyError("release_mode_live_provider_calls_forbidden")
        if not context.raw_manuscript_allowed and context.release_mode:
            return
        if context.release_mode and context.raw_manuscript_allowed:
            raise ProviderReleasePolicyError("release_mode_raw_manuscript_forbidden")

    def validate_provider(self, provider_id: str, context: ProviderCallContext) -> None:
        if context.release_mode and provider_id not in self.allowed_release_providers:
            raise ProviderReleasePolicyError(f"release_mode_live_provider_forbidden:{provider_id}")
