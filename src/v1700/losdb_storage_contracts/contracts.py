from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Literal

StorageContractStatus = Literal["pass", "blocked"]
ApprovalLaneName = Literal["automatic_registry", "writer_review_queue"]


@dataclass(frozen=True)
class StorageFieldContract:
    name: str
    field_type: str
    required: bool
    storage_column: str
    index_position: int
    description: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class NamespaceContract:
    contract_id: str
    contract_version: str
    schema_id: str
    record_kind: str
    target_namespace: str
    target_collection: str
    storage_key_template: str
    governance_channel: ApprovalLaneName
    migration_dependency: str
    fields: tuple[StorageFieldContract, ...]
    requires_human_approval: bool = False
    write_enabled: bool = False
    provider_call_required: bool = False
    rollback_anchor: str = ""

    def to_dict(self) -> dict:
        payload = asdict(self)
        payload["fields"] = [field.to_dict() for field in self.fields]
        return payload


@dataclass(frozen=True)
class BindingRoute:
    route_id: str
    case_id: str
    contract_id: str
    target_namespace: str
    storage_key: str
    depends_on_step: str
    approval_lane: ApprovalLaneName
    stage139_governance_ready: bool
    write_enabled: bool = False
    provider_call_required: bool = False
    rollback_anchor: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class ApprovalLaneContract:
    lane_id: str
    lane_name: ApprovalLaneName
    queue_namespace: str
    depends_on_steps: tuple[str, ...]
    reviewed_case_ids: tuple[str, ...]
    write_enabled: bool = False
    provider_call_required: bool = False
    rollback_anchor: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class StorageContractCatalog:
    stage: str
    baseline_stage: str
    status: StorageContractStatus
    contracts: tuple[NamespaceContract, ...]
    routes: tuple[BindingRoute, ...]
    approval_lanes: tuple[ApprovalLaneContract, ...]
    issues: tuple[str, ...] = ()
    counters: dict[str, int] = field(default_factory=dict)

    def to_dict(self) -> dict:
        payload = asdict(self)
        payload["contracts"] = [contract.to_dict() for contract in self.contracts]
        payload["routes"] = [route.to_dict() for route in self.routes]
        payload["approval_lanes"] = [lane.to_dict() for lane in self.approval_lanes]
        return payload
