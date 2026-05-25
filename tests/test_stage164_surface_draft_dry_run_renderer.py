from __future__ import annotations

import json
from pathlib import Path

from v1700.surface_draft_dry_run_renderer.renderer import build_surface_draft_dry_run
from v1700.surface_draft_dry_run_renderer import run_stage164_surface_draft_dry_run_renderer
from v1700.gates.stage164_release_gate import run_stage164_release_gate
from v1700.local_render_packet_store.loader import load_render_packets, compute_render_packet_checksum

ROOT = Path(__file__).resolve().parents[1]
STORE = ROOT / "samples/stage162_render_packet_store/render_packets.jsonl"


def test_stage164_surface_draft_is_deterministic() -> None:
    first = build_surface_draft_dry_run(ROOT)
    second = build_surface_draft_dry_run(ROOT)
    assert first["status"] == "pass"
    assert second["status"] == "pass"
    assert first["surface_draft_checksum"] == second["surface_draft_checksum"]
    assert first["draft_unit_count"] >= 6
    assert first["trace_step_count"] == first["draft_unit_count"]


def test_stage164_draft_units_are_surface_safe_and_side_effect_free() -> None:
    result = build_surface_draft_dry_run(ROOT)
    assert all(unit["boundary_level"] == "NODE2_SURFACE_SAFE" for unit in result["units"])
    assert all("hidden_render_payload" not in unit["draft_text"].lower() for unit in result["units"])
    assert all(step["provider_call_allowed"] is False for step in result["trace_steps"])
    assert all(step["write_allowed"] is False for step in result["trace_steps"])


def test_stage164_report_passes_and_blocks_runtime_rendering() -> None:
    result = run_stage164_surface_draft_dry_run_renderer(ROOT)
    assert result["status"] == "pass"
    assert result["draft_unit_count"] >= 6
    assert result["rendering_runtime_enabled"] is False
    assert result["provider_generation_enabled"] is False
    assert result["surface_draft_write_enabled"] is False
    assert result["provider_default_calls"] == 0
    assert result["stage165_render_quality_boundary_preflight_ready"] is True


def test_stage164_release_gate_passes() -> None:
    result = run_stage164_release_gate(ROOT)
    assert result["status"] == "pass"
    assert result["stage164"]["draft_unit_count"] >= 6
    assert result["provider_generation_enabled"] is False
    assert result["surface_draft_write_enabled"] is False


def test_stage164_hidden_payload_blocks_when_source_projection_is_tainted(tmp_path: Path) -> None:
    packets = load_render_packets(STORE)
    packets[0]["node2_projection_summary"] = "contains hidden_render_payload"
    packets[0]["checksum"] = compute_render_packet_checksum(packets[0])
    store = ROOT / "samples/stage162_render_packet_store/render_packets.jsonl"
    original = store.read_text(encoding="utf-8")
    try:
        store.write_text("\n".join(json.dumps(packet, ensure_ascii=False) for packet in packets) + "\n", encoding="utf-8")
        result = build_surface_draft_dry_run(ROOT)
        assert result["status"] == "blocked"
        assert any("hidden_render_payload" in issue for issue in result["issues"])
    finally:
        store.write_text(original, encoding="utf-8")


def test_stage164_tampered_packet_store_blocks(tmp_path: Path) -> None:
    packets = load_render_packets(STORE)
    packets[0]["render_payload_summary"] = "tampered after checksum"
    store = ROOT / "samples/stage162_render_packet_store/render_packets.jsonl"
    original = store.read_text(encoding="utf-8")
    try:
        store.write_text("\n".join(json.dumps(packet, ensure_ascii=False) for packet in packets) + "\n", encoding="utf-8")
        result = build_surface_draft_dry_run(ROOT)
        assert result["status"] == "blocked"
        assert any("checksum_mismatch" in issue for issue in result["issues"])
    finally:
        store.write_text(original, encoding="utf-8")
