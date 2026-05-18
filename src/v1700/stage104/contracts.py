from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Literal

Status = Literal["pass", "warn", "blocked"]


@dataclass(frozen=True)
class Stage104PreflightResult:
    status: Status
    baseline_stage: str
    gitnexus_preflight_status: str
    stage103_gate_status: str
    branchpoint_survival_status: str
    provider_zero: bool
    issues: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class Stage104ReleaseContract:
    status: Status
    workspace_kernel_status: str
    unified_board_status: str
    review_decision_status: str
    sample_project_status: str
    beta_handoff_status: str
    provider_default_calls: int = 0
    live_provider_call_count_in_release_gate: int = 0
    raw_manuscript_provider_leakage: int = 0
    node2_raw_reveal_access: int = 0
    credential_leakage: int = 0

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
