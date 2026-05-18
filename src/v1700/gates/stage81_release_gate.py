from __future__ import annotations
from pathlib import Path

from v1700.gates.stage80_release_gate import run_stage80_release_gate
from v1700.quality_endurance import QualityEnduranceGate


def run_stage81_release_gate(root: Path | None = None) -> dict:
    root = root or Path(__file__).resolve().parents[3]
    stage80 = run_stage80_release_gate(root)
    endurance = QualityEnduranceGate().validate()
    issues: list[str] = []
    if stage80.get("status") != "pass":
        issues.append("stage80_release_gate_blocked")
    if endurance.get("status") != "pass":
        issues.append("quality_endurance_gate_blocked")
    report = endurance.get("quality_endurance_report", {})
    return {
        "stage": "81",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "claim": "Stage81 applies actual-text 10-axis quality evaluation and refinement endurance to 30 Korean drama scenes.",
        "stage80_release_gate": stage80,
        "quality_endurance_gate": endurance,
        "actual_rendered_scene_count": report.get("scene_count", 0),
        "average_quality_after": report.get("average_after", 0.0),
        "average_quality_delta": report.get("average_delta", 0.0),
        "provider_default_calls": 0,
        "node2_raw_reveal_access_count": 0,
    }
