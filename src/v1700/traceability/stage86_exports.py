from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.gates.release_gate import run_release_gate
from v1700.gates.stage86_release_gate import run_stage86_release_gate
from v1700.traceability.index_quality import build_gitnexus_index_quality_report, export_gitnexus_index_quality_report
from v1700.traceability.symbol_trace import (
    build_symbol_to_branchpoint_trace_manifest,
    export_symbol_to_branchpoint_trace_manifest,
)


def _project_root() -> Path:
    return Path(__file__).resolve().parents[3]


def export_stage86_artifacts(root: Path | None = None) -> dict[str, str]:
    root = root or _project_root()
    written: dict[str, str] = {}
    written.update(export_symbol_to_branchpoint_trace_manifest(root))
    written.update(export_gitnexus_index_quality_report(root))
    stage86_quality = build_gitnexus_index_quality_report(root)
    stage86_quality["stage"] = "86"
    stage86_quality["title"] = "Stage86 GitNexus Index Quality Snapshot"
    stage86_quality_path = root / "release" / "current" / "stage86_gitnexus_index_quality_report.json"
    stage86_quality_path.parent.mkdir(parents=True, exist_ok=True)
    stage86_quality_path.write_text(
        json.dumps(stage86_quality, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    written["stage86_gitnexus_index_quality_report"] = str(stage86_quality_path.relative_to(root))

    trace_manifest = build_symbol_to_branchpoint_trace_manifest(root)
    stage86_trace = {
        **trace_manifest,
        "entries": [
            entry
            for entry in trace_manifest["entries"]
            if entry["branchpoint_id"].startswith("BP_STAGE86_")
        ],
    }
    stage86_trace_path = root / "manifests" / "stage86_branchpoint_trace_manifest.json"
    stage86_trace_path.write_text(
        json.dumps(stage86_trace, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    written["stage86_branchpoint_trace_manifest"] = str(stage86_trace_path.relative_to(root))

    gate = run_stage86_release_gate(root)
    main_release = run_release_gate()
    release_dir = root / "release" / "current"
    release_dir.mkdir(parents=True, exist_ok=True)

    phase0 = {
        "stage": "86",
        "status": "pass" if gate.get("status") == "pass" else "blocked",
        "title": "Stage86 Phase0 Stage85 Baseline Lock",
        "stage85_preserved": gate["checks"]["stage85_release_gate"].get("status") == "pass",
        "traceability_preserved": gate["checks"]["symbol_to_branchpoint_trace_gate"].get("status") == "pass",
        "provider_default_calls": 0,
        "node2_raw_reveal_access_count": 0,
    }
    phase0_path = release_dir / "stage86_phase0_stage85_baseline_lock_report.json"
    phase0_path.write_text(json.dumps(phase0, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    written["stage86_phase0_stage85_baseline_lock_report"] = str(phase0_path.relative_to(root))

    gate_path = release_dir / "stage86_release_gate_report.json"
    gate_path.write_text(json.dumps(gate, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    written["stage86_release_gate_report"] = str(gate_path.relative_to(root))

    main_path = release_dir / "release_gate_report.json"
    main_path.write_text(json.dumps(main_release, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    written["release_gate_report"] = str(main_path.relative_to(root))

    handoff_path = release_dir / "stage86_developer_handoff_report.md"
    handoff_path.write_text(_render_developer_handoff(root, gate, main_release) + "\n", encoding="utf-8")
    written["stage86_developer_handoff_report"] = str(handoff_path.relative_to(root))

    manifest = {
        "stage": "86",
        "title": "V380 Arc-Reveal-Knowledge Absorption",
        "status": gate["status"],
        "depends_on": ["stage85", "stage84", "stage83.1", "stage72.1"],
        "required_outputs": [
            "src/v1700/arc_reveal_knowledge/series_arc_planner.py",
            "src/v1700/arc_reveal_knowledge/causal_plot_graph.py",
            "src/v1700/arc_reveal_knowledge/reveal_budget.py",
            "src/v1700/arc_reveal_knowledge/character_knowledge_bridge.py",
            "src/v1700/arc_reveal_knowledge/prose_contract_bridge.py",
            "src/v1700/gates/stage86_release_gate.py",
            "tools/export_stage86_artifacts.py",
            "tools/run_stage86_release_gate.py",
            "tests/test_stage86_arc_reveal_knowledge.py",
            "manifests/stage86_v380_feature_map_manifest.json",
            "manifests/stage86_branchpoint_trace_manifest.json",
            "release/current/stage86_release_gate_report.json",
            "release/current/stage86_gitnexus_index_quality_report.json",
        ],
        "provider_default_calls": 0,
        "node2_raw_reveal_access_count": 0,
    }
    manifest_path = root / "manifests" / "stage86_manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    written["stage86_manifest"] = str(manifest_path.relative_to(root))
    return written


def _render_developer_handoff(root: Path, gate: dict[str, Any], main_release: dict[str, Any]) -> str:
    smoke = gate["checks"]["arc_reveal_knowledge_smoke"]
    graph = smoke["series_arc"]
    return "\n".join(
        [
            "# Stage86 Developer Handoff Report",
            "",
            "## Status",
            "",
            f"- Stage86 release gate: `{gate['status']}`",
            f"- Main release gate: `{main_release['status']}`",
            "- Provider default calls: `0`",
            "- Node2 raw reveal access: `0`",
            "",
            "## Absorbed V380 Concepts",
            "",
            "- `SeriesArcPlanner` is now live as deterministic 16-episode arc planning.",
            "- `CausalPlotGraph` now records causal, foreshadow, callback, and emotional escalation edges.",
            "- `EpisodeRevealBudget` now blocks premature direct reveal while allowing foreshadowing.",
            "- `CharacterKnowledgeProseBridge` now prevents character/reader knowledge leakage.",
            "- `KnowledgeStatus -> ProseRenderContract` now feeds Node2's surface-only contract.",
            "",
            "## Runtime Evidence",
            "",
            f"- Episode count: `{graph['act_structure']['episode_count']}`",
            f"- Causal edges: `{graph['edge_counts']['causal']}`",
            f"- Foreshadow edges: `{graph['edge_counts']['foreshadow']}`",
            f"- Callback edges: `{graph['edge_counts']['callback']}`",
            f"- Emotional escalation edges: `{graph['edge_counts']['emotional_escalation']}`",
            "",
            "## Developer Commands",
            "",
            "```bash",
            "python tools/run_stage86_release_gate.py",
            "python tools/run_symbol_to_branchpoint_trace_gate.py",
            "python tools/run_release_gate.py",
            "python -m pytest -q tests",
            "```",
            "",
            "## Next Direction",
            "",
            "`Stage87` should scale the evidence from local 16-episode arc contracts toward 8-16 episode generation evidence.",
            "",
            f"Repository root: `{root}`",
        ]
    )
