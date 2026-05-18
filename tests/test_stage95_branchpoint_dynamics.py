from v1700.narrative_physics.branchpoint_dynamics import BranchpointSurvivalDynamics


def test_stage95_branchpoint_dynamics_reports_missing_branchpoint():
    report = BranchpointSurvivalDynamics().evaluate({"preserved_branchpoints": ["stage25_guardrails"]}).to_dict()

    assert report["status"] == "blocked"
    assert "stage94_provider_evaluation" in report["missing_branchpoints"]
