from __future__ import annotations

from dataclasses import asdict, dataclass, field


@dataclass(frozen=True)
class Stage105PreflightResult:
    status: str
    baseline_stage: str
    stage104_gate_status: str
    gitnexus_preflight_status: str
    branchpoint_survival_status: str
    provider_zero: bool
    issues: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict:
        return asdict(self)
