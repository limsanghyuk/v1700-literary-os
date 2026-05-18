import pytest

from v1700.arc_reveal_knowledge.arc_contracts import ArcAct, ArcPlotEdgeType
from v1700.arc_reveal_knowledge.character_knowledge_bridge import CharacterKnowledgeProseBridge
from v1700.arc_reveal_knowledge.knowledge_contracts import (
    KnowledgeLeakageError,
    KnowledgeStatus,
    UnawarenessViolationError,
)
from v1700.arc_reveal_knowledge.prose_contract_bridge import build_prose_render_contract
from v1700.arc_reveal_knowledge.reveal_budget import (
    EpisodeRevealBudget,
    RevealForeshadowOnlyError,
    RevealPolicy,
)
from v1700.arc_reveal_knowledge.series_arc_planner import SeriesArcPlanner
from v1700.arc_reveal_knowledge.stage86_smoke import run_stage86_arc_reveal_knowledge_smoke
from v1700.gates.release_gate import run_release_gate
from v1700.gates.stage86_release_gate import run_stage86_release_gate


def test_stage86_series_arc_planner_creates_four_act_sixteen_episode_graph():
    graph = SeriesArcPlanner(total_episodes=16).plan()

    assert graph.validate_act_structure()["status"] == "pass"
    assert graph.validate_act_structure()["episode_count"] == 16
    assert {node.act for node in graph.ordered_nodes()} == {ArcAct.GI, ArcAct.SEUNG, ArcAct.JEON, ArcAct.GYEOL}
    assert graph.tension_curve()[0] < max(graph.tension_curve())


def test_stage86_causal_plot_graph_connects_causality_foreshadow_and_callbacks():
    graph = SeriesArcPlanner(total_episodes=16).plan()

    assert len(graph.edges(ArcPlotEdgeType.CAUSAL)) >= 15
    assert len(graph.edges(ArcPlotEdgeType.FORESHADOW)) >= 4
    assert len(graph.edges(ArcPlotEdgeType.CALLBACK)) >= 4
    assert len(graph.edges(ArcPlotEdgeType.EMOTIONAL_ESCALATION)) >= 3


def test_stage86_episode_reveal_budget_blocks_direct_early_reveal_but_allows_foreshadow():
    graph = SeriesArcPlanner(total_episodes=16).plan()
    budget = EpisodeRevealBudget.from_arc_graph(graph)

    with pytest.raises(RevealForeshadowOnlyError):
        budget.assert_allowed("EP01", "truth_seed_1", direct_reveal=True)
    assert budget.is_allowed("EP01", "truth_seed_1", direct_reveal=False)
    assert budget.get_policy("EP01", "truth_seed_1").policy == RevealPolicy.FORESHADOW_ONLY


def test_stage86_character_knowledge_bridge_prevents_knowledge_leakage():
    bridge = CharacterKnowledgeProseBridge()
    bridge.set_status("protagonist", "truth_seed_1", KnowledgeStatus.UNAWARE)
    bridge.set_status("reader", "truth_seed_1", KnowledgeStatus.READER_ONLY)

    with pytest.raises(UnawarenessViolationError):
        bridge.assert_no_leakage("protagonist", "truth_seed_1", direct_reference=True)
    with pytest.raises(KnowledgeLeakageError):
        bridge.assert_no_leakage("reader", "truth_seed_1", direct_reference=True)
    assert "truth_seed_1" in bridge.blocked_facts_for("protagonist")


def test_stage86_prose_contract_preserves_node2_surface_only_boundary():
    graph = SeriesArcPlanner(total_episodes=16).plan()
    budget = EpisodeRevealBudget.from_arc_graph(graph)
    bridge = CharacterKnowledgeProseBridge()
    bridge.set_status("protagonist", "truth_seed_1", KnowledgeStatus.UNAWARE)

    contract = build_prose_render_contract(
        episode_id="EP01",
        character_id="protagonist",
        fact_id="truth_seed_1",
        reveal_budget=budget,
        knowledge_bridge=bridge,
        arc_context=graph.get_node("EP01").to_dict(),
    )

    assert contract.surface_contract["surface_only"] is True
    assert contract.surface_contract["allow_reveal_change"] is False
    assert contract.reveal_policy["policy"] == "foreshadow_only"
    assert contract.knowledge_constraint["render_mode"] == "do_not_name_fact"


def test_stage86_smoke_and_release_gate_pass_without_provider_or_reveal_regression():
    smoke = run_stage86_arc_reveal_knowledge_smoke()
    gate = run_stage86_release_gate()

    assert smoke["status"] == "pass"
    assert gate["status"] == "pass"
    assert gate["provider_default_calls"] == 0
    assert gate["node2_raw_reveal_access_count"] == 0


def test_main_release_gate_includes_stage86_when_active():
    result = run_release_gate()

    assert result["status"] == "pass"
    assert result["stage86_release_gate"]["status"] == "pass"
