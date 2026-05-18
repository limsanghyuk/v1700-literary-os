from __future__ import annotations

from v1700.arc_reveal_knowledge.character_knowledge_bridge import CharacterKnowledgeProseBridge
from v1700.arc_reveal_knowledge.knowledge_contracts import KnowledgeLeakageError, KnowledgeStatus
from v1700.arc_reveal_knowledge.prose_contract_bridge import build_prose_render_contract
from v1700.arc_reveal_knowledge.reveal_budget import EpisodeRevealBudget
from v1700.arc_reveal_knowledge.series_arc_planner import SeriesArcPlanner


def run_stage86_arc_reveal_knowledge_smoke() -> dict:
    graph = SeriesArcPlanner(total_episodes=16).plan()
    budget = EpisodeRevealBudget.from_arc_graph(graph)
    knowledge = CharacterKnowledgeProseBridge()
    knowledge.set_status("protagonist", "truth_seed_1", KnowledgeStatus.UNAWARE)
    knowledge.set_status("antagonist", "truth_seed_1", KnowledgeStatus.KNOWS)
    knowledge.set_status("reader", "truth_seed_1", KnowledgeStatus.READER_ONLY)

    leakage_blocked = False
    try:
        knowledge.assert_no_leakage("reader", "truth_seed_1", direct_reference=True)
    except KnowledgeLeakageError:
        leakage_blocked = True

    contract = build_prose_render_contract(
        episode_id="EP01",
        character_id="protagonist",
        fact_id="truth_seed_1",
        reveal_budget=budget,
        knowledge_bridge=knowledge,
        arc_context=graph.get_node("EP01").to_dict(),
    )

    issues: list[str] = []
    if graph.validate_act_structure()["status"] != "pass":
        issues.append("series_arc_act_structure_invalid")
    if len(graph.nodes) != 16:
        issues.append("series_arc_episode_count_not_16")
    if not graph.edges():
        issues.append("causal_plot_graph_has_no_edges")
    if budget.is_allowed("EP01", "truth_seed_1", direct_reveal=True):
        issues.append("episode_reveal_budget_failed_to_block_direct_reveal")
    if not leakage_blocked:
        issues.append("character_knowledge_reader_only_leakage_not_blocked")
    if contract.surface_contract.get("surface_only") is not True:
        issues.append("node2_surface_contract_not_preserved")

    return {
        "stage": "86",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "series_arc": graph.to_dict(),
        "reveal_budget": budget.to_dict(),
        "knowledge_bridge": knowledge.to_dict(),
        "sample_prose_render_contract": contract.to_dict(),
        "provider_default_calls": 0,
        "node2_raw_reveal_access_count": 0,
    }
