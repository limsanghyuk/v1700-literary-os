from pathlib import Path

from v1700.gates.gitnexus_index_quality_gate import run_gitnexus_index_quality_gate
from v1700.gates.stage85_release_gate import run_stage85_release_gate
from v1700.gates.symbol_to_branchpoint_trace_gate import run_symbol_to_branchpoint_trace_gate
from v1700.traceability.symbol_trace import build_symbol_to_branchpoint_trace_manifest


ROOT = Path(__file__).resolve().parents[1]


def test_stage85_symbol_to_branchpoint_trace_covers_p0_logic():
    manifest = build_symbol_to_branchpoint_trace_manifest(ROOT)
    assert manifest["status"] == "pass"
    assert manifest["coverage"]["P0"]["coverage"] == 1.0
    branchpoint_ids = {entry["branchpoint_id"] for entry in manifest["entries"]}
    assert "BP_STAGE85_NODE2_REVEAL_BOUNDARY" in branchpoint_ids
    assert "BP_STAGE85_PROVIDER_ZERO_LOCAL_FIRST" in branchpoint_ids
    assert "BP_STAGE85_BRANCHPOINT_SURVIVAL" in branchpoint_ids


def test_stage85_symbol_trace_gate_preserves_runtime_boundaries():
    gate = run_symbol_to_branchpoint_trace_gate(ROOT)
    assert gate["status"] == "pass"
    assert gate["provider_default_calls"] == 0
    assert gate["node2_raw_reveal_access_count"] == 0


def test_stage85_gitnexus_index_quality_gate_uses_optional_sidecar_evidence():
    report = run_gitnexus_index_quality_gate(ROOT)
    assert report["status"] == "pass"
    assert report["checks"]["gitnexus_optional_sidecar_preserved"] is True
    assert report["checks"]["python_fallback_preserved"] is True
    assert report["metrics"]["flows"] >= 100


def test_stage85_release_gate_passes_without_provider_or_reveal_regression():
    gate = run_stage85_release_gate(ROOT)
    assert gate["status"] == "pass"
    assert gate["provider_default_calls"] == 0
    assert gate["node2_raw_reveal_access_count"] == 0

