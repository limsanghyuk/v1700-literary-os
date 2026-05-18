from __future__ import annotations
from dataclasses import dataclass, asdict

@dataclass(frozen=True)
class Stage109ReleaseContract:
    stage: str = "109"
    baseline_stage: str = "108"
    title: str = "Plugin / Marketplace Architecture"
    release_gate_affected_by_plugins: bool = False
    plugins_enabled_by_default: int = 0
    live_provider_call_count_in_release_gate: int = 0
    raw_manuscript_provider_leakage: int = 0

    def to_dict(self) -> dict:
        return asdict(self)
