from __future__ import annotations

from v1700.arc_reveal_knowledge.knowledge_contracts import (
    KnowledgeLeakageError,
    KnowledgeRenderConstraint,
    KnowledgeStatus,
    UnawarenessViolationError,
)


class CharacterKnowledgeProseBridge:
    """Turns character knowledge asymmetry into prose-safe render constraints."""

    def __init__(self):
        self._knowledge: dict[str, dict[str, KnowledgeStatus]] = {}

    def set_status(self, character_id: str, fact_id: str, status: KnowledgeStatus) -> None:
        self._knowledge.setdefault(character_id, {})[fact_id] = status

    def get_status(self, character_id: str, fact_id: str) -> KnowledgeStatus:
        return self._knowledge.get(character_id, {}).get(fact_id, KnowledgeStatus.UNAWARE)

    def constraint_for(self, character_id: str, fact_id: str) -> KnowledgeRenderConstraint:
        status = self.get_status(character_id, fact_id)
        mode, hint = {
            KnowledgeStatus.UNAWARE: ("do_not_name_fact", "render absence, hesitation, or irrelevant behavior"),
            KnowledgeStatus.SUSPECTS: ("indirect_suspicion_only", "render inference, not certainty"),
            KnowledgeStatus.KNOWS: ("direct_behavior_allowed", "render informed action without exposition dump"),
            KnowledgeStatus.MISBELIEVES: ("false_belief_behavior", "render confident but wrong interpretation"),
            KnowledgeStatus.READER_ONLY: ("reader_only_never_in_character_mind", "block character internalization"),
        }[status]
        return KnowledgeRenderConstraint(character_id, fact_id, status, mode, hint)

    def assert_no_leakage(self, character_id: str, fact_id: str, *, direct_reference: bool) -> None:
        status = self.get_status(character_id, fact_id)
        if status == KnowledgeStatus.READER_ONLY and direct_reference:
            raise KnowledgeLeakageError(f"{fact_id} is reader-only and leaked into {character_id}")
        if status == KnowledgeStatus.UNAWARE and direct_reference:
            raise UnawarenessViolationError(f"{character_id} is unaware of {fact_id}")

    def blocked_facts_for(self, character_id: str) -> tuple[str, ...]:
        blocked = [
            fact_id
            for fact_id, status in self._knowledge.get(character_id, {}).items()
            if status in {KnowledgeStatus.UNAWARE, KnowledgeStatus.READER_ONLY}
        ]
        return tuple(sorted(blocked))

    def asymmetry_pressure(self, fact_id: str) -> float:
        statuses = [facts[fact_id] for facts in self._knowledge.values() if fact_id in facts]
        if not statuses:
            return 0.0
        hidden = sum(1 for status in statuses if status in {KnowledgeStatus.UNAWARE, KnowledgeStatus.READER_ONLY})
        return round(hidden / len(statuses), 2)

    def to_dict(self) -> dict:
        return {
            character_id: {
                fact_id: status.value
                for fact_id, status in sorted(facts.items())
            }
            for character_id, facts in sorted(self._knowledge.items())
        }
