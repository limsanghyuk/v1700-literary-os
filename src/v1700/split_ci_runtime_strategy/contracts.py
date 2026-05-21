from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class WorkflowLane:
    name: str
    workflow: str
    purpose: str
    cadence: str
    python_version: str
    status: str

    def to_dict(self) -> dict[str, str]:
        return {
            "name": self.name,
            "workflow": self.workflow,
            "purpose": self.purpose,
            "cadence": self.cadence,
            "python_version": self.python_version,
            "status": self.status,
        }
