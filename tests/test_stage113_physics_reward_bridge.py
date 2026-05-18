from pathlib import Path

from v1700.gates.stage113_release_gate import run_stage113_release_gate
from v1700.nie.reward.mae_result_fixture import build_stage113_feature_vector, build_stage113_fixture_mae_result
from v1700.nie.reward.physics_reward_bridge import PhysicsRewardBridge
from v1700.stage113.orchestrator import run_stage113


def test_physics_reward_bridge_weighted_reward_and_baseline() -> None:
    mae = build_stage113_fixture_mae_result()
    signal = PhysicsRewardBridge().calculate_reward_signal(mae)
    assert signal.reward == 0.7855
    assert signal.advantage == 0.2855
    assert signal.baseline_after == 0.514275
    assert signal.provider_call_count == 0
    assert signal.physics_reward_bridge_llm_call_count == 0


def test_physics_reward_bridge_proposes_bounded_updates() -> None:
    mae = build_stage113_fixture_mae_result()
    bridge = PhysicsRewardBridge()
    signal = bridge.calculate_reward_signal(mae)
    proposals = bridge.propose_coefficient_updates(signal, build_stage113_feature_vector(mae))
    assert len(proposals) == 4
    assert all(abs(p.delta) <= 0.03 for p in proposals)
    assert bridge.drift_guard(proposals)["status"] == "pass"


def test_stage113_orchestrator_and_release_gate_pass() -> None:
    root = Path(__file__).resolve().parents[1]
    stage = run_stage113(root)
    assert stage["status"] == "pass"
    assert stage["physics_reward_bridge_llm_call_count"] == 0
    assert stage["mae_live_provider_call_count"] == 0
    gate = run_stage113_release_gate(root)
    assert gate["status"] == "pass"
    assert gate["checks"]["mae_reward_contract_pass"]["status"] == "pass"
