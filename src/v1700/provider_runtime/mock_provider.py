from __future__ import annotations

from .fixture_provider import FixtureProvider


class MockProvider(FixtureProvider):
    def __init__(self, provider_id: str = "mock", text: str = "mock provider response"):
        super().__init__(provider_id=provider_id, text=text)
