from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from v1700.gates.stage105_release_gate import run_stage105_release_gate


def export_stage105_artifacts(root: Path | None = None) -> dict:
    root = root or Path(__file__).resolve().parents[1]
    gate = run_stage105_release_gate(root)
    package_name = "V1700_stage105_multi_provider_creative_arbitration_2_FIXED.zip"
    payload = {
        "stage": "105",
        "status": gate.get("status"),
        "package": package_name,
        "sha256_sidecar": f"{package_name}.sha256",
        "filelist": "V1700_stage105_FIXED_filelist.txt",
        "release_gate": "release/current/stage105_release_gate_report.json",
        "developer_handoff": "release/current/stage105_developer_handoff_report.md",
    }
    out = root / "release" / "current" / "stage105_artifact_export_report.json"
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return payload


if __name__ == "__main__":
    result = export_stage105_artifacts()
    print(json.dumps(result, ensure_ascii=True, indent=2))
    raise SystemExit(0 if result.get("status") == "pass" else 1)
