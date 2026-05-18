from pathlib import Path

from v1700.stage99.impact_baseline import run_stage99_0_gitnexus_impact_baseline

ROOT = Path(__file__).resolve().parents[1]


def test_stage99_0_builds_gitnexus_impact_baseline_without_orphan_critical_nodes():
    report = run_stage99_0_gitnexus_impact_baseline(ROOT)
    assert report["status"] == "pass"
    assert report["stage"] == "99.0"
    assert report["baseline_stage"] == "98"
    assert report["orphan_nodes"] == []
    assert report["broken_edges"] == []
    assert report["branchpoint_survival_status"] == "pass"
    assert (ROOT / "release/current/stage99_gitnexus_pack/impact_nodes.json").exists()
