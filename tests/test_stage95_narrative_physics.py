from v1700.gates.release_gate import run_release_gate
from v1700.gates.stage95_release_gate import run_stage95_release_gate
from v1700.narrative_physics.belief_state import BeliefStateEngine
from v1700.narrative_physics.branchpoint_dynamics import BranchpointSurvivalDynamics
from v1700.narrative_physics.engine import NativeNarrativePhysicsEngine, run_stage95_narrative_physics_smoke
from v1700.narrative_physics.reveal_entropy import RevealEntropyBudgetEngine
from v1700.narrative_physics.scene_energy import SceneEnergyConservationAudit
from v1700.narrative_physics.surface_transform import Node2SurfaceTransformGuard


def test_stage95_state_tensor_builds_episode_scene_matrix():
    report = NativeNarrativePhysicsEngine().run(episode_count=16, scenes_per_episode=10).to_dict()

    assert report["status"] == "pass"
    assert report["tensor"]["matrix_shape"] == [16, 10, 12]
    assert len(report["tensor"]["vectors"]) == 160
    assert "branchpoint_risk" in report["tensor"]["dimensions"]


def test_stage95_belief_state_blocks_reader_only_surface_leakage():
    assert BeliefStateEngine().leakage_count("READER_ONLY: hidden fact") == 1

    report = run_stage95_narrative_physics_smoke()
    vector = report["belief_vectors"][0]
    assert vector["reader_only_fact_count"] > 0
    assert vector["leakage_count"] == 0
    assert vector["surface_safe"] is True


def test_stage95_reveal_entropy_penalizes_premature_reveal():
    low_entropy = {
        "episodes": [
            {"episode_id": "E01", "blocked_direct_reveal_count": 0, "reveal_policy_count": 4, "scenes": []},
            {"episode_id": "E02", "blocked_direct_reveal_count": 0, "reveal_policy_count": 4, "scenes": []},
        ]
    }
    report = RevealEntropyBudgetEngine().calculate(low_entropy).to_dict()

    assert report["premature_reveal_penalty"] > 0
    assert report["status"] == "pass"


def test_stage95_emotional_momentum_scene_energy_motif_and_curiosity_pass():
    report = run_stage95_narrative_physics_smoke()

    assert report["emotional_momentum"]["status"] == "pass"
    assert report["scene_energy"]["status"] == "pass"
    assert report["scene_energy"]["dead_scene_count"] == 0
    assert report["motif_residue"]["status"] == "pass"
    assert report["motif_residue"]["payoff_count"] > 0
    assert report["curiosity_gradient"]["status"] == "pass"
    assert report["curiosity_gradient"]["finale_rise"] > 0


def test_stage95_scene_energy_detects_dead_scene():
    bad = {"episodes": [{"scenes": [{"quality_score": 5.0}]}]}

    report = SceneEnergyConservationAudit().audit(bad).to_dict()
    assert report["status"] == "blocked"
    assert report["dead_scene_count"] == 1


def test_stage95_surface_guard_blocks_raw_reveal_and_internal_markers():
    report = Node2SurfaceTransformGuard().audit("RAW_REVEAL: fact INTERNAL_MARKER: route").to_dict()

    assert report["status"] == "blocked"
    assert report["node2_raw_reveal_access_count"] == 1
    assert report["internal_marker_leakage_count"] == 1


def test_stage95_branchpoint_survival_preserves_stage25_to_94():
    report = BranchpointSurvivalDynamics().evaluate({}).to_dict()

    assert report["status"] == "pass"
    assert "stage94_provider_evaluation" in report["preserved_branchpoints"]
    assert report["missing_branchpoints"] == []


def test_stage95_release_gate_passes_and_inherits_stage94():
    gate = run_stage95_release_gate()

    assert gate["status"] == "pass"
    assert gate["checks"]["stage94_release_gate"]["status"] == "pass"
    assert gate["provider_default_calls"] == 0
    assert gate["live_provider_call_count"] == 0
    assert gate["node2_raw_reveal_access_count"] == 0


def test_main_release_gate_includes_stage95_when_active():
    result = run_release_gate()

    assert result["status"] == "pass"
    assert result["stage95_release_gate"]["status"] == "pass"
