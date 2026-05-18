from pathlib import Path

from v1700.graph_nexus.registry import GraphNexusRegistry
from v1700.graph_nexus.tools.context import build_graph_nexus_context
from v1700.graph_nexus.tools.contracts import GraphNexusContextRequest, GraphNexusImpactRequest, GraphNexusQueryRequest
from v1700.graph_nexus.tools.detect_changes import run_graph_nexus_detect_changes
from v1700.graph_nexus.tools.impact import run_graph_nexus_impact
from v1700.graph_nexus.tools.query import run_graph_nexus_query
from v1700.graph_nexus.tools.route_map import build_graph_nexus_route_map
from v1700.graph_nexus.tools.shape_check import run_graph_nexus_shape_check
from v1700.graph_nexus.tools.skill_generator import generate_graph_nexus_skills
from v1700.graph_nexus.tools.tool_map import build_graph_nexus_tool_map
from v1700.graph_nexus.tools.wiki_generator import generate_graph_nexus_wiki
from v1700.sidecars.gitnexus.index_status import get_gitnexus_index_status


ROOT = Path(__file__).resolve().parents[1]


def test_stage72_2_operational_tools_have_python_fallback_outputs():
    query = run_graph_nexus_query(
        ROOT,
        GraphNexusQueryRequest(query="GraphNexus", use_gitnexus=False),
    ).to_dict()
    context = build_graph_nexus_context(
        ROOT,
        GraphNexusContextRequest(target="Node2ProseCompiler", use_gitnexus=False),
    )
    impact = run_graph_nexus_impact(
        ROOT,
        GraphNexusImpactRequest(target="Node2ProseCompiler", use_gitnexus=False),
    )
    changes = run_graph_nexus_detect_changes(ROOT, use_gitnexus=False).to_dict()

    assert query["status"] == "pass"
    assert query["matches"]
    assert context["status"] == "pass"
    assert impact["status"] == "pass"
    assert changes["status"] == "pass"
    assert changes["changed_paths"]


def test_stage72_2_maps_shape_docs_and_lineage_are_available():
    registry = GraphNexusRegistry.build(ROOT)
    skills = generate_graph_nexus_skills(ROOT)
    wiki = generate_graph_nexus_wiki(ROOT)
    route_map = build_graph_nexus_route_map(ROOT).to_dict()
    tool_map = build_graph_nexus_tool_map(ROOT).to_dict()
    shape_check = run_graph_nexus_shape_check(ROOT).to_dict()

    assert registry.stage_lineage_graph.has_stage("STAGE72.2")
    assert skills["status"] == "pass"
    assert wiki["status"] == "pass"
    assert route_map["status"] == "pass"
    assert tool_map["status"] == "pass"
    assert shape_check["status"] == "pass"


def test_gitnexus_index_status_reads_registered_alias_when_available():
    status = get_gitnexus_index_status()

    assert status.alias == "v1700_stage72_3_ascii"
    if status.registered:
        assert "gitnexus_index" in status.path.replace("\\", "/")
