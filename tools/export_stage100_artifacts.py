from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from v1700.gates.stage100_release_gate import run_stage100_release_gate


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    report = run_stage100_release_gate(root)
    pack_dirs = [
        root / "release" / "current" / "stage100_gitnexus_rc_pack",
        root / "release" / "current" / "stage100_evaluation_pack",
        root / "release" / "current" / "stage100_provider_pack",
    ]
    files = sorted(
        path.relative_to(root).as_posix()
        for pack in pack_dirs
        if pack.exists()
        for path in pack.rglob("*")
        if path.is_file()
    )
    extra = [
        "release/current/stage100_release_gate_report.json",
        "release/current/stage100_literary_os_rc_report.json",
        "release/current/stage100_developer_handoff_report.md",
        "release/current/stage100_dual_mode_evaluation_report.json",
        "release/current/stage100_provider_certification_report.json",
        "release/current/stage100_v430_comparison_report.json",
        "release/current/stage100_v430_absorption_candidate_matrix.json",
    ]
    files.extend(rel for rel in extra if (root / rel).exists())
    package_name = "V1700_stage100_literary_os_1_0_release_candidate_FIXED.zip"
    payload = {
        "status": "pass" if report.get("status") == "pass" else "blocked",
        "stage100_release_gate_status": report.get("status"),
        "canonical_package": package_name,
        "sha256_sidecar": f"{package_name}.sha256",
        "filelist": "V1700_stage100_FIXED_filelist.txt",
        "files": sorted(set(files)),
    }
    out = root / "release" / "current" / "stage100_artifact_export_report.json"
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=True, indent=2))
    return 0 if payload["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
