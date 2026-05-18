from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.gates.graph_nexus_release_gate import run_graph_nexus_release_gate
from v1700.gates.release_gate import run_release_gate
from v1700.gates.stage85_release_gate import run_stage85_release_gate
from v1700.traceability.index_quality import export_gitnexus_index_quality_report
from v1700.traceability.symbol_trace import export_symbol_to_branchpoint_trace_manifest


def _project_root() -> Path:
    return Path(__file__).resolve().parents[3]


def export_stage85_artifacts(root: Path | None = None) -> dict[str, str]:
    root = root or _project_root()
    written: dict[str, str] = {}
    written.update(export_symbol_to_branchpoint_trace_manifest(root))
    written.update(export_gitnexus_index_quality_report(root))

    graph_nexus = run_graph_nexus_release_gate(root)
    main_release = run_release_gate()
    gate = run_stage85_release_gate(root)
    release_dir = root / "release" / "current"
    release_dir.mkdir(parents=True, exist_ok=True)

    phase0 = {
        "stage": "85",
        "status": "pass" if graph_nexus.get("status") == "pass" and gate.get("status") == "pass" else "blocked",
        "title": "Stage85 Phase0 Baseline Lock",
        "stage84_preserved": gate["checks"]["stage84_release_gate"].get("status") == "pass",
        "graph_nexus_preserved": graph_nexus.get("status") == "pass",
        "provider_default_calls": 0,
        "node2_raw_reveal_access_count": 0,
        "gitnexus_density_baseline": (root / "release" / "current" / "stage85_gitnexus_meta_snapshot.json").exists(),
    }
    phase0_path = release_dir / "stage85_phase0_baseline_report.json"
    phase0_path.write_text(json.dumps(phase0, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    written["stage85_phase0_baseline_report"] = str(phase0_path.relative_to(root))

    gate_path = release_dir / "stage85_release_gate_report.json"
    gate_path.write_text(json.dumps(gate, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    written["stage85_release_gate_report"] = str(gate_path.relative_to(root))

    handoff = _render_developer_handoff(root, gate, main_release)
    handoff_path = release_dir / "stage85_developer_handoff_report.md"
    handoff_path.write_text(handoff + "\n", encoding="utf-8")
    written["stage85_developer_handoff_report"] = str(handoff_path.relative_to(root))

    manifest = {
        "stage": "85",
        "title": "GitNexus Density Upgrade and Symbol-to-Branchpoint Traceability",
        "status": gate["status"],
        "depends_on": ["stage84", "stage83.1", "stage72.1"],
        "required_outputs": [
            "manifests/symbol_to_branchpoint_trace_manifest.json",
            "release/current/stage85_gitnexus_index_quality_report.json",
            "release/current/stage85_release_gate_report.json",
            "tools/export_stage85_artifacts.py",
            "tools/run_stage85_release_gate.py",
            "tests/test_stage85_traceability.py",
        ],
        "provider_default_calls": 0,
        "node2_raw_reveal_access_count": 0,
    }
    manifest_path = root / "manifests" / "stage85_manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    written["stage85_manifest"] = str(manifest_path.relative_to(root))
    return written


def _render_developer_handoff(root: Path, gate: dict[str, Any], main_release: dict[str, Any]) -> str:
    quality = gate["checks"]["gitnexus_index_quality_gate"]
    metrics = quality["metrics"]
    trace = gate["checks"]["symbol_to_branchpoint_trace_gate"]["symbol_to_branchpoint_trace_manifest"]
    return "\n".join(
        [
            "# Stage85 Developer Handoff Report",
            "",
            "## Status",
            "",
            f"- Stage85 release gate: `{gate['status']}`",
            f"- Main release gate: `{main_release['status']}`",
            "- Provider default calls: `0`",
            "- Node2 raw reveal access: `0`",
            "",
            "## GitNexus Index Quality",
            "",
            f"- Files: `{metrics['files']}`",
            f"- Nodes: `{metrics['nodes']}`",
            f"- Edges: `{metrics['edges']}`",
            f"- Clusters: `{metrics['clusters']}`",
            f"- Flows: `{metrics['flows']}`",
            f"- Meta source: `{quality['meta_source']}`",
            "",
            "## Symbol-to-Branchpoint Coverage",
            "",
            f"- Entries: `{trace['entry_count']}`",
            f"- P0 coverage: `{trace['coverage']['P0']['coverage']}`",
            f"- P1 coverage: `{trace['coverage']['P1']['coverage']}`",
            f"- Overall coverage: `{trace['coverage']['overall']['coverage']}`",
            "",
            "## Developer Commands",
            "",
            "```bash",
            "python tools/run_symbol_to_branchpoint_trace_gate.py",
            "python tools/run_stage85_gitnexus_index_quality_gate.py",
            "python tools/run_stage85_release_gate.py",
            "python tools/run_release_gate.py",
            "```",
            "",
            "## Important Boundary",
            "",
            "GitNexus is optional developer impact evidence. GraphNexus remains the internal authority graph, and Python fallback remains required.",
            "",
            f"Repository root: `{root}`",
        ]
    )
