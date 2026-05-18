from __future__ import annotations
from dataclasses import asdict, dataclass, field


@dataclass(frozen=True)
class Stage106PreflightResult:
    status: str
    baseline_stage: str
    stage105_gate_status: str
    gitnexus_preflight_status: str
    branchpoint_survival_status: str
    provider_zero: bool
    privacy_mode: str = "FEATURE_ONLY"
    issues: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict:
        return asdict(self)
