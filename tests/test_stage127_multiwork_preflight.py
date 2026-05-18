from __future__ import annotations

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from v1700.gates.stage127_release_gate import run_stage127_release_gate
from v1700.multiwork_preflight.author_license_audit import run_author_license_audit
from v1700.multiwork_preflight.project_isolation_audit import run_project_isolation_audit
from v1700.multiwork_preflight.shared_world_audit import canon_conflict_score, density_status, run_shared_world_audit
from v1700.stage127 import run_stage127

ROOT = Path(__file__).resolve().parents[1]


def test_stage127_preflight_passes_with_python_fallback():
    result = run_stage127(ROOT)
    assert result["status"] == "pass"
    assert result["python_fallback_used"] is True
    assert result["provider_default_calls"] == 0
    assert result["raw_manuscript_cross_project_leakage"] == 0


def test_stage127_project_isolation_blocks_cross_write():
    audit = run_project_isolation_audit(ROOT)
    assert audit["status"] == "PASS"
    assert audit["unauthorized_cross_reads"] == 0
    assert audit["unauthorized_cross_writes"] == 0
    assert audit["details"]["cross_project_influence_write"] == 0


def test_stage127_author_license_formula_blocks_missing_license_and_write():
    audit = run_author_license_audit()
    assert audit["status"] == "pass"
    assert audit["license_edge_missing_but_access_allowed"] is False
    assert audit["cross_project_write_allowed"] is False


def test_stage127_canon_conflict_formula_thresholds():
    assert canon_conflict_score(timeline_conflict=1, world_rule_conflict=1, character_identity_conflict=0.5, relationship_conflict=0.6) > 0.60
    assert density_status(0.30) == "PASS"
    assert density_status(0.31) == "WARN"
    assert density_status(0.61) == "BLOCK"
    audit = run_shared_world_audit()
    assert audit["status"] == "pass"
    assert audit["blocking_conflicts_detected"] >= 1


def test_stage127_release_gate_passes_and_is_integrated():
    gate = run_stage127_release_gate(ROOT)
    assert gate["status"] == "pass"
    assert gate["live_provider_call_count_in_release_gate"] == 0
    assert gate["node2_raw_reveal_access"] == 0
    assert gate["raw_manuscript_provider_leakage"] == 0


def test_stage127_docs_manifests_and_evidence_exist():
    run_stage127_release_gate(ROOT)
    for rel in [
        "docs/stages/stage127.md",
        "manifests/stage127_manifest.json",
        "manifests/stage127_multiwork_preflight_manifest.json",
        "manifests/stage127_branchpoint_trace_manifest.json",
        "release/current/stage127_multiwork_preflight_report.json",
        "release/current/stage127_release_gate_report.json",
        "release/current/stage127_multiwork_preflight_pack/absorption_plan.json",
    ]:
        assert (ROOT / rel).exists()
