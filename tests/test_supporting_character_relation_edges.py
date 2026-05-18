
from v1700.lineage.stage83_1_consistency_audit import build_organic_relation_graph_manifest_v2


def test_supporting_character_relation_edges_never_render_none_to_none():
    graph = build_organic_relation_graph_manifest_v2()
    edge_text = "\n".join(graph["edge_texts"])
    assert "None --" not in edge_text
    assert "--> None" not in edge_text
    assert "UNSPECIFIED_SOURCE" not in edge_text
    assert "UNSPECIFIED_TARGET" not in edge_text
