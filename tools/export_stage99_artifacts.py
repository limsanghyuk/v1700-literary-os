from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from v1700.gates.stage99_release_gate import run_stage99_release_gate


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    report = run_stage99_release_gate(root)
    pack_dirs = [
        root / "release" / "current" / "stage99_gitnexus_pack",
        root / "release" / "current" / "stage99_security_pack",
        root / "release" / "current" / "stage99_regression_freeze_pack",
    ]
    files = sorted(
        path.relative_to(root).as_posix()
        for pack in pack_dirs
        if pack.exists()
        for path in pack.rglob("*")
        if path.is_file()
    )
    payload = {"status": "pass" if report["status"] == "pass" else "blocked", "stage99_release_gate_status": report["status"], "files": files}
    out = root / "release" / "current" / "stage99_artifact_export_report.json"
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=True, indent=2))
    return 0 if payload["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
