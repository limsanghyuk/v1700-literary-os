from __future__ import annotations

import json
from pathlib import Path

from v1700.render_plan_builder.builder import build_deterministic_render_plan
from v1700.render_plan_builder import run_stage163_deterministic_render_plan_builder
from v1700.gates.stage163_release_gate import run_stage163_release_gate
from v1700.local_render_packet_store.loader import load_render_packets, compute_render_packet_checksum

ROOT = Path(__file__).resolve().parents[1]
STORE = ROOT / "samples/stage162_render_packet_store/render_packets.jsonl"


def test_stage163_render_plan_is_deterministic() -> None:
    first = build_deterministic_render_plan(STORE)
    second = build_deterministic_render_plan(STORE)
    assert first["status"] == "pass"
    assert second["status"] == "pass"
    assert first["render_plan_checksum"] == second["render_plan_checksum"]
    assert first["node_count"] >= 6
    assert first["edge_count"] == first["node_count"] - 1


def test_stage163_render_order_preserves_surface_safe_packets() -> None:
    plan = build_deterministic_render_plan(STORE)
    assert plan["render_order"]
    assert len(plan["render_order"]) == plan["node_count"]
    assert all(node["boundary_level"] == "NODE2_SURFACE_SAFE" for node in plan["nodes"])
    assert all(node["render_mode"] == "DRY_RUN_RENDER_ONLY" for node in plan["nodes"])


def test_stage163_report_passes_and_blocks_runtime_generation() -> None:
    result = run_stage163_deterministic_render_plan_builder(ROOT)
    assert result["status"] == "pass"
    assert result["node_count"] >= 6
    assert result["rendering_runtime_enabled"] is False
    assert result["generation_runtime_enabled"] is False
    assert result["provider_generation_enabled"] is False
    assert result["render_plan_write_enabled"] is False
    assert result["provider_default_calls"] == 0


def test_stage163_release_gate_passes() -> None:
    result = run_stage163_release_gate(ROOT)
    assert result["status"] == "pass"
    assert result["stage163"]["node_count"] >= 6
    assert result["render_plan_write_enabled"] is False
    assert result["provider_generation_enabled"] is False


def test_stage163_hidden_render_payload_blocks(tmp_path: Path) -> None:
    packets = load_render_packets(STORE)
    packets[0]["node2_projection_summary"] = "contains hidden_render_payload"
    packets[0]["checksum"] = compute_render_packet_checksum(packets[0])
    store = tmp_path / "render_packets.jsonl"
    store.write_text("\n".join(json.dumps(packet, ensure_ascii=False) for packet in packets) + "\n", encoding="utf-8")
    result = build_deterministic_render_plan(store)
    assert result["status"] == "blocked"
    assert any("hidden_render_payload" in issue for issue in result["issues"])


def test_stage163_tampered_packet_store_blocks(tmp_path: Path) -> None:
    packets = load_render_packets(STORE)
    packets[0]["render_payload_summary"] = "tampered after checksum"
    store = tmp_path / "render_packets.jsonl"
    store.write_text("\n".join(json.dumps(packet, ensure_ascii=False) for packet in packets) + "\n", encoding="utf-8")
    result = build_deterministic_render_plan(store)
    assert result["status"] == "blocked"
    assert any("checksum_mismatch" in issue for issue in result["issues"])
