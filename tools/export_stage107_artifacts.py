from __future__ import annotations
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from v1700.stage107.orchestrator import run_stage107

def export_stage107_artifacts(root: Path | None = None) -> dict:
    root = root or Path(__file__).resolve().parents[1]
    report = run_stage107(root)
    files = [
        "release/current/stage107_longform_production_suite_report.json",
        "release/current/stage107_release_gate_report.json",
        "release/current/stage107_developer_handoff_report.md",
    ]
    payload = {"stage": "107", "status": report.get("status"), "artifact_files": files, "canonical_package": "V1700_stage107_longform_production_suite_FIXED.zip"}
    out = root / "release" / "current" / "stage107_artifact_export_report.json"
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return payload

if __name__ == "__main__":
    result = export_stage107_artifacts()
    print(json.dumps(result, ensure_ascii=True, indent=2))
    raise SystemExit(0 if result.get("status") == "pass" else 1)
