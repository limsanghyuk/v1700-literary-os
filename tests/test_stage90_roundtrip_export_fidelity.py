from v1700.gates.release_gate import run_release_gate
from v1700.gates.stage90_release_gate import run_stage90_release_gate
from v1700.traceability.symbol_trace import build_symbol_to_branchpoint_trace_manifest
from v1700.writer_studio.roundtrip import StudioRoundTripEngine, run_stage90_roundtrip_smoke


def test_stage90_roundtrip_applies_writer_edits_and_reexports_all_formats():
    report = run_stage90_roundtrip_smoke()

    assert report["status"] == "pass"
    assert report["edit_count"] >= 4
    assert report["applied_count"] == report["edit_count"]
    assert report["before_artifact_count"] >= 5
    assert report["after_artifact_count"] == report["before_artifact_count"]
    assert report["changed_artifact_count"] >= 5
    assert report["fidelity_score"] == 10.0
    assert report["provider_default_calls"] == 0
    assert report["node2_raw_reveal_access_count"] == 0


def test_stage90_roundtrip_preserves_panel_and_scene_csv_shape():
    report = StudioRoundTripEngine().run_roundtrip()
    payload = report.to_dict()

    assert payload["json_roundtrip_panel_count"] >= 8
    assert payload["markdown_contains_edit_summary"] is True
    assert payload["html_contains_stage90_marker"] is True
    assert payload["scene_csv_row_count"] == 32
    assert not payload["issues"]


def test_stage90_release_gate_inherits_stage89_and_blocks_on_fidelity():
    gate = run_stage90_release_gate()

    assert gate["status"] == "pass"
    assert gate["checks"]["stage89_release_gate"]["status"] == "pass"
    assert gate["checks"]["stage90_roundtrip_smoke"]["status"] == "pass"
    assert gate["checks"]["stage90_roundtrip_smoke"]["fidelity_score"] == 10.0
    assert gate["provider_default_calls"] == 0
    assert gate["node2_raw_reveal_access_count"] == 0


def test_stage90_symbol_trace_manifest_covers_roundtrip_branchpoints():
    manifest = build_symbol_to_branchpoint_trace_manifest()
    ids = {entry["branchpoint_id"] for entry in manifest["entries"]}

    assert manifest["status"] == "pass"
    assert manifest["stage"] in {"90", "91", "92", "93", "94", "97.1"}
    assert "BP_STAGE90_STUDIO_ROUNDTRIP_EDITING" in ids
    assert "BP_STAGE90_EXPORT_FIDELITY_HARDENING" in ids
    assert "BP_STAGE90_PROVIDER_ZERO_ROUNDTRIP" in ids
    assert manifest["coverage"]["P0"]["coverage"] == 1.0


def test_main_release_gate_includes_stage90_when_active():
    result = run_release_gate()

    assert result["status"] == "pass"
    assert result["stage89_release_gate"]["status"] == "pass"
    assert result["stage90_release_gate"]["status"] == "pass"
