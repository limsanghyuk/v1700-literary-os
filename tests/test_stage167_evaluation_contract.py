from __future__ import annotations

from pathlib import Path

from v1700.evaluation_body_contract import run_stage167_evaluation_contract
from v1700.gates.stage167_release_gate import run_stage167_release_gate


def test_stage167_evaluation_contract_passes() -> None:
    result = run_stage167_evaluation_contract(Path(__file__).resolve().parents[1])
    assert result["status"] == "pass"
    assert result["evaluation_contract_only"] is True
    assert result["stage166_page04_seal_inherited"] is True
    assert result["contract_count"] >= 12
    assert result["rubric_weights_valid"] is True
    assert result["thresholds_explicit"] is True
    assert result["provider_default_calls"] == 0
    assert result["provider_evaluation_enabled"] is False
    assert result["evaluation_write_enabled"] is False
    assert result["node2_raw_reveal_access"] == 0


def test_stage167_release_gate_preserves_evaluation_boundaries() -> None:
    result = run_stage167_release_gate(Path(__file__).resolve().parents[1])
    assert result["status"] == "pass"
    assert result["provider_default_calls"] == 0
    assert result["provider_evaluation_enabled"] is False
    assert result["evaluation_write_enabled"] is False
    assert result["memory_write_enabled"] is False
    assert result["write_operation_count"] == 0
    assert result["node2_raw_reveal_access"] == 0


def test_stage167_boundary_criteria_are_non_overridable() -> None:
    result = run_stage167_evaluation_contract(Path(__file__).resolve().parents[1])
    criteria = result["parts"]["evaluation_boundary_policy"]["boundary_criteria"]
    assert all(item["overridable"] is False for item in criteria)


def test_stage167_rubric_weights_sum_to_one() -> None:
    result = run_stage167_evaluation_contract(Path(__file__).resolve().parents[1])
    rubric = result["parts"]["evaluation_rubric_catalog"]
    assert rubric["weight_sum_valid"] is True
    assert rubric["weight_sum"] == 1.0


def test_stage167_outputs_release_evidence_files() -> None:
    root = Path(__file__).resolve().parents[1]
    run_stage167_evaluation_contract(root)
    expected = [
        "release/current/stage167_evaluation_contract_pack/page05_readiness_matrix.json",
        "release/current/stage167_evaluation_contract_pack/evaluation_contract_catalog.json",
        "release/current/stage167_evaluation_contract_pack/evaluation_rubric_catalog.json",
        "release/current/stage167_evaluation_contract_pack/evaluation_boundary_policy.json",
        "release/current/stage167_evaluation_contract_pack/evaluation_authority_policy.json",
        "release/current/stage167_evaluation_contract_pack/stage168_entry_criteria.json",
    ]
    assert all((root / rel).exists() for rel in expected)
