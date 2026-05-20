from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Literal

MigrationManagerStatus = Literal["pass", "blocked"]
MigrationScope = Literal["schema", "binding", "checkpoint"]
MigrationAction = Literal["FREEZE_SCHEMA_CATALOG", "PLAN_NAMESPACE_MIGRATION", "PLAN_APPROVAL_CHECKPOINT"]


@dataclass(frozen=True)
class MigrationStep:
    step_id: str
    order: int
    scope: MigrationScope
    action: MigrationAction
    target_namespace: str
    schema_id: str | None = None
    case_id: str | None = None
    depends_on: tuple[str, ...] = ()
    requires_human_approval: bool = False
    execution_enabled: bool = False
    losdb_write_enabled: bool = False
    provider_call_required: bool = False
    rollback_anchor: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class MigrationPlan:
    stage: str
    baseline_stage: str
    status: MigrationManagerStatus
    steps: tuple[MigrationStep, ...]
    issues: tuple[str, ...] = ()
    counters: dict[str, int] = field(default_factory=dict)

    def to_dict(self) -> dict:
        payload = asdict(self)
        payload["steps"] = [step.to_dict() for step in self.steps]
        return payload
