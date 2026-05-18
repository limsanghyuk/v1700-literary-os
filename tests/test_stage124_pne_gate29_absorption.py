from __future__ import annotations

from pathlib import Path

from v1700.gates.stage124_release_gate import run_stage124_release_gate
from v1700.nie.predictive import DebtPredictor, FeedbackLearner, Gate29, PNECore, PreemptiveGate
from v1700.stage124.fixtures import FEEDBACK_RECORDS, PNE_REPAIR_OUTCOMES
from v1700.stage124.orchestrator import run_stage124

ROOT = Path(__file__).resolve().parents[1]


def test_stage124_orchestrator_passes_and_keeps_gate29_secondary():
    result = run_stage124(ROOT)
    assert result["status"] == "pass"
    assert result["absorption_policy"]["gate29_authority_mode"] == "secondary_predictive_gate"
    assert result["absorption_policy"]["gate29_primary_authority_enabled"] is False
    assert result["absorption_policy"]["direct_v555_merge_performed"] is False
    assert result["absorption_policy"]["release_gate_runtime_training_enabled"] is False


def test_pne_core_feature_vector_matches_v555_pattern_library_concept():
    core = PNECore()
    core.ingest_outcomes(PNE_REPAIR_OUTCOMES)
    fv = core.feature_vector("unresolved_secret")
    assert len(fv) == 4
    assert fv[0] == core.category_stats("unresolved_secret").success_rate()
    assert core.total_ingested() == len(PNE_REPAIR_OUTCOMES)


def test_debt_predictor_uses_heuristic_fallback_without_runtime_training():
    core = PNECore()
    core.ingest_outcomes(PNE_REPAIR_OUTCOMES)
    predictor = DebtPredictor(core, runtime_training_enabled=False)
    train_result = predictor.train(core)
    assert not any(train_result.values())
    report = predictor.predict("s1", current_severity=0.95, horizon=3)
    assert report.runtime_training_enabled is False
    assert all(p.mode == "heuristic_fallback" for p in report.predictions)
    assert 0.0 <= report.max_probability() <= 1.0


def test_preemptive_gate_allows_low_risk_and_blocks_high_risk():
    core = PNECore(); core.ingest_outcomes(PNE_REPAIR_OUTCOMES)
    gate = PreemptiveGate(DebtPredictor(core), threshold=0.60, horizon=3)
    low = gate.evaluate("low", current_severity=0.10)
    high = gate.evaluate("high", current_severity=0.96)
    assert low.status == "pass"
    assert not low.blocked
    assert high.status == "blocked"
    assert high.blocked
    assert high.max_probability >= 0.60


def test_feedback_learner_precision_target_met_without_retraining():
    learner = FeedbackLearner(threshold=0.60, precision_target=0.70, runtime_retraining_enabled=False)
    learner.record_many(list(FEEDBACK_RECORDS))
    report = learner.report()
    assert report.status == "pass"
    assert report.metrics.precision() == 0.75
    assert report.runtime_retraining_triggered is False


def test_gate29_passes_low_risk_and_blocks_high_risk_case():
    core = PNECore(); core.ingest_outcomes(PNE_REPAIR_OUTCOMES)
    gate = PreemptiveGate(DebtPredictor(core), threshold=0.60, horizon=3)
    learner = FeedbackLearner(runtime_retraining_enabled=False)
    learner.record_many(list(FEEDBACK_RECORDS))
    feedback = learner.report()
    low = Gate29().evaluate(gate.evaluate("low", 0.10), feedback)
    high = Gate29().evaluate(gate.evaluate("high", 0.96), feedback)
    assert low.status == "pass"
    assert low.authority_mode == "secondary_predictive_gate"
    assert high.status == "blocked"


def test_stage124_release_gate_passes():
    result = run_stage124_release_gate(ROOT)
    assert result["status"] == "pass"
    assert result["checks"]["gate29_secondary_predictive_gate"]["status"] == "pass"
    assert result["checks"]["runtime_training_disabled"]["status"] == "pass"
    assert result["pne_runtime_training_count"] == 0
