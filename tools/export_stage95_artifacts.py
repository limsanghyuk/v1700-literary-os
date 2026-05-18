from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from v1700.gates.release_gate import run_release_gate
from v1700.gates.stage95_release_gate import run_stage95_release_gate
from v1700.narrative_physics.engine import run_stage95_narrative_physics_smoke
from v1700.narrative_physics.report import build_stage95_narrative_physics_manifest

ROOT = Path(__file__).resolve().parents[1]
RELEASE = ROOT / "release" / "current"


def main() -> int:
    RELEASE.mkdir(parents=True, exist_ok=True)
    written = {}

    physics = run_stage95_narrative_physics_smoke()
    physics_path = RELEASE / "stage95_narrative_physics_report.json"
    physics_path.write_text(json.dumps(physics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    written["stage95_narrative_physics_report"] = str(physics_path.relative_to(ROOT))

    gate = run_stage95_release_gate(ROOT)
    gate_path = RELEASE / "stage95_release_gate_report.json"
    gate_path.write_text(json.dumps(gate, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    written["stage95_release_gate_report"] = str(gate_path.relative_to(ROOT))

    main_gate = run_release_gate()
    main_path = RELEASE / "release_gate_report.json"
    main_path.write_text(json.dumps(main_gate, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    written["release_gate_report"] = str(main_path.relative_to(ROOT))

    manifest = build_stage95_narrative_physics_manifest()
    manifest_path = ROOT / "manifests" / "stage95_narrative_physics_manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    written["stage95_narrative_physics_manifest"] = str(manifest_path.relative_to(ROOT))

    handoff_path = RELEASE / "stage95_developer_handoff_report.md"
    handoff_path.write_text(_handoff(physics) + "\n", encoding="utf-8")
    written["stage95_developer_handoff_report"] = str(handoff_path.relative_to(ROOT))

    print(json.dumps({"status": "pass" if gate.get("status") == "pass" else "blocked", "artifacts": written}, ensure_ascii=True, indent=2))
    return 0 if gate.get("status") == "pass" else 1


def _handoff(physics: dict) -> str:
    return "\n".join(
        [
            "# Stage95 Developer Handoff",
            "",
            "Stage95 introduces the V1700 Native Narrative Physics Engine.",
            "",
            "## Runtime Boundary",
            "",
            "- Provider ensemble arbitration moves to Stage96.",
            "- Release verification performs zero live provider calls.",
            "- Node2 receives surface-safe transform evidence only.",
            "- Branchpoint survival remains the release authority.",
            "",
            "## Evidence",
            "",
            f"- Tensor shape: `{physics['tensor']['matrix_shape']}`",
            f"- Reveal entropy status: `{physics['reveal_entropy']['status']}`",
            f"- Scene energy status: `{physics['scene_energy']['status']}`",
            f"- Branchpoint survival status: `{physics['branchpoint_survival']['status']}`",
            "",
            "## Commands",
            "",
            "```bash",
            "python tools/run_stage95_narrative_physics_smoke.py",
            "python tools/run_stage95_release_gate.py",
            "python tools/run_release_gate.py",
            "```",
        ]
    )


if __name__ == "__main__":
    raise SystemExit(main())
