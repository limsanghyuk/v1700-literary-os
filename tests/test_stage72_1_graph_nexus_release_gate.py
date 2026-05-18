from pathlib import Path

from v1700.gates.graph_nexus_release_gate import run_graph_nexus_release_gate
from v1700.gates.release_gate import run_release_gate


ROOT = Path(__file__).resolve().parents[1]


def test_graph_nexus_release_gate_passes_without_gitnexus_installation():
    report = run_graph_nexus_release_gate(ROOT)

    assert report["status"] == "pass"
    assert report["gitnexus_optional_only"] is True
    assert report["python_fallback_available"] is True
    assert report["provider_default_calls"] == 0
    assert report["code_graph_available"] is True
    assert report["narrative_graph_available"] is True
    assert report["stage_lineage_graph_available"] is True
    assert report["node2_raw_reveal_access_count"] == 0


def test_stage72_release_gate_includes_graph_nexus_release_gate():
    report = run_release_gate()

    assert report["status"] == "pass"
    assert report["graph_nexus_release_gate"]["status"] == "pass"
