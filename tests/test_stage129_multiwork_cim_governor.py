from __future__ import annotations

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from v1700.gates.stage129_release_gate import run_stage129_release_gate
from v1700.multiwork_cim_governor.canon_governor import canon_conflict_score, canon_status, run_cross_work_canon_governor
from v1700.multiwork_cim_governor.cross_project_influence import run_cross_project_influence_edges
from v1700.multiwork_cim_governor.project_local_cim import run_project_local_cim_builder
from v1700.stage129 import run_stage129

ROOT = Path(__file__).resolve().parents[1]


def test_stage129_multiwork_cim_governor_passes():
    result = run_stage129(ROOT)
    assert result["status"] == "pass"
    assert result["project_local_cim_preserved"] is True
    assert result["provider_default_calls"] == 0
    assert result["raw_manuscript_provider_leakage"] == 0
    assert result["node2_raw_reveal_access"] == 0


def test_project_local_cim_remains_project_local():
    report = run_project_local_cim_builder()
    assert report["status"] == "pass"
    assert report["project_local_only"] is True
    assert report["cross_project_influence_write"] == 0
    assert report["raw_manuscript_exported"] is False


def test_cross_project_influence_is_read_only_and_blocks_write():
    report = run_cross_project_influence_edges()
    assert report["status"] == "pass"
    assert report["read_only_edge_count"] >= 2
    assert report["blocked_edge_count"] >= 2
    assert report["cross_project_write_edges"] >= 1
    assert report["cross_project_write_allowed"] is False
    assert report["license_edge_missing_but_access_allowed"] is False


def test_canon_governor_thresholds_and_auto_resolution_disabled():
    assert canon_conflict_score(timeline_conflict=1, world_rule_conflict=1, character_identity_conflict=1, relationship_conflict=1) == 1.0
    assert canon_status(0.30) == "PASS"
    assert canon_status(0.31) == "WARN"
    assert canon_status(0.61) == "BLOCK"
    report = run_cross_work_canon_governor()
    assert report["status"] == "pass"
    assert report["block_count"] >= 1
    assert report["canon_auto_resolution_count"] == 0
    assert report["cross_work_canon_merge_allowed"] is False


def test_stage129_release_gate_passes_and_preserves_boundaries():
    gate = run_stage129_release_gate(ROOT)
    assert gate["status"] == "pass"
    assert gate["live_provider_call_count_in_release_gate"] == 0
    assert gate["node2_raw_reveal_access"] == 0
    assert gate["raw_manuscript_provider_leakage"] == 0
    assert gate["branchpoint_lineage_preserved"] is True


def test_stage129_docs_manifests_and_evidence_exist():
    run_stage129_release_gate(ROOT)
    for rel in [
        "docs/stages/stage129.md",
        "docs/proposals/stage129_proposal.md",
        "docs/architecture/stage129_blueprint.md",
        "manifests/stage129_manifest.json",
        "manifests/stage129_multiwork_cim_governor_manifest.json",
        "manifests/stage129_branchpoint_trace_manifest.json",
        "release/current/stage129_multiwork_cim_governor_report.json",
        "release/current/stage129_release_gate_report.json",
        "release/current/stage129_multiwork_cim_governor_pack/project_local_cim_report.json",
        "release/current/stage129_multiwork_cim_governor_pack/cross_project_influence_report.json",
        "release/current/stage129_multiwork_cim_governor_pack/cross_work_canon_governor_report.json",
    ]:
        assert (ROOT / rel).exists()
