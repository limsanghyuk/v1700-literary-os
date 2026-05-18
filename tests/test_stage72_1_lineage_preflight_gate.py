from pathlib import Path

from v1700.gates.lineage_preflight_gate import run_lineage_preflight_gate


ROOT = Path(__file__).resolve().parents[1]


def test_lineage_preflight_requires_graph_intelligence_and_current_stage():
    report = run_lineage_preflight_gate(ROOT)

    assert report["status"] == "pass"
    assert report["missing_stages"] == []
    assert report["graph_intelligence_lineage_present"] is True
