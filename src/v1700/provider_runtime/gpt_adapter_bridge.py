from __future__ import annotations

from .fixture_provider import FixtureProvider


class GPTAdapterBridge(FixtureProvider):
    """Dry-run compatibility bridge for gpt runtime contracts.

    Live SDK calls remain outside release gates; this bridge exists so contract
    gates can validate shape without calling external providers.
    """

    def __init__(self, provider_id: str = "gpt"):
        super().__init__(provider_id=provider_id, text="gpt fixture bridge response")
