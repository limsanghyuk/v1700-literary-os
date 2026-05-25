from __future__ import annotations

import json
from pathlib import Path

from v1700.local_render_packet_store.loader import load_render_packets, validate_render_packet_store
from v1700.local_render_packet_store import run_stage162_local_render_packet_store
from v1700.gates.stage162_release_gate import run_stage162_release_gate

ROOT = Path(__file__).resolve().parents[1]
STORE = ROOT / "samples/stage162_render_packet_store/render_packets.jsonl"


def test_stage162_render_packet_store_fixture_validates() -> None:
    validation = validate_render_packet_store(STORE)
    assert validation["status"] == "pass"
    assert validation["packet_count"] >= 6
    assert all(entry["checksum"] == entry["expected_checksum"] for entry in validation["checksum_index"])


def test_stage162_packets_are_read_only_and_dry_run_render() -> None:
    packets = load_render_packets(STORE)
    assert packets
    assert all(packet["write_policy"] == "READ_ONLY_DISABLED_WRITE" for packet in packets)
    assert all(packet["render_mode"] == "DRY_RUN_RENDER_ONLY" for packet in packets)
    assert all(packet["boundary_level"] == "NODE2_SURFACE_SAFE" for packet in packets)


def test_stage162_report_passes_and_blocks_runtime_privilege() -> None:
    result = run_stage162_local_render_packet_store(ROOT)
    assert result["status"] == "pass"
    assert result["render_packet_count"] >= 6
    assert result["rendering_runtime_enabled"] is False
    assert result["generation_runtime_enabled"] is False
    assert result["store_write_enabled"] is False
    assert result["provider_default_calls"] == 0
    assert result["node2_raw_reveal_access"] == 0


def test_stage162_release_gate_passes() -> None:
    result = run_stage162_release_gate(ROOT)
    assert result["status"] == "pass"
    assert result["stage162"]["render_packet_count"] >= 6
    assert result["store_write_enabled"] is False
    assert result["provider_generation_enabled"] is False


def test_stage162_tampered_checksum_blocks(tmp_path: Path) -> None:
    store = tmp_path / "render_packets.jsonl"
    packet = load_render_packets(STORE)[0]
    packet["render_payload_summary"] = "tampered"
    store.write_text(json.dumps(packet, ensure_ascii=False) + "\n", encoding="utf-8")
    validation = validate_render_packet_store(store)
    assert validation["status"] == "blocked"
    assert any(issue.startswith("checksum_mismatch") for issue in validation["issues"])


def test_stage162_node2_forbidden_payload_blocks(tmp_path: Path) -> None:
    store = tmp_path / "render_packets.jsonl"
    packet = load_render_packets(STORE)[0]
    packet["node2_projection_summary"] = "contains hidden_reveal_payload"
    packet["checksum"] = "invalid"
    store.write_text(json.dumps(packet, ensure_ascii=False) + "\n", encoding="utf-8")
    validation = validate_render_packet_store(store)
    assert validation["status"] == "blocked"
    assert any("forbidden_token" in issue for issue in validation["issues"])
