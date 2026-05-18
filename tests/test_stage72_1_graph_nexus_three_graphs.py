from pathlib import Path

from v1700.graph_nexus.registry import GraphNexusRegistry


ROOT = Path(__file__).resolve().parents[1]


def test_graph_nexus_builds_code_narrative_and_stage_lineage_graphs():
    registry = GraphNexusRegistry.build(ROOT)

    assert registry.code_graph.nodes
    assert registry.narrative_graph.nodes
    assert registry.stage_lineage_graph.nodes
    assert registry.stage_lineage_graph.has_stage("STAGE61-66")
    assert registry.stage_lineage_graph.has_stage("STAGE72.1")

    packet = registry.context_packet("Node2ProseCompiler").to_dict()
    assert packet["code_summary"]["available"] is True
    assert packet["narrative_summary"]["available"] is True
    assert packet["lineage_summary"]["stage72_1_present"] is True
