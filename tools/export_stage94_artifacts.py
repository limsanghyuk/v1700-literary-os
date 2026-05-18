from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from v1700.gates.release_gate import run_release_gate
from v1700.gates.stage94_release_gate import run_stage94_release_gate
from v1700.provider_evaluation.harness import run_stage94_provider_evaluation_smoke
from v1700.provider_evaluation.report import build_stage94_provider_evaluation_manifest
from v1700.traceability.index_quality import build_gitnexus_index_quality_report
from v1700.traceability.symbol_trace import build_symbol_to_branchpoint_trace_manifest, export_symbol_to_branchpoint_trace_manifest


ROOT = Path(__file__).resolve().parents[1]
RELEASE = ROOT / "release" / "current"


def main() -> int:
    RELEASE.mkdir(parents=True, exist_ok=True)
    written = {}
    written.update(export_symbol_to_branchpoint_trace_manifest(ROOT))

    evaluation = run_stage94_provider_evaluation_smoke()
    evaluation_path = RELEASE / "stage94_provider_evaluation_report.json"
    evaluation_path.write_text(json.dumps(evaluation, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    written["stage94_provider_evaluation_report"] = str(evaluation_path.relative_to(ROOT))

    gate = run_stage94_release_gate(ROOT)
    gate_path = RELEASE / "stage94_release_gate_report.json"
    gate_path.write_text(json.dumps(gate, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    written["stage94_release_gate_report"] = str(gate_path.relative_to(ROOT))

    main_release = run_release_gate()
    main_path = RELEASE / "release_gate_report.json"
    main_path.write_text(json.dumps(main_release, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    written["release_gate_report"] = str(main_path.relative_to(ROOT))

    quality = build_gitnexus_index_quality_report(ROOT)
    quality["stage"] = "94"
    quality["title"] = "Stage94 GitNexus Index Quality Snapshot"
    quality_path = RELEASE / "stage94_gitnexus_index_quality_report.json"
    quality_path.write_text(json.dumps(quality, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    written["stage94_gitnexus_index_quality_report"] = str(quality_path.relative_to(ROOT))

    manifest = build_stage94_provider_evaluation_manifest()
    manifest_path = ROOT / "manifests" / "stage94_provider_evaluation_manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    written["stage94_provider_evaluation_manifest"] = str(manifest_path.relative_to(ROOT))

    trace = build_symbol_to_branchpoint_trace_manifest(ROOT)
    stage94_trace = {
        **trace,
        "entries": [entry for entry in trace["entries"] if entry["branchpoint_id"].startswith("BP_STAGE94_")],
    }
    stage94_trace_path = ROOT / "manifests" / "stage94_branchpoint_trace_manifest.json"
    stage94_trace_path.write_text(json.dumps(stage94_trace, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    written["stage94_branchpoint_trace_manifest"] = str(stage94_trace_path.relative_to(ROOT))

    handoff_path = RELEASE / "stage94_developer_handoff_report.md"
    handoff_path.write_text(_handoff(evaluation) + "\n", encoding="utf-8")
    written["stage94_developer_handoff_report"] = str(handoff_path.relative_to(ROOT))

    print(json.dumps({"status": "pass", "artifacts": written}, ensure_ascii=True, indent=2))
    return 0


def _handoff(evaluation: dict) -> str:
    return "\n".join(
        [
            "# Stage94 Developer Handoff",
            "",
            "Stage94 adds a dry-run provider evaluation harness for Ollama, GPT, Claude, and Gemini.",
            "",
            "## Runtime Boundary",
            "",
            "- Release gates perform zero live provider calls.",
            "- Credential values are not written to reports.",
            "- Provider responses are normalized before scoring.",
            "- Node2 raw reveal access remains zero.",
            "",
            "## Evidence",
            "",
            f"- Provider count: `{evaluation['provider_count']}`",
            f"- Prompt count: `{evaluation['prompt_count']}`",
            f"- Evaluation count: `{evaluation['evaluation_count']}`",
            f"- Best provider by deterministic score: `{evaluation['best_provider_id']}`",
            "",
            "## Commands",
            "",
            "```bash",
            "python tools/run_stage94_provider_evaluation.py",
            "python tools/run_stage94_release_gate.py",
            "python tools/run_release_gate.py",
            "```",
        ]
    )


if __name__ == "__main__":
    raise SystemExit(main())
