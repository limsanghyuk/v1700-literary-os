from __future__ import annotations

from pathlib import Path

from v1700.corpus_governance_pipeline import run_stage139_corpus_governance_pipeline
from v1700.corpus_governance_pipeline.gate import CORPUS_GOVERNANCE_MODE
from v1700.gates.release_gate import run_release_gate
from v1700.gates.stage139_release_gate import run_stage139_release_gate

ROOT = Path(__file__).resolve().parents[1]


def test_stage139_report_passes() -> None:
    result = run_stage139_corpus_governance_pipeline(ROOT)
    assert result["status"] == "pass"
    assert result["mode"] == CORPUS_GOVERNANCE_MODE
    assert result["corpus_governance_pipeline_only"] is True
    assert result["governance_profile_count"] >= 3


def test_stage139_governs_every_stage138_route() -> None:
    result = run_stage139_corpus_governance_pipeline(ROOT)
    assert result["case_packet_count"] >= 1
    assert result["governed_case_count"] == result["case_packet_count"]
    assert result["policy_binding_count"] == result["case_packet_count"]
    assert result["review_queue_packet_count"] >= 1


def test_stage139_blocks_writes_training_and_providers() -> None:
    result = run_stage139_corpus_governance_pipeline(ROOT)
    assert result["runtime_training_enabled"] is False
    assert result["active_meta_learning_enabled"] is False
    assert result["model_weight_update_count"] == 0
    assert result["losdb_write_enabled"] is False
    assert result["migration_execution_enabled"] is False
    assert result["storage_contract_write_enabled"] is False
    assert result["provider_default_calls"] == 0
    assert result["node2_raw_reveal_access"] == 0


def test_stage139_preserves_review_queue_and_audit_trail() -> None:
    result = run_stage139_corpus_governance_pipeline(ROOT)
    queue_packets = result["parts"]["corpus_governance_pipeline"]["review_queue_packets"]
    case_packets = result["parts"]["corpus_governance_pipeline"]["case_packets"]
    assert queue_packets
    assert any(packet["lane_name"] == "writer_review_queue" for packet in queue_packets)
    assert any(packet["approval_lane"] == "writer_review_queue" for packet in case_packets)
    assert all(packet["audit_event_key"] for packet in case_packets)


def test_stage139_preflight_and_release_gate_pass() -> None:
    result = run_stage139_corpus_governance_pipeline(ROOT)
    preflight = result["parts"]["preflight"]
    assert preflight["python_fallback"]["status"] == "PASS"
    assert all(preflight["survival_matrix"].values())
    gate = run_stage139_release_gate(ROOT)
    assert gate["status"] == "pass"
    assert gate["checks"]["stage140_release_ready_pass"]["status"] == "pass"


def test_stage139_release_evidence_remains_available() -> None:
    manifest = (ROOT / "manifests" / "live_core_manifest.json").read_text(encoding="utf-8")
    assert '"stage139_corpus_governance_pipeline"' in manifest
    assert '"stage139_release_gate"' in manifest

    result = run_release_gate()
    assert result["status"] == "pass"
    assert result["stage139_release_gate"]["status"] == "pass"
