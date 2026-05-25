from __future__ import annotations

import json
from pathlib import Path

from v1700.render_quality_boundary_preflight.analyzer import analyze_render_quality_boundary
from v1700.render_quality_boundary_preflight import run_stage165_render_quality_boundary_preflight
from v1700.gates.stage165_release_gate import run_stage165_release_gate
from v1700.local_render_packet_store.loader import load_render_packets, compute_render_packet_checksum

ROOT = Path(__file__).resolve().parents[1]
STORE = ROOT / "samples/stage162_render_packet_store/render_packets.jsonl"


def test_stage165_quality_analysis_is_deterministic() -> None:
    first = analyze_render_quality_boundary(ROOT)
    second = analyze_render_quality_boundary(ROOT)
    assert first["status"] == "pass"
    assert second["status"] == "pass"
    assert first["quality_boundary_checksum"] == second["quality_boundary_checksum"]
    assert first["quality_score"] >= 0.92
    assert first["unit_count"] >= 6


def test_stage165_report_passes_and_keeps_generation_disabled() -> None:
    result = run_stage165_render_quality_boundary_preflight(ROOT)
    assert result["status"] == "pass"
    assert result["stage166_page04_release_seal_ready"] is True
    assert result["provider_generation_enabled"] is False
    assert result["rendering_runtime_enabled"] is False
    assert result["quality_gate_write_enabled"] is False
    assert result["provider_default_calls"] == 0


def test_stage165_release_gate_passes() -> None:
    result = run_stage165_release_gate(ROOT)
    assert result["status"] == "pass"
    assert result["stage165"]["quality_score"] >= 0.92
    assert result["provider_generation_enabled"] is False
    assert result["quality_gate_write_enabled"] is False


def test_stage165_hidden_surface_payload_blocks() -> None:
    packets = load_render_packets(STORE)
    packets[0]["node2_projection_summary"] = "contains hidden_render_payload"
    packets[0]["checksum"] = compute_render_packet_checksum(packets[0])
    original = STORE.read_text(encoding="utf-8")
    try:
        STORE.write_text("\n".join(json.dumps(packet, ensure_ascii=False) for packet in packets) + "\n", encoding="utf-8")
        result = analyze_render_quality_boundary(ROOT)
        assert result["status"] == "blocked"
        assert any("hidden_render_payload" in issue for issue in result["issues"])
    finally:
        STORE.write_text(original, encoding="utf-8")


def test_stage165_tampered_render_packet_store_blocks() -> None:
    packets = load_render_packets(STORE)
    packets[0]["render_payload_summary"] = "tampered after checksum"
    original = STORE.read_text(encoding="utf-8")
    try:
        STORE.write_text("\n".join(json.dumps(packet, ensure_ascii=False) for packet in packets) + "\n", encoding="utf-8")
        result = analyze_render_quality_boundary(ROOT)
        assert result["status"] == "blocked"
        assert any("checksum_mismatch" in issue for issue in result["issues"])
    finally:
        STORE.write_text(original, encoding="utf-8")


def test_stage165_pack_contains_stage166_entry_criteria() -> None:
    result = run_stage165_render_quality_boundary_preflight(ROOT)
    criteria = result["parts"]["stage166_entry_criteria"]
    assert criteria["status"] == "pass"
    assert criteria["criteria"]["quality_score_threshold_pass"] is True
    assert criteria["criteria"]["quality_boundary_checksum_present"] is True
