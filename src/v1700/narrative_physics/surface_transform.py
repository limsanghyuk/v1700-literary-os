from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class SurfaceTransformGuardReport:
    node2_raw_reveal_access_count: int
    reader_only_leakage_count: int
    internal_marker_leakage_count: int
    status: str

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__.copy()


class Node2SurfaceTransformGuard:
    raw_markers = ("RAW_REVEAL:", "FORBIDDEN_REVEAL:", "SECRET:")
    internal_markers = ("INTERNAL_MARKER:", "Command authority", "Node1 authority", "READER_ONLY:")

    def audit(self, payload: Any) -> SurfaceTransformGuardReport:
        text = str(payload)
        raw = sum(text.count(marker) for marker in self.raw_markers)
        reader_only = text.count("READER_ONLY:")
        internal = sum(text.count(marker) for marker in self.internal_markers)
        return SurfaceTransformGuardReport(
            node2_raw_reveal_access_count=raw,
            reader_only_leakage_count=reader_only,
            internal_marker_leakage_count=internal,
            status="pass" if raw == 0 and reader_only == 0 and internal == 0 else "blocked",
        )
