from pathlib import Path

from v1700.gates.release_gate import run_release_gate
from v1700.gates.stage89_release_gate import run_stage89_release_gate
from v1700.traceability.symbol_trace import build_symbol_to_branchpoint_trace_manifest
from v1700.writer_studio.export_pipeline import WriterStudioExportPipeline, run_stage89_export_pipeline_smoke
from v1700.writer_studio.workspace import REQUIRED_PANEL_IDS, build_writer_studio_workspace, run_writer_studio_smoke


def test_stage89_writer_studio_builds_required_panels():
    workspace = build_writer_studio_workspace(episode_count=16, scenes_per_episode=10)

    assert workspace.status == "pass"
    assert set(REQUIRED_PANEL_IDS).issubset(set(workspace.panel_ids))
    assert workspace.panel_count >= 8
    assert workspace.panel("episode_board").item_count == 16
    assert workspace.panel("scene_card_board").item_count == 32
    assert workspace.provider_default_calls == 0
    assert workspace.node2_raw_reveal_access_count == 0


def test_stage89_export_pipeline_builds_all_required_formats_with_checksums():
    workspace = build_writer_studio_workspace(episode_count=16, scenes_per_episode=10)
    bundle = WriterStudioExportPipeline().build_bundle(workspace)

    assert bundle.status == "pass"
    assert bundle.artifact_count >= 5
    assert {"markdown", "json", "html", "platform_serialization_pack", "scene_csv"}.issubset(set(bundle.formats))
    assert all(artifact.byte_size > 0 for artifact in bundle.artifacts)
    assert all(len(artifact.checksum) == 64 for artifact in bundle.artifacts)
    assert bundle.provider_default_calls == 0
    assert bundle.node2_raw_reveal_access_count == 0


def test_stage89_smokes_and_release_gate_preserve_stage88_lineage():
    studio = run_writer_studio_smoke()
    export = run_stage89_export_pipeline_smoke()
    gate = run_stage89_release_gate()

    assert studio["status"] == "pass"
    assert export["status"] == "pass"
    assert gate["status"] == "pass"
    assert gate["checks"]["stage88_release_gate"]["status"] == "pass"
    assert gate["provider_default_calls"] == 0
    assert gate["node2_raw_reveal_access_count"] == 0


def test_stage89_symbol_trace_manifest_covers_writer_studio_branchpoints():
    manifest = build_symbol_to_branchpoint_trace_manifest()
    ids = {entry["branchpoint_id"] for entry in manifest["entries"]}

    assert manifest["status"] == "pass"
    assert manifest["stage"] in {"89", "90", "91", "92", "93", "94", "97.1"}
    assert "BP_STAGE89_WRITER_STUDIO_UI_CONTRACT" in ids
    assert "BP_STAGE89_EXPORT_PIPELINE" in ids
    assert "BP_STAGE89_STATIC_STUDIO_PREVIEW" in ids
    assert "BP_STAGE89_PROVIDER_ZERO_EXPORT" in ids
    assert manifest["coverage"]["P0"]["coverage"] == 1.0


def test_main_release_gate_includes_stage89_when_active():
    result = run_release_gate()

    assert result["status"] == "pass"
    assert result["stage88_release_gate"]["status"] == "pass"
    assert result["stage89_release_gate"]["status"] == "pass"
