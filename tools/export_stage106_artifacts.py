from __future__ import annotations
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from v1700.stage106.orchestrator import run_stage106

def export_stage106_artifacts(root: Path | None = None) -> dict:
    root = root or Path(__file__).resolve().parents[1]
    report = run_stage106(root)
    files = [
        "release/current/stage106_adaptive_author_profile_style_genome_report.json",
        "release/current/stage106_release_gate_report.json",
        "release/current/stage106_developer_handoff_report.md",
    ]
    payload = {"stage":"106", "status": report.get("status"), "artifact_files": files, "canonical_package":"V1700_stage106_adaptive_author_profile_style_genome_FIXED.zip"}
    out = root / "release" / "current" / "stage106_artifact_export_report.json"
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return payload
if __name__ == "__main__":
    result = export_stage106_artifacts()
    print(json.dumps(result, ensure_ascii=True, indent=2))
    raise SystemExit(0 if result.get("status") == "pass" else 1)
