from __future__ import annotations

from dataclasses import dataclass

from v1700.arc_reveal_knowledge.character_knowledge_bridge import CharacterKnowledgeProseBridge
from v1700.arc_reveal_knowledge.reveal_budget import EpisodeRevealBudget
from v1700.nodes.node2_prose_renderer.contract import SurfaceOnlyContract


@dataclass(frozen=True)
class ProseRenderContract:
    episode_id: str
    character_id: str
    fact_id: str
    surface_contract: dict
    reveal_policy: dict
    knowledge_constraint: dict
    arc_context: dict

    def to_dict(self) -> dict:
        return {
            "episode_id": self.episode_id,
            "character_id": self.character_id,
            "fact_id": self.fact_id,
            "surface_contract": self.surface_contract,
            "reveal_policy": self.reveal_policy,
            "knowledge_constraint": self.knowledge_constraint,
            "arc_context": self.arc_context,
        }


def build_prose_render_contract(
    *,
    episode_id: str,
    character_id: str,
    fact_id: str,
    reveal_budget: EpisodeRevealBudget,
    knowledge_bridge: CharacterKnowledgeProseBridge,
    arc_context: dict,
) -> ProseRenderContract:
    surface_contract = SurfaceOnlyContract()
    surface_contract.assert_valid()
    return ProseRenderContract(
        episode_id=episode_id,
        character_id=character_id,
        fact_id=fact_id,
        surface_contract=surface_contract.to_dict(),
        reveal_policy=reveal_budget.get_policy(episode_id, fact_id).to_dict(),
        knowledge_constraint=knowledge_bridge.constraint_for(character_id, fact_id).to_dict(),
        arc_context=arc_context,
    )
