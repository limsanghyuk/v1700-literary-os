from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Literal

SchemaRegistryStatus = Literal["pass", "blocked"]
SchemaFieldType = Literal["string", "boolean"]
BindingStatus = Literal["pass", "blocked"]


@dataclass(frozen=True)
class SchemaField:
    name: str
    field_type: SchemaFieldType
    required: bool
    description: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class SchemaDefinition:
    schema_id: str
    title: str
    stage: str
    version: str
    record_kind: str
    fields: tuple[SchemaField, ...]
    review_required: bool
    migration_ready: bool
    storage_contract_ready: bool
    losdb_write_enabled: bool = False
    migration_execution_enabled: bool = False
    provider_call_required: bool = False

    def to_dict(self) -> dict:
        payload = asdict(self)
        payload["fields"] = [field.to_dict() for field in self.fields]
        return payload


@dataclass(frozen=True)
class CandidateSchemaBinding:
    case_id: str
    decision: str
    schema_id: str
    status: BindingStatus
    schema_valid: bool
    migration_ready: bool
    storage_contract_ready: bool
    writer_review_required: bool
    losdb_write_enabled: bool = False
    migration_execution_enabled: bool = False
    provider_call_required: bool = False
    issues: tuple[str, ...] = ()

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class SchemaRegistry:
    stage: str
    baseline_stage: str
    status: SchemaRegistryStatus
    schemas: tuple[SchemaDefinition, ...]
    bindings: tuple[CandidateSchemaBinding, ...]
    issues: tuple[str, ...] = ()
    counters: dict[str, int] = field(default_factory=dict)

    def to_dict(self) -> dict:
        payload = asdict(self)
        payload["schemas"] = [schema.to_dict() for schema in self.schemas]
        payload["bindings"] = [binding.to_dict() for binding in self.bindings]
        return payload
