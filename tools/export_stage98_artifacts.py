from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from v1700.studio_workflow.studio_orchestrator import run_stage98_studio_workflow


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    report = run_stage98_studio_workflow(root)
    pack = root / "release" / "current" / "stage98_studio_pack"
    files = sorted(str(path.relative_to(root)).replace("\\", "/") for path in pack.rglob("*") if path.is_file())
    out = root / "release" / "current" / "stage98_artifact_export_report.json"
    payload = {"status": "pass", "workflow_status": report["status"], "files": files, "full_text_exported": False}
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
