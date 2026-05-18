from __future__ import annotations
from dataclasses import asdict, dataclass, field

@dataclass(frozen=True)
class Stage1075ReleaseContract:
    stage: str = '107.5'
    baseline_stage: str = '107'
    release_gate_affected: bool = False
    release_path_live_call_count: int = 0
    sandbox_raw_manuscript_allowed: bool = False
    python_fallback_required: bool = True
    issues: tuple[str, ...] = field(default_factory=tuple)
    def to_dict(self) -> dict: return asdict(self)
