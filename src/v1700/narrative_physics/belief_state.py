from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class CharacterBeliefStateVector:
    character_id: str
    reader_only_fact_count: int
    character_known_fact_count: int
    indirect_suspicion_count: int
    leakage_count: int
    surface_safe: bool

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__.copy()


class BeliefStateEngine:
    """Builds prose-safe belief vectors without exposing raw reader-only facts."""

    forbidden_markers = ("READER_ONLY:", "RAW_REVEAL:", "INTERNAL_MARKER:", "SECRET:")

    def build(self, season_evidence: dict[str, Any]) -> tuple[CharacterBeliefStateVector, ...]:
        reader_only = 0
        indirect = 0
        known = 0
        leakage = 0
        for episode in season_evidence.get("episodes", []):
            for scene in episode.get("scenes", []):
                mode = scene.get("knowledge_mode", "")
                if mode in {"reader_only_never_in_character_mind", "do_not_name_fact"}:
                    reader_only += 1
                elif mode == "indirect_suspicion_only":
                    indirect += 1
                else:
                    known += 1
                leakage += self.leakage_count(str(scene))
        return (
            CharacterBeliefStateVector(
                character_id="protagonist",
                reader_only_fact_count=reader_only,
                character_known_fact_count=known,
                indirect_suspicion_count=indirect,
                leakage_count=leakage,
                surface_safe=leakage == 0,
            ),
        )

    def leakage_count(self, text: str) -> int:
        return sum(text.count(marker) for marker in self.forbidden_markers)
