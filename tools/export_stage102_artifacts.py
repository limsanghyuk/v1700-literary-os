from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from v1700.gates.stage102_release_gate import run_stage102_release_gate


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    gate = run_stage102_release_gate(root)
    pack_dirs = [
        root / "release" / "current" / "stage102_writer_trial_pack",
        root / "release" / "current" / "stage102_blind_benchmark_pack",
        root / "release" / "current" / "stage102_revision_efficiency_pack",
    ]
    files = sorted(
        path.relative_to(root).as_posix()
        for pack in pack_dirs
        if pack.exists()
        for path in pack.rglob("*")
        if path.is_file()
    )
    extra = [
        "release/current/stage102_0_preflight_report.json",
        "release/current/stage102_writer_trial_report.json",
        "release/current/stage102_blind_benchmark_report.json",
        "release/current/stage102_revision_efficiency_report.json",
        "release/current/stage102_real_writer_trial_report.json",
        "release/current/stage102_release_gate_report.json",
        "release/current/stage102_developer_handoff_report.md",
        "release/current/stage102_gitnexus_index_report.json",
    ]
    files.extend(rel for rel in extra if (root / rel).exists())
    package_name = "V1700_stage102_real_writer_trial_blind_benchmark_FIXED.zip"
    payload = {
        "status": "pass" if gate.get("status") == "pass" else "blocked",
        "stage102_release_gate_status": gate.get("status"),
        "canonical_package": package_name,
        "sha256_sidecar": f"{package_name}.sha256",
        "filelist": "V1700_stage102_FIXED_filelist.txt",
        "files": sorted(set(files)),
    }
    out = root / "release" / "current" / "stage102_artifact_export_report.json"
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=True, indent=2))
    return 0 if payload["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
