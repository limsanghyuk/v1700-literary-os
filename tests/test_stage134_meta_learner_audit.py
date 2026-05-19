from __future__ import annotations

from pathlib import Path

from v1700.gates.stage134_release_gate import run_stage134_release_gate
from v1700.meta_learner_audit import run_stage134_meta_learner_audit
from v1700.meta_learner_audit.audit import AUDIT_MODE, audit_stage133_tensor_report
from v1700.stage133 import run_stage133

ROOT = Path(__file__).resolve().parents[1]


def test_stage134_audit_report_passes() -> None:
    result = run_stage134_meta_learner_audit(ROOT)
    assert result["status"] == "pass"
    assert result["mode"] == AUDIT_MODE
    assert result["audit_only"] is True
    assert result["case_count"] == 5


def test_stage134_never_trains_or_mutates() -> None:
    result = run_stage134_meta_learner_audit(ROOT)
    assert result["runtime_training_enabled"] is False
    assert result["active_meta_learning_enabled"] is False
    assert result["model_weight_update_count"] == 0
    assert result["training_allowed_count"] == 0
    assert result["mutation_allowed_count"] == 0
    assert result["active_learning_allowed_count"] == 0
    assert result["auto_repair_mutation_count"] == 0


def test_stage134_preserves_provider_zero_node2_and_canon_boundaries() -> None:
    result = run_stage134_meta_learner_audit(ROOT)
    assert result["provider_default_calls"] == 0
    assert result["live_provider_call_count_in_release_gate"] == 0
    assert result["node2_raw_reveal_access"] == 0
    assert result["raw_manuscript_provider_leakage"] == 0
    assert result["raw_manuscript_cross_project_leakage"] == 0
    assert result["canon_auto_resolution_count"] == 0
    assert result["cross_project_write_allowed"] is False


def test_stage134_routes_true_contradiction_to_review_recommendation() -> None:
    audit = audit_stage133_tensor_report(run_stage133(ROOT))
    true_case = next(case for case in audit.cases if case.source_classification == "true_contradiction")
    assert true_case.recommendation == "RECOMMEND_REVIEW"
    assert true_case.writer_review_required is True
    assert true_case.training_allowed is False
    assert true_case.mutation_allowed is False


def test_stage134_preflight_and_release_gate_pass() -> None:
    result = run_stage134_meta_learner_audit(ROOT)
    preflight = result["parts"]["gitnexus_preflight"]
    assert preflight["python_fallback"]["status"] == "PASS"
    assert all(preflight["survival_matrix"].values())
    gate = run_stage134_release_gate(ROOT)
    assert gate["status"] == "pass"
    assert gate["checks"]["audit_only_mode_pass"]["status"] == "pass"
