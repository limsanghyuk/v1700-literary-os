from __future__ import annotations

from pathlib import Path

from v1700.gates.stage122_release_gate import run_stage122_release_gate
from v1700.nie.stability import AgentCalibrator, MetaLearnerSkeleton, NILStabilityModule, TIdealLearner, TemporalCIMAdapter
from v1700.stage122.fixtures import AGENT_RELIABILITY, MAE_AGENT_WEIGHTS, TEMPORAL_CIM_VOLATILITY, TEMPORAL_ROLE_TIERS
from v1700.stage122.orchestrator import run_stage122

ROOT = Path(__file__).resolve().parents[1]


def test_stage122_orchestrator_passes_and_blocks_direct_merge():
    result = run_stage122(ROOT)
    assert result["status"] == "pass"
    assert result["absorption_policy"]["direct_v545_v555_merge_allowed"] is False
    assert result["absorption_policy"]["v525_alpha_relaxation_adopted"] is False
    assert result["absorption_policy"]["gate28_authority_enabled"] is False
    assert result["absorption_policy"]["gate29_authority_enabled"] is False


def test_agent_calibrator_is_bounded_and_normalized():
    report = AgentCalibrator().calibrate(MAE_AGENT_WEIGHTS, AGENT_RELIABILITY)
    assert report.status == "pass"
    assert report.max_shift <= 0.05
    assert abs(report.normalized_sum - 1.0) < 1e-9
    assert all(0.10 <= value <= 0.45 for value in report.weights_after.values())


def test_temporal_cim_adapter_detects_stable_roles():
    report = TemporalCIMAdapter().evaluate(TEMPORAL_ROLE_TIERS, TEMPORAL_CIM_VOLATILITY)
    assert report.status == "pass"
    assert report.mean_volatility <= 0.25
    assert report.role_continuity >= 0.60


def test_meta_learner_is_proposal_only():
    report = MetaLearnerSkeleton().propose([{"proposal_id": "x"}])
    assert report.status == "pass"
    assert report.mode == "proposal_only"
    assert report.applied_count == 0
    assert report.provider_calls == 0
    assert report.runtime_training_performed is False


def test_stage122_release_gate_passes():
    result = run_stage122_release_gate(ROOT)
    assert result["status"] == "pass"
    assert result["checks"]["stage120_gate25_primary_authority_preserved"]["status"] == "pass"
    assert result["checks"]["v525_alpha_relaxation_not_adopted"]["status"] == "pass"
    assert result["provider_default_calls"] == 0
