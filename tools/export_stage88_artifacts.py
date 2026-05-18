from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from v1700.agent_benchmark.harness import run_stage88_agent_benchmark_smoke
from v1700.gates.release_gate import run_release_gate
from v1700.gates.stage88_release_gate import run_stage88_release_gate
from v1700.traceability.index_quality import build_gitnexus_index_quality_report
from v1700.traceability.symbol_trace import build_symbol_to_branchpoint_trace_manifest, export_symbol_to_branchpoint_trace_manifest


def _project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def export_stage88_artifacts(root: Path | None = None) -> dict[str, str]:
    root = root or _project_root()
    written: dict[str, str] = {}
    release_dir = root / "release" / "current"
    release_dir.mkdir(parents=True, exist_ok=True)

    benchmark = run_stage88_agent_benchmark_smoke()
    benchmark_path = release_dir / "stage88_agent_benchmark_report.json"
    benchmark_path.write_text(json.dumps(benchmark, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    written["stage88_agent_benchmark_report"] = str(benchmark_path.relative_to(root))

    manifest = {
        "stage": "88",
        "title": "AI-Agent Editor/Reader Blind Benchmark",
        "status": "pending",
        "depends_on": ["stage87", "stage86", "stage85", "stage84", "stage83.1"],
        "substitution_policy": {
            "external_human_editors": "replaced_by_local_ai_editor_agents",
            "external_human_readers": "replaced_by_local_ai_reader_agents",
            "provider_default_calls": 0,
            "human_benchmark_required": False,
        },
        "required_outputs": [
            "src/v1700/agent_benchmark/contracts.py",
            "src/v1700/agent_benchmark/agents.py",
            "src/v1700/agent_benchmark/harness.py",
            "src/v1700/gates/stage88_release_gate.py",
            "tools/run_stage88_agent_benchmark.py",
            "tools/run_stage88_release_gate.py",
            "tools/export_stage88_artifacts.py",
            "tests/test_stage88_agent_benchmark.py",
            "manifests/stage88_branchpoint_trace_manifest.json",
            "release/current/stage88_agent_benchmark_report.json",
            "release/current/stage88_release_gate_report.json",
        ],
        "benchmark_targets": {
            "minimum_agent_count": 6,
            "minimum_blind_sample_count": 16,
            "default_agent_count": benchmark["agent_count"],
            "default_sample_count": benchmark["sample_count"],
            "pass_threshold": benchmark["pass_threshold"],
            "consensus_score": benchmark["consensus_score"],
            "min_agent_average": benchmark["min_agent_average"],
            "min_sample_average": benchmark["min_sample_average"],
        },
        "provider_default_calls": 0,
        "node2_raw_reveal_access_count": 0,
    }
    manifest_path = root / "manifests" / "stage88_manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    written["stage88_manifest"] = str(manifest_path.relative_to(root))

    written.update(export_symbol_to_branchpoint_trace_manifest(root))

    gate = run_stage88_release_gate(root)
    gate_path = release_dir / "stage88_release_gate_report.json"
    gate_path.write_text(json.dumps(gate, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    written["stage88_release_gate_report"] = str(gate_path.relative_to(root))

    main_release = run_release_gate()
    main_path = release_dir / "release_gate_report.json"
    main_path.write_text(json.dumps(main_release, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    written["release_gate_report"] = str(main_path.relative_to(root))

    stage88_quality = build_gitnexus_index_quality_report(root)
    stage88_quality["stage"] = "88"
    stage88_quality["title"] = "Stage88 GitNexus Index Quality Snapshot"
    quality_path = release_dir / "stage88_gitnexus_index_quality_report.json"
    quality_path.write_text(json.dumps(stage88_quality, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    written["stage88_gitnexus_index_quality_report"] = str(quality_path.relative_to(root))

    trace_manifest = build_symbol_to_branchpoint_trace_manifest(root)
    stage88_trace = {
        **trace_manifest,
        "entries": [entry for entry in trace_manifest["entries"] if entry["branchpoint_id"].startswith("BP_STAGE88_")],
    }
    trace_path = root / "manifests" / "stage88_branchpoint_trace_manifest.json"
    trace_path.write_text(json.dumps(stage88_trace, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    written["stage88_branchpoint_trace_manifest"] = str(trace_path.relative_to(root))

    manifest["status"] = gate["status"]
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    handoff_path = release_dir / "stage88_developer_handoff_report.md"
    handoff_path.write_text(_render_developer_handoff(root, gate, benchmark, main_release) + "\n", encoding="utf-8")
    written["stage88_developer_handoff_report"] = str(handoff_path.relative_to(root))
    return written


def _render_developer_handoff(root: Path, gate: dict[str, Any], benchmark: dict[str, Any], main_release: dict[str, Any]) -> str:
    return "\n".join([
        "# Stage88 Developer Handoff Report",
        "",
        "## Status",
        "",
        f"- Stage88 release gate: `{gate['status']}`",
        f"- Main release gate: `{main_release['status']}`",
        "- Provider default calls: `0`",
        "- Node2 raw reveal access: `0`",
        "",
        "## AI-Agent Blind Benchmark",
        "",
        f"- Agent count: `{benchmark['agent_count']}`",
        f"- Blind sample count: `{benchmark['sample_count']}`",
        f"- Assessment count: `{benchmark['assessment_count']}`",
        f"- Consensus score: `{benchmark['consensus_score']}`",
        f"- Minimum agent average: `{benchmark['min_agent_average']}`",
        f"- Minimum sample average: `{benchmark['min_sample_average']}`",
        "",
        "## What Stage88 Proves",
        "",
        "- External human/editor/reader benchmark is replaced by local AI editor/reader agents per user direction.",
        "- Six role-separated artificial reviewer agents evaluate blinded Stage87 scale-up samples.",
        "- The benchmark is deterministic and does not call external providers by default.",
        "- Stage87 8/16 episode scale-up evidence remains the evaluated source pack.",
        "- Stage86 Arc-Reveal-Knowledge and Stage85 traceability remain inherited release conditions.",
        "",
        "## Developer Commands",
        "",
        "```bash",
        "python -m pip install -e .",
        "python tools/run_stage88_agent_benchmark.py",
        "python tools/run_stage88_release_gate.py",
        "python tools/run_symbol_to_branchpoint_trace_gate.py",
        "python tools/run_release_gate.py",
        "python -m pytest -q tests",
        "```",
        "",
        "## Next Direction",
        "",
        "`Stage89` should add Writer Studio UI + Export Pipeline around the Stage88 agent-benchmark-protected engine.",
        "",
        f"Repository root: `{root}`",
    ])


if __name__ == "__main__":
    result = export_stage88_artifacts()
    print(json.dumps(result, ensure_ascii=True, indent=2))
