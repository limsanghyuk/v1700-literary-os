from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from v1700.gates.release_gate import run_release_gate
from v1700.gates.stage89_release_gate import run_stage89_release_gate
from v1700.traceability.index_quality import build_gitnexus_index_quality_report
from v1700.traceability.symbol_trace import build_symbol_to_branchpoint_trace_manifest, export_symbol_to_branchpoint_trace_manifest
from v1700.writer_studio.export_pipeline import WriterStudioExportPipeline, run_stage89_export_pipeline_smoke
from v1700.writer_studio.workspace import build_writer_studio_workspace, run_writer_studio_smoke


def _project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def export_stage89_artifacts(root: Path | None = None) -> dict[str, str]:
    root = root or _project_root()
    written: dict[str, str] = {}
    release_dir = root / "release" / "current"
    export_dir = release_dir / "stage89_exports"
    release_dir.mkdir(parents=True, exist_ok=True)
    export_dir.mkdir(parents=True, exist_ok=True)

    workspace = build_writer_studio_workspace(episode_count=16, scenes_per_episode=10)
    workspace_payload = workspace.to_dict()
    workspace_path = release_dir / "stage89_writer_studio_workspace.json"
    workspace_path.write_text(json.dumps(workspace_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    written["stage89_writer_studio_workspace"] = str(workspace_path.relative_to(root))

    bundle = WriterStudioExportPipeline().build_bundle(workspace)
    bundle_path = release_dir / "stage89_export_bundle_report.json"
    bundle_path.write_text(json.dumps(bundle.to_dict(include_content=False), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    written["stage89_export_bundle_report"] = str(bundle_path.relative_to(root))

    for artifact in bundle.artifacts:
        artifact_path = export_dir / artifact.filename
        artifact_path.write_text(artifact.content, encoding="utf-8")
        written[f"stage89_export_{artifact.artifact_id}"] = str(artifact_path.relative_to(root))

    manifest = {
        "stage": "89",
        "title": "Writer Studio UI + Export Pipeline",
        "status": "pending",
        "depends_on": ["stage88", "stage87", "stage86", "stage85", "stage84", "stage83.1"],
        "required_outputs": [
            "src/v1700/writer_studio/contracts.py",
            "src/v1700/writer_studio/workspace.py",
            "src/v1700/writer_studio/export_pipeline.py",
            "src/v1700/gates/stage89_release_gate.py",
            "tools/run_stage89_writer_studio.py",
            "tools/run_stage89_export_pipeline.py",
            "tools/run_stage89_release_gate.py",
            "tools/export_stage89_artifacts.py",
            "tests/test_stage89_writer_studio_export.py",
            "manifests/stage89_branchpoint_trace_manifest.json",
            "release/current/stage89_writer_studio_workspace.json",
            "release/current/stage89_export_bundle_report.json",
            "release/current/stage89_release_gate_report.json",
        ],
        "writer_studio_targets": {
            "minimum_panel_count": 8,
            "panel_ids": list(workspace.panel_ids),
            "export_targets": list(workspace.export_targets),
        },
        "export_pipeline_targets": {
            "minimum_artifact_count": 5,
            "formats": list(bundle.formats),
            "artifact_count": bundle.artifact_count,
        },
        "provider_default_calls": 0,
        "node2_raw_reveal_access_count": 0,
    }
    manifest_path = root / "manifests" / "stage89_manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    written["stage89_manifest"] = str(manifest_path.relative_to(root))

    written.update(export_symbol_to_branchpoint_trace_manifest(root))

    gate = run_stage89_release_gate(root)
    gate_path = release_dir / "stage89_release_gate_report.json"
    gate_path.write_text(json.dumps(gate, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    written["stage89_release_gate_report"] = str(gate_path.relative_to(root))

    main_release = run_release_gate()
    main_path = release_dir / "release_gate_report.json"
    main_path.write_text(json.dumps(main_release, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    written["release_gate_report"] = str(main_path.relative_to(root))

    stage89_quality = build_gitnexus_index_quality_report(root)
    stage89_quality["stage"] = "89"
    stage89_quality["title"] = "Stage89 GitNexus Index Quality Snapshot"
    quality_path = release_dir / "stage89_gitnexus_index_quality_report.json"
    quality_path.write_text(json.dumps(stage89_quality, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    written["stage89_gitnexus_index_quality_report"] = str(quality_path.relative_to(root))

    trace_manifest = build_symbol_to_branchpoint_trace_manifest(root)
    stage89_trace = {
        **trace_manifest,
        "entries": [entry for entry in trace_manifest["entries"] if entry["branchpoint_id"].startswith("BP_STAGE89_")],
    }
    trace_path = root / "manifests" / "stage89_branchpoint_trace_manifest.json"
    trace_path.write_text(json.dumps(stage89_trace, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    written["stage89_branchpoint_trace_manifest"] = str(trace_path.relative_to(root))

    manifest["status"] = gate["status"]
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    handoff_path = release_dir / "stage89_developer_handoff_report.md"
    handoff_path.write_text(_render_developer_handoff(root, gate, workspace_payload, bundle.to_dict(include_content=False), main_release) + "\n", encoding="utf-8")
    written["stage89_developer_handoff_report"] = str(handoff_path.relative_to(root))
    return written


def _render_developer_handoff(root: Path, gate: dict[str, Any], workspace: dict[str, Any], bundle: dict[str, Any], main_release: dict[str, Any]) -> str:
    return "\n".join([
        "# Stage89 Developer Handoff Report",
        "",
        "## Status",
        "",
        f"- Stage89 release gate: `{gate['status']}`",
        f"- Main release gate: `{main_release['status']}`",
        "- Provider default calls: `0`",
        "- Node2 raw reveal access: `0`",
        "",
        "## Writer Studio",
        "",
        f"- Panel count: `{workspace['panel_count']}`",
        "- Panels: " + ", ".join(f"`{panel}`" for panel in workspace["panel_ids"]),
        "",
        "## Export Pipeline",
        "",
        f"- Artifact count: `{bundle['artifact_count']}`",
        "- Formats: " + ", ".join(f"`{fmt}`" for fmt in bundle["formats"]),
        "- Output folder: `release/current/stage89_exports`",
        "",
        "## What Stage89 Proves",
        "",
        "- Writer-facing Studio panels can be generated from Stage87/88 evidence without external provider calls.",
        "- Export artifacts can be generated deterministically as JSON, Markdown, HTML, platform pack, and scene CSV.",
        "- Stage88 AI-agent benchmark, Stage87 scale-up evidence, Stage86 Arc-Reveal-Knowledge, and Stage85 traceability remain inherited gates.",
        "",
        "## Developer Commands",
        "",
        "```bash",
        "python -m pip install -e .",
        "python tools/run_stage89_writer_studio.py",
        "python tools/run_stage89_export_pipeline.py",
        "python tools/run_stage89_release_gate.py",
        "python tools/run_release_gate.py",
        "python -m pytest -q tests",
        "```",
        "",
        "## Next Direction",
        "",
        "`Stage90` should add Studio interaction/round-trip editing and export fidelity hardening.",
        "",
        f"Repository root: `{root}`",
    ])


if __name__ == "__main__":
    result = export_stage89_artifacts()
    print(json.dumps(result, ensure_ascii=True, indent=2))
