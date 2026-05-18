from __future__ import annotations

from v1700.nie.reward.contracts import PhysicsRewardBridgeReport
from v1700.nie.reward.mae_result_fixture import build_stage113_feature_vector, build_stage113_fixture_mae_result
from v1700.nie.reward.physics_reward_bridge import PhysicsRewardBridge


def build_stage113_reward_bridge_report() -> dict:
    mae = build_stage113_fixture_mae_result()
    bridge = PhysicsRewardBridge()
    signal = bridge.calculate_reward_signal(mae)
    proposals = bridge.propose_coefficient_updates(signal, build_stage113_feature_vector(mae))
    drift_guard = bridge.drift_guard(proposals)
    issues: list[str] = []
    if signal.provider_call_count != 0:
        issues.append("mae_live_provider_call_count_nonzero")
    if signal.physics_reward_bridge_llm_call_count != 0:
        issues.append("physics_reward_bridge_llm_call_count_nonzero")
    if drift_guard["status"] != "pass":
        issues.append("reward_bridge_drift_guard_blocked")
    if not proposals:
        issues.append("coefficient_update_proposals_missing")
    report = PhysicsRewardBridgeReport(
        stage="113",
        status="pass" if not issues else "blocked",
        mae_result=mae,
        reward_signal=signal,
        coefficient_update_proposals=proposals,
        drift_guard=drift_guard,
        issues=tuple(issues),
    )
    return report.to_dict()
