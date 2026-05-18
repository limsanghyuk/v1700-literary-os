from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ProviderCallContext:
    """Typed provider-call contract for Stage97.2.

    Defaults are intentionally safe: release mode is on, live provider calls are
    disabled, and raw manuscript transport is disallowed.
    """

    series_id: str = ""
    episode_idx: int = 0
    scene_id: str = ""
    stage: str = "97.2"

    narrative_fitness: float = 0.0
    endurance_risk: float = 0.0
    adversarial_severity: str = "NONE"

    provider_hint: str = ""  # local | speed | quality | cost | offline | fixture
    cost_policy: str = "bounded"  # zero | bounded | quality
    latency_policy: str = "normal"

    max_tokens: int = 2000
    temperature: float = 0.7
    timeout_seconds: int = 30
    cold_start_timeout_seconds: int = 90

    release_mode: bool = True
    allow_live_provider_calls: bool = False
    raw_manuscript_allowed: bool = False

    def normalized_hint(self) -> str:
        return (self.provider_hint or "").strip().lower()

    def clamp_fitness(self) -> float:
        return min(1.0, max(0.0, float(self.narrative_fitness)))
