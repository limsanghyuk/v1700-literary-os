from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class Gate26AdvisoryCase:
    case_id: str
    conflict_type: str
    description: str
    advisory_level: str
    recommendation: str
    requires_writer_approval: bool
    hard_block_allowed: bool = False
    canon_auto_resolution_allowed: bool = False

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class Gate26AdvisoryPolicy:
    stage: str
    baseline_stage: str
    mode: str
    hard_block_enabled: bool
    auto_repair_enabled: bool
    canon_auto_resolution_enabled: bool
    writer_approval_required_for_true_contradiction: bool
    provider_default_calls: int
    live_provider_call_count_in_release_gate: int

    def to_dict(self) -> dict:
        return asdict(self)
