from v1700.creative_arbitration.ensemble_orchestrator import run_creative_arbitration


def test_stage105_creative_arbitration_has_final_v1700_authority():
    report = run_creative_arbitration()
    assert report["status"] == "pass"
    decisions = report["arbitration"]["decisions"]
    assert {d["mode"] for d in decisions} == {"PROSE", "SCENARIO", "HYBRID"}
    assert all(d["provider_call_count"] == 0 for d in decisions)
    assert all("V1700" in d["final_authority"] for d in decisions)
