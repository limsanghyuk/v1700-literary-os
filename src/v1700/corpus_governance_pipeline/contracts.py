from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Literal

CorpusGovernanceStatus = Literal["pass", "blocked"]
ApprovalLaneName = Literal["automatic_registry", "writer_review_queue"]


@dataclass(frozen=True)
class NamespaceGovernanceProfile:
    profile_id: str
    contract_id: str
    target_namespace: str
    governance_channel: ApprovalLaneName
    retention_class: str
    evidence_scope: str
    requires_human_approval: bool
    stage140_release_ready: bool
    write_enabled: bool = False
    provider_call_required: bool = False
    rollback_anchor: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class CorpusCasePacket:
    packet_id: str
    case_id: str
    contract_id: str
    governance_profile_id: str
    target_namespace: str
    storage_key: str
    approval_lane: ApprovalLaneName
    corpus_status: str
    retention_class: str
    audit_event_key: str
    depends_on_route: str
    requires_human_approval: bool
    stage140_release_ready: bool
    write_enabled: bool = False
    provider_call_required: bool = False
    rollback_anchor: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class ReviewQueuePacket:
    packet_id: str
    lane_name: ApprovalLaneName
    queue_namespace: str
    reviewed_case_ids: tuple[str, ...]
    governance_profile_ids: tuple[str, ...]
    depends_on_steps: tuple[str, ...]
    audit_event_key: str
    stage140_release_ready: bool
    write_enabled: bool = False
    provider_call_required: bool = False
    rollback_anchor: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class CorpusGovernancePipeline:
    stage: str
    baseline_stage: str
    status: CorpusGovernanceStatus
    governance_profiles: tuple[NamespaceGovernanceProfile, ...]
    case_packets: tuple[CorpusCasePacket, ...]
    review_queue_packets: tuple[ReviewQueuePacket, ...]
    issues: tuple[str, ...] = ()
    counters: dict[str, int] = field(default_factory=dict)

    def to_dict(self) -> dict:
        payload = asdict(self)
        payload["governance_profiles"] = [profile.to_dict() for profile in self.governance_profiles]
        payload["case_packets"] = [packet.to_dict() for packet in self.case_packets]
        payload["review_queue_packets"] = [packet.to_dict() for packet in self.review_queue_packets]
        return payload
