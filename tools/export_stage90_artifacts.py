from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from v1700.gates.release_gate import run_release_gate
from v1700.gates.stage90_release_gate import run_stage90_release_gate
from v1700.traceability.index_quality import build_gitnexus_index_quality_report
from v1700.traceability.symbol_trace import build_symbol_to_branchpoint_trace_manifest, export_symbol_to_branchpoint_trace_manifest
from v1700.writer_studio.export_pipeline import WriterStudioExportPipeline
from v1700.writer_studio.roundtrip import StudioRoundTripEngine, run_stage90_roundtrip_smoke
from v1700.writer_studio.workspace import build_writer_studio_workspace


def _project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def export_stage90_artifacts(root: Path | None = None) -> dict[str, str]:
    root = root or _project_root()
    written: dict[str, str] = {}
    release_dir = root / "release" / "current"
    export_dir = release_dir / "stage90_exports"
    release_dir.mkdir(parents=True, exist_ok=True)
    export_dir.mkdir(parents=True, exist_ok=True)

    # Create the patched workspace and export its post-edit artifacts.
    engine = StudioRoundTripEngine()
    base_workspace = build_writer_studio_workspace(episode_count=16, scenes_per_episode=10)
    patched_workspace, applied = engine.apply_patch(base_workspace)
    workspace_path = release_dir / "stage90_patched_writer_studio_workspace.json"
    workspace_path.write_text(json.dumps(patched_workspace.to_dict(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    written["stage90_patched_writer_studio_workspace"] = str(workspace_path.relative_to(root))

    bundle = WriterStudioExportPipeline().build_bundle(patched_workspace)
    bundle_path = release_dir / "stage90_export_bundle_report.json"
    bundle_path.write_text(json.dumps(bundle.to_dict(include_content=False), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    written["stage90_export_bundle_report"] = str(bundle_path.relative_to(root))

    for artifact in bundle.artifacts:
        artifact_path = export_dir / artifact.filename
        artifact_path.write_text(artifact.content, encoding="utf-8")
        written[f"stage90_export_{artifact.artifact_id}"] = str(artifact_path.relative_to(root))

    roundtrip = run_stage90_roundtrip_smoke()
    roundtrip_path = release_dir / "stage90_roundtrip_fidelity_report.json"
    roundtrip_path.write_text(json.dumps(roundtrip, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    written["stage90_roundtrip_fidelity_report"] = str(roundtrip_path.relative_to(root))

    manifest = {
        "stage": "90",
        "title": "Studio Round-trip Editing + Export Fidelity Hardening",
        "status": "pending",
        "depends_on": ["stage89", "stage88", "stage87", "stage86", "stage85", "stage84", "stage83.1"],
        "required_outputs": [
            "src/v1700/writer_studio/roundtrip.py",
            "src/v1700/gates/stage90_release_gate.py",
            "tools/run_stage90_roundtrip.py",
            "tools/run_stage90_release_gate.py",
            "tools/export_stage90_artifacts.py",
            "tests/test_stage90_roundtrip_export_fidelity.py",
            "manifests/stage90_branchpoint_trace_manifest.json",
            "release/current/stage90_roundtrip_fidelity_report.json",
            "release/current/stage90_release_gate_report.json",
        ],
        "roundtrip_targets": {
            "minimum_edit_count": 4,
            "minimum_changed_artifact_count": 5,
            "required_fidelity_score": 10.0,
        },
        "export_fidelity_targets": {
            "formats": list(bundle.formats),
            "artifact_count": bundle.artifact_count,
            "post_edit_export_folder": "release/current/stage90_exports",
        },
        "provider_default_calls": 0,
        "node2_raw_reveal_access_count": 0,
    }
    manifest_path = root / "manifests" / "stage90_manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    written["stage90_manifest"] = str(manifest_path.relative_to(root))

    # Trace export needs roundtrip report to exist before P0 coverage can pass.
    written.update(export_symbol_to_branchpoint_trace_manifest(root))

    trace_manifest = build_symbol_to_branchpoint_trace_manifest(root)
    stage90_trace = {
        **trace_manifest,
        "entries": [entry for entry in trace_manifest["entries"] if entry["branchpoint_id"].startswith("BP_STAGE90_")],
    }
    trace_path = root / "manifests" / "stage90_branchpoint_trace_manifest.json"
    trace_path.write_text(json.dumps(stage90_trace, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    written["stage90_branchpoint_trace_manifest"] = str(trace_path.relative_to(root))

    gate = run_stage90_release_gate(root)
    gate_path = release_dir / "stage90_release_gate_report.json"
    gate_path.write_text(json.dumps(gate, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    written["stage90_release_gate_report"] = str(gate_path.relative_to(root))

    # Re-export trace after gate report exists, then main release.
    written.update(export_symbol_to_branchpoint_trace_manifest(root))
    trace_manifest = build_symbol_to_branchpoint_trace_manifest(root)
    stage90_trace = {
        **trace_manifest,
        "entries": [entry for entry in trace_manifest["entries"] if entry["branchpoint_id"].startswith("BP_STAGE90_")],
    }
    trace_path.write_text(json.dumps(stage90_trace, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    main_release = run_release_gate()
    main_path = release_dir / "release_gate_report.json"
    main_path.write_text(json.dumps(main_release, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    written["release_gate_report"] = str(main_path.relative_to(root))

    quality = build_gitnexus_index_quality_report(root)
    quality["stage"] = "90"
    quality["title"] = "Stage90 GitNexus Index Quality Snapshot"
    quality_path = release_dir / "stage90_gitnexus_index_quality_report.json"
    quality_path.write_text(json.dumps(quality, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    written["stage90_gitnexus_index_quality_report"] = str(quality_path.relative_to(root))

    manifest["status"] = gate["status"]
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    handoff_path = release_dir / "stage90_developer_handoff_report.md"
    handoff_path.write_text(_render_developer_handoff(root, gate, roundtrip, bundle.to_dict(include_content=False), main_release) + "\n", encoding="utf-8")
    written["stage90_developer_handoff_report"] = str(handoff_path.relative_to(root))
    return written


def _render_developer_handoff(root: Path, gate: dict[str, Any], roundtrip: dict[str, Any], bundle: dict[str, Any], main_release: dict[str, Any]) -> str:
    return "\n".join([
        "# Stage90 Developer Handoff Report",
        "",
        "## Status",
        "",
        f"- Stage90 release gate: `{gate['status']}`",
        f"- Main release gate: `{main_release['status']}`",
        "- Provider default calls: `0`",
        "- Node2 raw reveal access: `0`",
        "",
        "## Round-trip Fidelity",
        "",
        f"- Edit count: `{roundtrip['edit_count']}`",
        f"- Applied count: `{roundtrip['applied_count']}`",
        f"- Changed artifact count: `{roundtrip['changed_artifact_count']}`",
        f"- Fidelity score: `{roundtrip['fidelity_score']}`",
        "",
        "## Export Pipeline",
        "",
        f"- Artifact count: `{bundle['artifact_count']}`",
        "- Formats: " + ", ".join(f"`{fmt}`" for fmt in bundle["formats"]),
        "- Output folder: `release/current/stage90_exports`",
        "",
        "## What Stage90 Proves",
        "",
        "- Writer-facing Studio edits can be applied deterministically.",
        "- Patched Studio state re-exports to JSON, Markdown, HTML, platform pack, and scene CSV.",
        "- Before/after checksum deltas and shape checks are release-gated.",
        "- Stage89/88/87/86/85 lineage remains inherited.",
        "",
        "## Developer Commands",
        "",
        "```bash",
        "python -m pip install -e .",
        "python tools/run_stage90_roundtrip.py",
        "python tools/run_stage90_release_gate.py",
        "python tools/run_release_gate.py",
        "python -m pytest -q tests",
        "```",
        "",
        "## Next Direction",
        "",
        "`Stage91` should add interactive Studio persistence, review queues, and UI event replay while preserving Stage90 export fidelity.",
        "",
        f"Repository root: `{root}`",
    ])


if __name__ == "__main__":
    print(json.dumps(export_stage90_artifacts(), ensure_ascii=True, indent=2))
