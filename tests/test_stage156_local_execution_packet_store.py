from __future__ import annotations

from pathlib import Path

from v1700.local_execution_packet_store.loader import load_execution_packets, validate_execution_packet_store
from v1700.local_execution_packet_store import run_stage156_local_execution_packet_store
from v1700.gates.stage156_release_gate import run_stage156_release_gate

ROOT = Path(__file__).resolve().parents[1]
STORE = ROOT / "samples/stage156_execution_packet_store/execution_packets.jsonl"


def test_stage156_packet_store_fixture_validates() -> None:
    validation = validate_execution_packet_store(STORE)
    assert validation["status"] == "pass"
    assert validation["packet_count"] >= 6
    assert all(entry["checksum"] == entry["expected_checksum"] for entry in validation["checksum_index"])


def test_stage156_packets_are_read_only_and_dry_run() -> None:
    packets = load_execution_packets(STORE)
    assert packets
    assert all(packet["write_policy"] == "READ_ONLY_DISABLED_WRITE" for packet in packets)
    assert all(packet["execution_mode"] == "DRY_RUN_ONLY" for packet in packets)


def test_stage156_report_passes_and_blocks_runtime_privilege() -> None:
    result = run_stage156_local_execution_packet_store(ROOT)
    assert result["status"] == "pass"
    assert result["packet_count"] >= 6
    assert result["runtime_execution_enabled"] is False
    assert result["store_write_enabled"] is False
    assert result["provider_default_calls"] == 0
    assert result["node2_raw_reveal_access"] == 0


def test_stage156_release_gate_passes() -> None:
    result = run_stage156_release_gate(ROOT)
    assert result["status"] == "pass"
    assert result["stage156"]["packet_count"] >= 6
    assert result["store_write_enabled"] is False
    assert result["runtime_execution_enabled"] is False


def test_stage156_tampered_checksum_blocks(tmp_path: Path) -> None:
    store = tmp_path / "execution_packets.jsonl"
    packet = load_execution_packets(STORE)[0]
    packet["payload_summary"] = "tampered"
    import json
    store.write_text(json.dumps(packet, ensure_ascii=False) + "\n", encoding="utf-8")
    validation = validate_execution_packet_store(store)
    assert validation["status"] == "blocked"
    assert any(issue.startswith("checksum_mismatch") for issue in validation["issues"])
