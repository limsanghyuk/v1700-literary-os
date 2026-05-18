from pathlib import Path

from v1700.stage101.orchestrator import run_stage101_0_cross_lineage_preflight

ROOT = Path(__file__).resolve().parents[1]


def test_stage101_cross_lineage_preflight_locks_stage100_and_source_policy():
    report = run_stage101_0_cross_lineage_preflight(ROOT)
    assert report["status"] == "pass"
    assert report["stage100_baseline_status"] == "pass"
    assert report["v430_untraced_merge"] is False
    assert report["absorption_mode"] in {"fixture_contract_validation", "gitnexus_impact_then_contract_adapter"}

