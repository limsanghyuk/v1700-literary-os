from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DocumentedSurface:
    name: str
    status: str
    path: str
    summary: str

    def to_dict(self) -> dict[str, str]:
        return {
            "name": self.name,
            "status": self.status,
            "path": self.path,
            "summary": self.summary,
        }
