from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from v1700.episode_scaleup.evidence import run_stage87_episode_scaleup_smoke
from v1700.gates.release_gate import run_release_gate
from v1700.gates.stage87_release_gate import run_stage87_release_gate
from v1700.traceability.index_quality import build_gitnexus_index_quality_report
from v1700.traceability.symbol_trace import build_symbol_to_branchpoint_trace_manifest, export_symbol_to_branchpoint_trace_manifest


def _project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def export_stage87_artifacts(root: Path | None = None) -> dict[str, str]:
    root = root or _project_root()
    written: dict[str, str] = {}
    release_dir = root / "release" / "current"
    release_dir.mkdir(parents=True, exist_ok=True)

    evidence = run_stage87_episode_scaleup_smoke()
    evidence_path = release_dir / "stage87_episode_scaleup_evidence.json"
    evidence_path.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    written["stage87_episode_scaleup_evidence"] = str(evidence_path.relative_to(root))

    manifest = {
        "stage": "87",
        "title": "8-16 Episode Scale-up Evidence",
        "status": "pending",
        "depends_on": ["stage86", "stage85", "stage84", "stage83.1"],
        "required_outputs": [
            "src/v1700/episode_scaleup/evidence.py",
            "src/v1700/gates/stage87_release_gate.py",
            "tools/run_stage87_release_gate.py",
            "tools/export_stage87_artifacts.py",
            "tests/test_stage87_episode_scaleup.py",
            "manifests/stage87_branchpoint_trace_manifest.json",
            "release/current/stage87_episode_scaleup_evidence.json",
            "release/current/stage87_release_gate_report.json",
        ],
        "scaleup_targets": {
            "minimum_episode_count": 8,
            "full_episode_count": 16,
            "scenes_per_episode": 10,
            "minimum_scene_count": 80,
            "full_scene_count": 160,
        },
        "provider_default_calls": 0,
        "node2_raw_reveal_access_count": 0,
    }
    manifest_path = root / "manifests" / "stage87_manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    written["stage87_manifest"] = str(manifest_path.relative_to(root))

    written.update(export_symbol_to_branchpoint_trace_manifest(root))

    gate = run_stage87_release_gate(root)
    gate_path = release_dir / "stage87_release_gate_report.json"
    gate_path.write_text(json.dumps(gate, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    written["stage87_release_gate_report"] = str(gate_path.relative_to(root))

    main_release = run_release_gate()
    main_path = release_dir / "release_gate_report.json"
    main_path.write_text(json.dumps(main_release, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    written["release_gate_report"] = str(main_path.relative_to(root))

    stage87_quality = build_gitnexus_index_quality_report(root)
    stage87_quality["stage"] = "87"
    stage87_quality["title"] = "Stage87 GitNexus Index Quality Snapshot"
    quality_path = release_dir / "stage87_gitnexus_index_quality_report.json"
    quality_path.write_text(json.dumps(stage87_quality, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    written["stage87_gitnexus_index_quality_report"] = str(quality_path.relative_to(root))

    trace_manifest = build_symbol_to_branchpoint_trace_manifest(root)
    stage87_trace = {
        **trace_manifest,
        "entries": [entry for entry in trace_manifest["entries"] if entry["branchpoint_id"].startswith("BP_STAGE87_")],
    }
    trace_path = root / "manifests" / "stage87_branchpoint_trace_manifest.json"
    trace_path.write_text(json.dumps(stage87_trace, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    written["stage87_branchpoint_trace_manifest"] = str(trace_path.relative_to(root))

    manifest["status"] = gate["status"]
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    handoff_path = release_dir / "stage87_developer_handoff_report.md"
    handoff_path.write_text(_render_developer_handoff(root, gate, evidence, main_release) + "\n", encoding="utf-8")
    written["stage87_developer_handoff_report"] = str(handoff_path.relative_to(root))
    return written


def _render_developer_handoff(root: Path, gate: dict[str, Any], evidence: dict[str, Any], main_release: dict[str, Any]) -> str:
    eight = evidence["eight_episode_evidence"]
    sixteen = evidence["sixteen_episode_evidence"]
    return "\n".join([
        "# Stage87 Developer Handoff Report",
        "",
        "## Status",
        "",
        f"- Stage87 release gate: `{gate['status']}`",
        f"- Main release gate: `{main_release['status']}`",
        "- Provider default calls: `0`",
        "- Node2 raw reveal access: `0`",
        "",
        "## Scale-up Evidence",
        "",
        f"- 8-episode evidence: `{eight['episode_count']}` episodes / `{eight['total_scene_count']}` scenes",
        f"- 16-episode evidence: `{sixteen['episode_count']}` episodes / `{sixteen['total_scene_count']}` scenes",
        f"- 16-episode average quality score: `{sixteen['average_quality_score']}`",
        f"- 16-episode min quality score: `{sixteen['min_quality_score']}`",
        f"- Blocked direct reveal count: `{sixteen['blocked_direct_reveal_count']}`",
        f"- Knowledge constraint count: `{sixteen['knowledge_constraint_count']}`",
        "",
        "## What Stage87 Proves",
        "",
        "- Stage86 `SeriesArcPlanner` scales from contract smoke to 8/16 episode evidence.",
        "- `EpisodeRevealBudget` remains active across long episode maps.",
        "- `CharacterKnowledgeProseBridge` remains active across scene-level contracts.",
        "- Node2 surface-only boundary remains preserved for all scale-up scene contracts.",
        "- GitNexus/GraphNexus traceability remains optional-sidecar safe.",
        "",
        "## Developer Commands",
        "",
        "```bash",
        "python -m pip install -e .",
        "python tools/run_stage87_release_gate.py",
        "python tools/run_symbol_to_branchpoint_trace_gate.py",
        "python tools/run_release_gate.py",
        "python -m pytest -q tests",
        "```",
        "",
        "## Next Direction",
        "",
        "`Stage88` should add external human/editor/reader benchmark evidence against the 8-16 episode scale-up pack.",
        "",
        f"Repository root: `{root}`",
    ])


if __name__ == "__main__":
    result = export_stage87_artifacts()
    print(json.dumps(result, ensure_ascii=True, indent=2))
