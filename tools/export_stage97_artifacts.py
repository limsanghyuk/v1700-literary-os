from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from v1700.gates.release_gate import run_release_gate
from v1700.gates.stage97_release_gate import run_stage97_release_gate
from v1700.longform_endurance.endurance_orchestrator import run_stage97_longform_endurance
from v1700.longform_endurance.report import (
    build_stage97_branchpoint_trace_manifest,
    build_stage97_longform_endurance_manifest,
    build_stage97_manifest,
)

ROOT = Path(__file__).resolve().parents[1]
RELEASE = ROOT / "release" / "current"
PACK = RELEASE / "stage97_longform_endurance_pack"
MANIFESTS = ROOT / "manifests"


def main() -> int:
    PACK.mkdir(parents=True, exist_ok=True)
    MANIFESTS.mkdir(parents=True, exist_ok=True)
    endurance = run_stage97_longform_endurance(ROOT)
    proof = endurance["required_16_episode_proof"]
    checks = proof["checks"]
    written = {}
    _write_json(RELEASE / "stage97_longform_endurance_report.json", endurance, written)
    _write_json(PACK / "series_arc.json", {"stage": "97", "episode_count": 16, "acts": ["gi", "seung", "jeon", "gyeol"]}, written)
    _write_json(PACK / "episode_plan_16.json", proof["episodes"], written)
    _write_json(PACK / "episode_plan_24.json", endurance["extended_24_episode_proof"]["episodes"], written)
    _write_json(PACK / "scene_necessity_report.json", checks["scene_necessity"], written)
    _write_json(PACK / "payoff_debt_ledger.json", checks["payoff_debt_ledger"], written)
    _write_json(PACK / "character_agency_curves.json", checks["agency_conservation"]["character_agency_curves"], written)
    _write_json(PACK / "dramatic_load_curve.json", checks["dramatic_load_balancing"], written)
    _write_json(PACK / "dialogue_pragmatics_report.json", checks["dialogue_pragmatics"], written)
    _write_json(PACK / "voice_manifold_report.json", checks["voice_manifold"], written)
    _write_json(PACK / "attention_economy_report.json", checks["attention_economy"], written)
    _write_microplot_csv(PACK / "microplot_matrix.csv", proof["episodes"], written)
    summary_path = PACK / "endurance_summary.md"
    summary_path.write_text(_summary(endurance) + "\n", encoding="utf-8")
    written["stage97_longform_endurance_pack/endurance_summary.md"] = str(summary_path.relative_to(ROOT))
    gate = run_stage97_release_gate(ROOT)
    _write_json(RELEASE / "stage97_release_gate_report.json", gate, written)
    _write_json(RELEASE / "release_gate_report.json", run_release_gate(), written)
    _write_json(MANIFESTS / "stage97_manifest.json", build_stage97_manifest(), written)
    _write_json(MANIFESTS / "stage97_branchpoint_trace_manifest.json", build_stage97_branchpoint_trace_manifest(), written)
    _write_json(MANIFESTS / "stage97_longform_endurance_manifest.json", build_stage97_longform_endurance_manifest(), written)
    handoff = RELEASE / "stage97_developer_handoff_report.md"
    handoff.write_text(_handoff(gate) + "\n", encoding="utf-8")
    written["release/current/stage97_developer_handoff_report.md"] = str(handoff.relative_to(ROOT))
    print(json.dumps({"status": gate["status"], "artifacts": written}, ensure_ascii=True, indent=2))
    return 0 if gate.get("status") == "pass" else 1


def _write_json(path: Path, payload, written: dict) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    written[str(path.relative_to(ROOT)).replace("\\", "/")] = str(path.relative_to(ROOT))


def _write_microplot_csv(path: Path, episodes: list[dict], written: dict) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["episode_id", "act", "microplot_index", "scene_count"])
        for episode in episodes:
            for index in range(1, episode["microplot_count"] + 1):
                writer.writerow([episode["episode_id"], episode["act"], index, 3])
    written[str(path.relative_to(ROOT)).replace("\\", "/")] = str(path.relative_to(ROOT))


def _summary(endurance: dict) -> str:
    return "\n".join(
        [
            "# Stage97 Longform Endurance Summary",
            "",
            f"- Required proof status: `{endurance['required_16_episode_proof']['status']}`",
            f"- Episode count: `{endurance['episode_count_verified']}`",
            f"- Microplot count: `{endurance['microplot_count']}`",
            f"- Scene estimate: `{endurance['scene_count_estimate']}`",
            "- Provider calls: `0`",
            "- Node2 raw reveal access: `0`",
        ]
    )


def _handoff(gate: dict) -> str:
    return "\n".join(
        [
            "# Stage97 Developer Handoff",
            "",
            "Stage97 implements the Full Longform Narrative Endurance Engine.",
            "",
            f"- Gate: `{gate['status']}`",
            f"- Episodes verified: `{gate['episode_count_verified']}`",
            f"- Microplots: `{gate['microplot_count']}`",
            f"- Scene estimate: `{gate['scene_count_estimate']}`",
            f"- Critical debt defaults: `{gate['critical_debt_default_count']}`",
            f"- Provider calls: `{gate['provider_call_count']}`",
        ]
    )


if __name__ == "__main__":
    raise SystemExit(main())
