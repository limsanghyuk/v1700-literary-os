from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from v1700.stage104.orchestrator import run_stage104
from v1700.studio_beta.report import write_json, write_summary

PACKAGE_NAME = "V1700_stage104_commercial_writer_studio_beta_FIXED.zip"


def export_stage104_artifacts(root: Path | None = None) -> dict:
    root = root or Path(__file__).resolve().parents[1]
    report = run_stage104(root)
    payload = {
        "stage": "104",
        "status": report.get("status"),
        "package": PACKAGE_NAME,
        "canonical_package": PACKAGE_NAME,
        "sha256_sidecar": f"{PACKAGE_NAME}.sha256",
        "filelist": "V1700_stage104_FIXED_filelist.txt",
        "release_evidence": [
            "release/current/stage104_commercial_writer_studio_beta_report.json",
            "release/current/stage104_release_gate_report.json",
            "release/current/stage104_developer_handoff_report.md",
        ],
    }
    write_json(root / "release" / "current" / "stage104_artifact_export_report.json", payload)
    write_summary(root / "release" / "current" / "stage104_artifact_export_report.md", "Stage104 Artifact Export", [
        f"status: {payload['status']}",
        f"package: {PACKAGE_NAME}",
        "Stage104 exports local-first Studio Beta evidence and package metadata.",
    ])
    return payload


if __name__ == "__main__":
    result = export_stage104_artifacts()
    print(json.dumps(result, ensure_ascii=True, indent=2))
    raise SystemExit(0 if result.get("status") == "pass" else 1)
