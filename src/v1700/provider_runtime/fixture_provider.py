from __future__ import annotations

from .context import ProviderCallContext
from .interface import ProviderBridgeInterface


class FixtureProvider(ProviderBridgeInterface):
    """Provider-zero deterministic provider for release gates and tests."""

    def __init__(self, provider_id: str = "fixture", text: str = "fixture provider response"):
        self._provider_id = provider_id
        self._text = text
        self.generate_call_count = 0

    def generate(self, prompt: str, context: ProviderCallContext) -> str:
        self.generate_call_count += 1
        return f"{self._text}: {prompt[:80]}"

    def is_available(self) -> bool:
        return True

    def get_provider_id(self) -> str:
        return self._provider_id
