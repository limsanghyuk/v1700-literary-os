from __future__ import annotations

from pathlib import Path

from v1700.memory_body_contract import run_stage150_memory_contract
from v1700.gates.stage150_release_gate import run_stage150_release_gate


def test_stage150_memory_contract_passes() -> None:
    result = run_stage150_memory_contract(Path(__file__).resolve().parents[1])
    assert result["status"] == "pass"
    assert result["memory_contract_only"] is True
    assert result["provider_default_calls"] == 0
    assert result["node2_raw_reveal_access"] == 0
    assert result["memory_write_enabled"] is False
    assert result["runtime_training_enabled"] is False


def test_stage150_release_gate_preserves_boundaries() -> None:
    result = run_stage150_release_gate(Path(__file__).resolve().parents[1])
    assert result["status"] == "pass"
    assert result["provider_default_calls"] == 0
    assert result["node2_raw_reveal_access"] == 0
    assert result["memory_write_enabled"] is False
    assert result["runtime_training_enabled"] is False
