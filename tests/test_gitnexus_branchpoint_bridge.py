
from v1700.lineage.stage83_1_consistency_audit import build_gitnexus_branchpoint_bridge_manifest


def test_gitnexus_branchpoint_bridge_manifest_keeps_gitnexus_optional():
    manifest = build_gitnexus_branchpoint_bridge_manifest()
    assert manifest["status"] == "pass"
    assert manifest["gitnexus_role"] == "optional_sidecar"
    assert manifest["graphnexus_role"] == "CodeGraph + NarrativeGraph + StageLineageGraph"
    bridges = {bridge["bridge_id"]: bridge for bridge in manifest["bridges"]}
    assert "gitnexus_to_codegraph" in bridges
    assert "codegraph_to_branchpoint_logic_graph" in bridges
    assert bridges["stage_lineage_to_release_gate"]["target"] == "Stage83.1ReleaseGate"
