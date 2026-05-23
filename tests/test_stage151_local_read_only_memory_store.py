from __future__ import annotations

from pathlib import Path

from v1700.gates.stage151_release_gate import run_stage151_release_gate
from v1700.local_memory_store import load_memory_records, run_stage151_local_read_only_memory_store, validate_records


def test_stage151_local_read_only_store_passes() -> None:
    root = Path(__file__).resolve().parents[1]
    result = run_stage151_local_read_only_memory_store(root)
    assert result["status"] == "pass"
    assert result["read_only_store_enabled"] is True
    assert result["store_write_enabled"] is False
    assert result["memory_write_enabled"] is False
    assert result["query_runtime_enabled"] is False
    assert result["provider_default_calls"] == 0
    assert result["node2_raw_reveal_access"] == 0
    assert result["record_count"] >= 5


def test_stage151_loader_validates_fixture() -> None:
    root = Path(__file__).resolve().parents[1]
    records = load_memory_records(root / "samples/stage151_memory_store/project_memory_records.jsonl")
    validation = validate_records(records)
    assert validation["status"] == "pass"
    assert validation["record_count"] == len(records)
    assert validation["checksum_mismatches"] == []
    assert validation["write_policy_enabled"] == []
    assert validation["hidden_payload_leaks"] == []


def test_stage151_release_gate_preserves_boundaries() -> None:
    result = run_stage151_release_gate(Path(__file__).resolve().parents[1])
    assert result["status"] == "pass"
    assert result["provider_default_calls"] == 0
    assert result["node2_raw_reveal_access"] == 0
    assert result["memory_write_enabled"] is False
    assert result["store_write_enabled"] is False
    assert result["runtime_training_enabled"] is False
