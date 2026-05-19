from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class ContradictionEvidence:
    case_id: str
    surface_conflict: bool
    canon_fact_a: str
    canon_fact_b: str
    same_canon_scope: bool
    truth_confidence_a: float
    truth_confidence_b: float
    reveal_lock_id: str = ""
    pov_boundary: bool = False
    scheduled_reveal_episode: int | None = None
    payoff_budget_reserved: bool = False
    writer_intent_tag: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class ContradictionClassification:
    case_id: str
    classification: str
    advisory_level: str
    exemption_status: str
    recommendation: str
    requires_writer_approval: bool
    confidence: float
    hard_block_allowed: bool = False
    canon_auto_resolution_allowed: bool = False
    auto_repair_allowed: bool = False

    def to_dict(self) -> dict:
        return asdict(self)
