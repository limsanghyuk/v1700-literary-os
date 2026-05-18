from __future__ import annotations

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from v1700.gates.stage128_release_gate import run_stage128_release_gate
from v1700.shared_readonly_absorption.license_boundary import run_license_boundary_adapter
from v1700.shared_readonly_absorption.project_isolation import run_project_isolation_guard
from v1700.shared_readonly_absorption.shared_character_adapter import run_shared_character_read_only_adapter
from v1700.shared_readonly_absorption.shared_world_adapter import canon_conflict_score, canon_status, run_shared_world_read_only_adapter
from v1700.stage128 import run_stage128

ROOT = Path(__file__).resolve().parents[1]


def test_stage128_read_only_absorption_passes():
    result = run_stage128(ROOT)
    assert result["status"] == "pass"
    assert result["read_only_absorption"] is True
    assert result["provider_default_calls"] == 0
    assert result["raw_manuscript_provider_leakage"] == 0
    assert result["raw_manuscript_cross_project_leakage"] == 0


def test_stage128_shared_character_adapter_is_feature_only_and_read_only():
    report = run_shared_character_read_only_adapter()
    assert report["status"] == "PASS"
    assert report["read_only"] is True
    assert report["blocked_writes"] >= 1
    assert report["raw_text_exported"] is False


def test_stage128_shared_world_adapter_blocks_canon_collision_and_does_not_promote_truth():
    report = run_shared_world_read_only_adapter()
    assert report["status"] == "PASS"
    assert report["read_only"] is True
    assert report["evidence"]["shared_world_is_not_source_of_truth"] is True
    assert canon_conflict_score(timeline_conflict=1, world_rule_conflict=1, character_identity_conflict=0.5, relationship_conflict=0.6) > 0.60
    assert canon_status(0.30) == "PASS"
    assert canon_status(0.31) == "WARN"
    assert canon_status(0.61) == "BLOCK"


def test_stage128_license_boundary_blocks_missing_license_and_write():
    report = run_license_boundary_adapter()
    assert report["status"] == "pass"
    assert report["license_edge_missing_but_access_allowed"] is False
    assert report["cross_project_write_allowed"] is False


def test_stage128_project_isolation_zero_leakage():
    report = run_project_isolation_guard()
    assert report["status"] == "pass"
    assert report["unauthorized_cross_reads"] == 0
    assert report["unauthorized_cross_writes"] == 0
    assert report["raw_manuscript_cross_project_leakage"] == 0


def test_stage128_release_gate_passes_and_is_integrated():
    gate = run_stage128_release_gate(ROOT)
    assert gate["status"] == "pass"
    assert gate["live_provider_call_count_in_release_gate"] == 0
    assert gate["node2_raw_reveal_access"] == 0
    assert gate["raw_manuscript_provider_leakage"] == 0


def test_stage128_docs_manifests_and_evidence_exist():
    run_stage128_release_gate(ROOT)
    for rel in [
        "docs/stages/stage128.md",
        "manifests/stage128_manifest.json",
        "manifests/stage128_read_only_absorption_manifest.json",
        "manifests/stage128_branchpoint_trace_manifest.json",
        "release/current/stage128_read_only_absorption_report.json",
        "release/current/stage128_release_gate_report.json",
        "release/current/stage128_read_only_absorption_pack/shared_character_adapter_report.json",
        "release/current/stage128_read_only_absorption_pack/shared_world_adapter_report.json",
    ]:
        assert (ROOT / rel).exists()
