from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from v1700.stage103.orchestrator import run_stage103
from v1700.stage103.release_notes import PACKAGE_NAME
from v1700.stage103.report import write_json, write_summary


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    report = run_stage103(root)
    package_dir = root.parents[1] / "packages" if len(root.parents) > 1 else root.parent / "packages"
    payload = {
        "stage": "103",
        "status": report.get("status"),
        "canonical_package": PACKAGE_NAME,
        "canonical_package_path": str(package_dir / PACKAGE_NAME),
        "sha256_sidecar": f"{PACKAGE_NAME}.sha256",
        "filelist": "V1700_stage103_FIXED_filelist.txt",
        "release_evidence": [
            "release/current/stage103_production_hardening_report.json",
            "release/current/stage103_release_gate_report.json",
            "release/current/stage103_developer_handoff_report.md",
        ],
    }
    write_json(root / "release" / "current" / "stage103_artifact_export_report.json", payload)
    write_summary(
        root / "release" / "current" / "stage103_artifact_export_report.md",
        "Stage103 Artifact Export",
        [
            f"canonical package: {PACKAGE_NAME}",
            "sidecars: sha256 and filelist",
            f"stage103 status: {report.get('status')}",
        ],
    )
    print(json.dumps(payload, ensure_ascii=True, indent=2))
    return 0 if report.get("status") == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
