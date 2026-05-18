from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class KnowledgeStatus(str, Enum):
    UNAWARE = "unaware"
    SUSPECTS = "suspects"
    KNOWS = "knows"
    MISBELIEVES = "misbelieves"
    READER_ONLY = "reader_only"


class KnowledgeViolationError(AssertionError):
    pass


class KnowledgeLeakageError(KnowledgeViolationError):
    pass


class UnawarenessViolationError(KnowledgeViolationError):
    pass


@dataclass(frozen=True)
class KnowledgeRenderConstraint:
    character_id: str
    fact_id: str
    status: KnowledgeStatus
    render_mode: str
    behavioral_hint: str

    def to_dict(self) -> dict:
        return {
            "character_id": self.character_id,
            "fact_id": self.fact_id,
            "status": self.status.value,
            "render_mode": self.render_mode,
            "behavioral_hint": self.behavioral_hint,
        }
