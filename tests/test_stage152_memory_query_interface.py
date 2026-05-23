
from __future__ import annotations

from pathlib import Path

from v1700.gates.stage152_release_gate import run_stage152_release_gate
from v1700.memory_query_interface import find_characters, project_for_node2, run_stage152_memory_query_interface

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ID = "sample_project_stage151"


def test_stage152_memory_query_interface_passes() -> None:
    result = run_stage152_memory_query_interface(ROOT)
    assert result["status"] == "pass"
    assert result["query_runtime_enabled"] is True
    assert result["ranking_runtime_enabled"] is True
    assert result["query_write_enabled"] is False
    assert result["memory_write_enabled"] is False
    assert result["provider_default_calls"] == 0
    assert result["node2_raw_reveal_access"] == 0


def test_stage152_finds_character_memory_deterministically() -> None:
    result = find_characters(ROOT, PROJECT_ID, "Minseo secret")
    assert result["status"] == "pass"
    assert result["candidate_count"] >= 1
    assert result["candidates"][0]["record_type"] == "character"
    assert result["candidates"][0]["score"] >= result["candidates"][-1]["score"]


def test_stage152_node2_projection_blocks_hidden_reveal() -> None:
    report = run_stage152_memory_query_interface(ROOT)
    candidates = report["parts"]["intent_query_result"]["candidates"]
    projection = project_for_node2(candidates)
    assert projection["status"] == "pass"
    assert projection["node2_raw_reveal_access"] == 0
    assert all("hidden_reveal_payload" not in entry for entry in projection["entries"])


def test_stage152_release_gate_passes() -> None:
    result = run_stage152_release_gate(ROOT)
    assert result["status"] == "pass"
    assert result["provider_default_calls"] == 0
    assert result["node2_raw_reveal_access"] == 0
    assert result["query_write_enabled"] is False
