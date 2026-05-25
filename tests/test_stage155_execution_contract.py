from __future__ import annotations

from pathlib import Path

from v1700.execution_body_contract import run_stage155_execution_contract
from v1700.gates.stage155_release_gate import run_stage155_release_gate

ROOT = Path(__file__).resolve().parents[1]


def test_stage155_execution_contract_passes() -> None:
    result = run_stage155_execution_contract(ROOT)
    assert result["status"] == "pass"
    assert result["execution_contract_only"] is True
    assert result["page02_seal_inherited"] is True
    assert result["stage156_local_execution_packet_store_ready"] is True
    assert result["contract_count"] >= 6


def test_stage155_forbids_runtime_privilege_expansion() -> None:
    result = run_stage155_execution_contract(ROOT)
    assert result["runtime_execution_enabled"] is False
    assert result["generation_runtime_enabled"] is False
    assert result["provider_execution_enabled"] is False
    assert result["memory_write_enabled"] is False
    assert result["execution_write_enabled"] is False
    assert result["canon_mutation_enabled"] is False
    assert result["auto_repair_apply_enabled"] is False


def test_stage155_boundary_counters_are_zero() -> None:
    result = run_stage155_execution_contract(ROOT)
    assert result["provider_default_calls"] == 0
    assert result["live_provider_call_count_in_release_gate"] == 0
    assert result["node2_raw_reveal_access"] == 0
    assert result["node2_hidden_execution_payload_access"] == 0
    assert result["boundary_violation_count"] == 0
    assert result["raw_manuscript_provider_leakage"] == 0
    assert result["raw_manuscript_cross_project_leakage"] == 0
    assert result["credential_leakage"] == 0


def test_stage155_release_gate_passes() -> None:
    result = run_stage155_release_gate(ROOT)
    assert result["status"] == "pass"
    assert result["provider_default_calls"] == 0
    assert result["node2_raw_reveal_access"] == 0
    assert result["runtime_execution_enabled"] is False
    assert result["memory_write_enabled"] is False


def test_stage155_blocks_node2_forbidden_execution_payloads() -> None:
    result = run_stage155_execution_contract(ROOT)
    node2 = result["parts"]["node2_execution_projection_policy"]
    forbidden = {rule["forbidden_payload"] for rule in node2["rules"]}
    assert "provider_execution_handle" in forbidden
    assert "raw_manuscript_payload" in forbidden
    assert "learning_payload" in forbidden
    assert all(rule["blocked"] is True for rule in node2["rules"])
