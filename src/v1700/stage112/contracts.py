from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class Stage112Contract:
    stage: str = "112"
    baseline_stage: str = "111"
    title: str = "GitNexus-Aware NIE Preflight Bridge"
    implementation_mode: str = "preflight_before_nie"
    gitnexus_cli_required: bool = False
    python_fallback_required: bool = True
    live_provider_call_count_in_release_gate: int = 0
    physics_reward_bridge_llm_call_allowed: bool = False
    node2_raw_reveal_access: int = 0
    raw_manuscript_provider_leakage: int = 0
    credential_leakage: int = 0
    branchpoint_lineage_must_be_preserved: bool = True
    gate25_target_stage: str = "120"

    def to_dict(self) -> dict:
        return asdict(self)

