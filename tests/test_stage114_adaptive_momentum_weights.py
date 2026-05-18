from pathlib import Path

from v1700.gates.stage114_release_gate import run_stage114_release_gate
from v1700.nie.emotion.adaptive_momentum_weights import AdaptiveMomentumWeights, build_amw_inputs
from v1700.nie.emotion.amw_report import build_stage114_amw_report
from v1700.nie.emotion.genre_alpha_table import ALPHA_MAX, ALPHA_MIN, initial_alpha_state
from v1700.nie.reward.mae_result_fixture import build_stage113_fixture_mae_result
from v1700.stage114.orchestrator import run_stage114


def test_amw_updates_are_bounded_and_use_mae_dimensions() -> None:
    mae = build_stage113_fixture_mae_result()
    before = initial_alpha_state("melodrama", 0.56)
    amw = AdaptiveMomentumWeights(genre="melodrama", alpha=before.copy())
    updates = amw.update_many(build_amw_inputs(mae.dimension_scores.to_dict(), genre="melodrama", act_pos=0.56))
    assert len(updates) == 4
    assert all(ALPHA_MIN <= update.alpha_after <= ALPHA_MAX for update in updates)
    assert all(abs(update.shift) <= 0.03 for update in updates)
    assert {u.mae_dim_score for u in updates} == {0.78, 0.72, 0.61, 0.69}
    assert amw.drift_guard(updates).status == "pass"


def test_stage114_report_contains_guarded_alpha_state() -> None:
    report = build_stage114_amw_report()
    assert report["status"] == "pass"
    assert report["drift_guard"]["status"] == "pass"
    assert report["provider_call_count"] == 0
    assert report["physics_reward_bridge_llm_call_count"] == 0
    assert set(report["alpha_after"]) == {"tension", "sympathy", "dread", "catharsis"}


def test_stage114_orchestrator_and_release_gate_pass() -> None:
    root = Path(__file__).resolve().parents[1]
    stage = run_stage114(root)
    assert stage["status"] == "pass"
    assert stage["mae_live_provider_call_count"] == 0
    gate = run_stage114_release_gate(root)
    assert gate["status"] == "pass"
    assert gate["checks"]["amw_alpha_bounds_pass"]["status"] == "pass"
    assert gate["checks"]["amw_drift_guard_pass"]["status"] == "pass"
