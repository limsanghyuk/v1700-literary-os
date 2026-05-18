from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from v1700.gates.stage101_release_gate import run_stage101_release_gate


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    gate = run_stage101_release_gate(root)
    pack_dirs = [
        root / "release" / "current" / "stage101_cross_lineage_pack",
        root / "release" / "current" / "stage101_scenario_room_pack",
    ]
    files = sorted(
        path.relative_to(root).as_posix()
        for pack in pack_dirs
        if pack.exists()
        for path in pack.rglob("*")
        if path.is_file()
    )
    extra = [
        "release/current/stage101_0_cross_lineage_preflight_report.json",
        "release/current/stage101_v430_source_probe_report.json",
        "release/current/stage101_absorption_candidate_matrix.json",
        "release/current/stage101_scenario_room_contract_report.json",
        "release/current/stage101_scenario_cue_integration_report.json",
        "release/current/stage101_dual_mode_regression_report.json",
        "release/current/stage101_cross_lineage_scenario_room_report.json",
        "release/current/stage101_gitnexus_index_report.json",
        "release/current/stage101_release_gate_report.json",
        "release/current/stage101_developer_handoff_report.md",
    ]
    files.extend(rel for rel in extra if (root / rel).exists())
    package_name = "V1700_stage101_cross_lineage_absorption_scenario_room_FIXED.zip"
    payload = {
        "status": "pass" if gate.get("status") == "pass" else "blocked",
        "stage101_release_gate_status": gate.get("status"),
        "canonical_package": package_name,
        "sha256_sidecar": f"{package_name}.sha256",
        "filelist": "V1700_stage101_FIXED_filelist.txt",
        "files": sorted(set(files)),
    }
    out = root / "release" / "current" / "stage101_artifact_export_report.json"
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=True, indent=2))
    return 0 if payload["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
