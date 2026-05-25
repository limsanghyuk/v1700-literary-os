from __future__ import annotations

from pathlib import Path

from v1700.rendering_body_contract import run_stage161_rendering_contract
from v1700.gates.stage161_release_gate import run_stage161_release_gate


def test_stage161_rendering_contract_passes() -> None:
    result = run_stage161_rendering_contract(Path(__file__).resolve().parents[1])
    assert result["status"] == "pass"
    assert result["rendering_contract_only"] is True
    assert result["page03_seal_inherited"] is True
    assert result["contract_count"] >= 6
    assert result["provider_default_calls"] == 0
    assert result["provider_generation_count"] == 0
    assert result["render_write_enabled"] is False
    assert result["generation_runtime_enabled"] is False
    assert result["node2_raw_reveal_access"] == 0


def test_stage161_release_gate_preserves_rendering_boundaries() -> None:
    result = run_stage161_release_gate(Path(__file__).resolve().parents[1])
    assert result["status"] == "pass"
    assert result["provider_default_calls"] == 0
    assert result["provider_generation_enabled"] is False
    assert result["runtime_execution_enabled"] is False
    assert result["write_operation_count"] == 0
    assert result["node2_raw_reveal_access"] == 0


def test_stage161_node2_projection_blocks_hidden_render_payloads() -> None:
    result = run_stage161_rendering_contract(Path(__file__).resolve().parents[1])
    rules = result["parts"]["node2_rendering_projection_policy"]["rules"]
    assert any(rule["forbidden_payload"] == "hidden_reveal_payload" and rule["blocked"] is True for rule in rules)
    assert any(rule["forbidden_payload"] == "provider handle" and rule["blocked"] is True for rule in rules)


def test_stage161_write_policy_blocks_generation_and_publication() -> None:
    result = run_stage161_rendering_contract(Path(__file__).resolve().parents[1])
    rules = result["parts"]["rendering_write_policy"]["rules"]
    assert all(rule["default_enabled"] is False for rule in rules)
    assert all(rule["generation_runtime_allowed"] is False for rule in rules)
    assert all(rule["runtime_write_allowed"] is False for rule in rules)


def test_stage161_outputs_release_evidence_files() -> None:
    root = Path(__file__).resolve().parents[1]
    run_stage161_rendering_contract(root)
    expected = [
        "release/current/stage161_rendering_contract_pack/page04_readiness_matrix.json",
        "release/current/stage161_rendering_contract_pack/rendering_contracts.json",
        "release/current/stage161_rendering_contract_pack/rendering_boundary_policy.json",
        "release/current/stage161_rendering_contract_pack/rendering_write_policy.json",
        "release/current/stage161_rendering_contract_pack/node2_rendering_projection_policy.json",
    ]
    assert all((root / rel).exists() for rel in expected)
