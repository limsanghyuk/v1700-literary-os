from __future__ import annotations

import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from v1700.gitnexus_preflight import run_stage112_gitnexus_nie_preflight
from v1700.gates.stage112_release_gate import run_stage112_release_gate
from v1700.stage112 import run_stage112

ROOT = Path(__file__).resolve().parents[1]


def test_stage112_preflight_passes_with_python_fallback():
    result = run_stage112_gitnexus_nie_preflight(ROOT)
    assert result["status"] == "pass"
    assert result["python_fallback_used"] is True
    assert result["stale_index_detected"] is False
    assert result["shape_check_pass"] is True


def test_stage112_survival_matrix_preserves_core_branchpoints():
    result = run_stage112_gitnexus_nie_preflight(ROOT)
    matrix = result["survival_matrix"]
    for key in [
        "stage51_character_event_time_ledger",
        "stage52_reveal_budget_memory_guard",
        "stage95_narrative_physics",
        "stage96_coefficient_memory",
        "stage97_longform_endurance",
        "stage107_longform_production_suite",
        "stage111_absorption_candidate_bridge",
    ]:
        assert matrix[key] is True


def test_stage112_concept_impact_preserves_privacy_and_provider_zero():
    result = run_stage112_gitnexus_nie_preflight(ROOT)
    concept = result["concept_impact"]
    assert concept["provider_zero_preserved"] is True
    assert concept["live_provider_call_count_in_release_gate"] == 0
    assert concept["node2_raw_reveal_access"] == 0
    assert concept["raw_manuscript_provider_leakage"] == 0
    assert concept["credential_leakage"] == 0


def test_stage112_symbol_trace_connects_new_logic_to_branchpoints():
    result = run_stage112_gitnexus_nie_preflight(ROOT)
    trace = result["branchpoint_trace"]
    assert "GitNexusPreflightResult" in trace
    assert "stage112_preflight" in trace["GitNexusPreflightResult"]
    assert "NarrativeWeightKernel" in trace


def test_stage112_orchestrator_and_release_gate_pass():
    stage = run_stage112(ROOT)
    assert stage["status"] == "pass"
    gate = run_stage112_release_gate(ROOT)
    assert gate["status"] == "pass"
    assert gate["live_provider_call_count_in_release_gate"] == 0
    assert gate["physics_reward_bridge_llm_call_count"] == 0


def test_stage112_docs_and_manifests_exist():
    for rel in [
        "docs/stages/stage112.md",
        "manifests/stage112_manifest.json",
        "manifests/stage112_nie_branchpoint_manifest.json",
        "manifests/stage112_gitnexus_nie_preflight_manifest.json",
    ]:
        assert (ROOT / rel).exists()

