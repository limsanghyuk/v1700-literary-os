from __future__ import annotations

from pathlib import Path

from v1700.lineage_absorption.absorption_planner import build_stage121_absorption_preflight
from v1700.lineage_absorption.conflict_matrix import build_conflict_matrix
from v1700.lineage_absorption.formula_ledger import build_formula_ledger
from v1700.lineage_absorption.gate_authority_map import build_gate_authority_map
from v1700.stage121.orchestrator import run_stage121
from v1700.gates.stage121_release_gate import run_stage121_release_gate


def test_stage121_formula_ledger_preserves_stage120_and_blocks_conflicts() -> None:
    ledger = build_formula_ledger()
    assert ledger["status"] == "pass"
    assert ledger["stage120_formulas_preserved"] is True
    ids = {entry["formula_id"] for entry in ledger["entries"]}
    assert "STAGE120_AMW_ALPHA_BOUNDS" in ids
    assert "V525_AMW_ALPHA_BOUNDS" in ids
    assert "V555_PNE_PREEMPTIVE_GATE" in ids


def test_stage121_conflict_and_gate_authority_maps() -> None:
    conflicts = build_conflict_matrix()
    assert conflicts["direct_merge_blocked"] is True
    assert "C121-005" in conflicts["resolution_required_before_absorption"]
    gates = build_gate_authority_map()
    assert gates["status"] == "pass"
    assert gates["primary_gate"] == "Gate25"
    assert gates["future_governor_blocked_until_stage125"] is True


def test_stage121_orchestrator_release_gate_pass() -> None:
    root = Path(__file__).resolve().parents[1]
    preflight = build_stage121_absorption_preflight(root)
    assert preflight["status"] == "pass"
    assert preflight["lineage_relationship_map"]["all_direct_merges_blocked"] is True
    stage = run_stage121(root)
    assert stage["status"] == "pass"
    assert stage["candidate_direct_merge_allowed"] is False
    gate = run_stage121_release_gate(root)
    assert gate["status"] == "pass"
    assert gate["checks"]["candidate_direct_merge_blocked"]["status"] == "pass"
    assert gate["checks"]["gate_authority_primary_gate25"]["status"] == "pass"
