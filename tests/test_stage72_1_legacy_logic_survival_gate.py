from pathlib import Path

from v1700.gates.legacy_logic_survival_gate import run_legacy_logic_survival_gate


ROOT = Path(__file__).resolve().parents[1]


def test_legacy_graph_intelligence_concepts_survive_as_optional_layer():
    report = run_legacy_logic_survival_gate(ROOT)

    assert report["status"] == "pass"
    assert report["missing_concepts"] == []
    assert report["current_status"] == "restored_as_optional_graphnexus_layer"
