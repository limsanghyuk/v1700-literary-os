from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from v1700.gates.release_gate import run_release_gate
from v1700.gates.stage96_release_gate import run_stage96_release_gate
from v1700.manuscript_learning.learning_report import build_stage96_manuscript_learning_manifest
from v1700.narrative_optimization.report import build_stage96_narrative_optimization_manifest
from v1700.provider_ensemble.decision_report import build_stage96_provider_ensemble_manifest
from v1700.stage96.orchestrator import run_stage96_pipeline
from v1700.stage96.release_contract import build_stage96_branchpoint_trace_manifest, build_stage96_manifest

ROOT = Path(__file__).resolve().parents[1]
RELEASE = ROOT / "release" / "current"
MANIFESTS = ROOT / "manifests"


def main() -> int:
    RELEASE.mkdir(parents=True, exist_ok=True)
    MANIFESTS.mkdir(parents=True, exist_ok=True)
    pipeline = run_stage96_pipeline(ROOT)
    checks = pipeline["checks"]
    written = {}
    for key, path_name in (
        ("narrative_optimization", "stage96_narrative_optimization_report.json"),
        ("manuscript_learning", "stage96_manuscript_learning_report.json"),
        ("provider_ensemble", "stage96_provider_ensemble_report.json"),
    ):
        path = RELEASE / path_name
        path.write_text(json.dumps(checks[key], ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        written[key] = str(path.relative_to(ROOT))

    memory_path = RELEASE / "stage96_coefficient_memory.json"
    memory_path.write_text(
        json.dumps(checks["manuscript_learning"]["coefficient_memory"], ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    written["coefficient_memory"] = str(memory_path.relative_to(ROOT))

    gate = run_stage96_release_gate(ROOT)
    gate_path = RELEASE / "stage96_release_gate_report.json"
    gate_path.write_text(json.dumps(gate, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    written["stage96_release_gate"] = str(gate_path.relative_to(ROOT))

    main_gate = run_release_gate()
    main_path = RELEASE / "release_gate_report.json"
    main_path.write_text(json.dumps(main_gate, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    written["release_gate"] = str(main_path.relative_to(ROOT))

    manifest_map = {
        "stage96_manifest.json": build_stage96_manifest(),
        "stage96_branchpoint_trace_manifest.json": build_stage96_branchpoint_trace_manifest(),
        "stage96_narrative_optimization_manifest.json": build_stage96_narrative_optimization_manifest(),
        "stage96_manuscript_learning_manifest.json": build_stage96_manuscript_learning_manifest(),
        "stage96_provider_ensemble_manifest.json": build_stage96_provider_ensemble_manifest(),
    }
    for name, payload in manifest_map.items():
        path = MANIFESTS / name
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        written[name] = str(path.relative_to(ROOT))

    handoff_path = RELEASE / "stage96_developer_handoff_report.md"
    handoff_path.write_text(_handoff(gate) + "\n", encoding="utf-8")
    written["developer_handoff"] = str(handoff_path.relative_to(ROOT))
    print(json.dumps({"status": gate["status"], "artifacts": written}, ensure_ascii=True, indent=2))
    return 0 if gate.get("status") == "pass" else 1


def _handoff(gate: dict) -> str:
    return "\n".join(
        [
            "# Stage96 Developer Handoff",
            "",
            "Stage96 integrates Narrative Physics Optimization, Manuscript Learning, and Provider Ensemble Arbitration.",
            "",
            "## Runtime Boundary",
            "",
            "- Release gates use dry-run fixture candidates only.",
            "- Raw manuscript text remains local and is reduced to feature summaries.",
            "- Provider candidates are inputs; V1700 Narrative Physics remains the authority.",
            "- Merge output is directive-level, never provider text concatenation.",
            "",
            "## Evidence",
            "",
            f"- Stage96 gate: `{gate['status']}`",
            f"- Provider calls: `{gate['provider_call_count']}`",
            f"- Node2 raw reveal access: `{gate['node2_raw_reveal_access']}`",
            "",
            "## Commands",
            "",
            "```bash",
            "python tools/run_stage96_narrative_optimization.py",
            "python tools/run_stage96_manuscript_learning.py",
            "python tools/run_stage96_provider_ensemble.py",
            "python tools/run_stage96_release_gate.py",
            "python tools/run_release_gate.py",
            "```",
        ]
    )


if __name__ == "__main__":
    raise SystemExit(main())
