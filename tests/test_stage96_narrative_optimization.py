from v1700.narrative_optimization.optimizer import run_narrative_physics_optimization


def test_stage96_narrative_optimization_drift_guard_passes():
    report = run_narrative_physics_optimization()
    assert report["status"] == "pass"
    assert report["drift_guard"]["status"] == "pass"
    assert report["drift_guard"]["max_single_update_delta"] <= 0.05
    assert report["learned_coefficients"]["branchpoint_survival_weight"] >= report["baseline_coefficients"]["branchpoint_survival_weight"]
    assert report["learned_coefficients"]["surface_safety_weight"] >= report["baseline_coefficients"]["surface_safety_weight"]
    assert report["learned_coefficients"]["leakage_penalty_weight"] >= report["baseline_coefficients"]["leakage_penalty_weight"]
