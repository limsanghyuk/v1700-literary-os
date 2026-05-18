from pathlib import Path

from v1700.gates.pre_stage40_survival_gate import run_pre_stage40_survival_gate
from v1700.gates.release_gate import run_release_gate
from v1700.gates.stage72_3_release_gate import run_stage72_3_release_gate
from v1700.graph_nexus.tools.concept_impact import analyze_concept_impact
from v1700.graph_nexus.tools.foundation_lineage import (
    build_pre_stage40_lineage_manifest,
    scan_pre_stage40_evidence,
)
from v1700.graph_nexus.tools.survival_matrix import build_survival_matrix


ROOT = Path(__file__).resolve().parents[1]


def test_stage72_3_scans_pre_stage40_evidence_and_builds_concepts():
    evidence = scan_pre_stage40_evidence(ROOT)
    manifest = build_pre_stage40_lineage_manifest(ROOT)

    assert evidence["status"] == "pass"
    assert evidence["artifact_count"] >= 20
    assert manifest["concept_count"] >= 20
    assert {concept["concept_id"] for concept in manifest["concepts"]} >= {
        "foundation.longform.series_arc_control",
        "foundation.stage39.temporal_continuity",
        "foundation.node2.style_evolution_memory",
        "foundation.stage39.branch_commit_rollback",
    }


def test_stage72_3_survival_gate_preserves_high_priority_foundations():
    report = run_pre_stage40_survival_gate(ROOT)

    assert report["stage"] == "72.3"
    assert report["status"] == "pass"
    assert report["concept_count"] >= 20
    assert report["missing_required"] == []
    assert report["missing_source_evidence"] == []
    assert report["missing_evidence_files"] == []
    assert report["missing_current_anchor"] == []
    assert report["high_priority_unknown"] == []
    assert report["provider_default_calls"] == 0
    assert report["node2_raw_reveal_access_count"] == 0


def test_stage72_3_survival_matrix_and_concept_impact_are_available():
    matrix = build_survival_matrix(ROOT)
    impact = analyze_concept_impact(ROOT, "Node2")

    assert matrix["status"] == "pass"
    assert matrix["concept_count"] >= 20
    assert "LIVE_RUNTIME" in matrix["buckets"]
    assert impact["status"] == "pass"
    assert impact["risk"] == "high"
    assert impact["affected_concepts"]


def test_stage72_3_release_gate_and_main_gate_include_foundation_lineage():
    stage_gate = run_stage72_3_release_gate(ROOT)
    main_gate = run_release_gate()

    assert stage_gate["status"] == "pass"
    assert stage_gate["pre_stage40_survival_gate"]["status"] == "pass"
    assert main_gate["status"] == "pass"
    assert main_gate["stage72_2_release_gate"]["status"] == "pass"
    assert main_gate["stage72_3_release_gate"]["status"] == "pass"
