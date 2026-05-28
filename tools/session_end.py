from __future__ import annotations

import json
import subprocess
from pathlib import Path


def _git_value(root: Path, args: list[str], fallback: str = "") -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=root,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=30,
        check=False,
    )
    output = ((result.stdout or "") + (result.stderr or "")).strip()
    return output.splitlines()[0].strip() if result.returncode == 0 and output else fallback


def run_session_end(root: Path | None = None) -> dict:
    root = root or Path(__file__).resolve().parents[1]
    payload = {
        "stage": "session_end",
        "status": "pass",
        "branch": _git_value(root, ["rev-parse", "--abbrev-ref", "HEAD"], "DETACHED_HEAD"),
        "head": _git_value(root, ["rev-parse", "HEAD"]),
        "git_status": _git_value(root, ["status", "--short", "--branch"]),
        "required_closure": [
            "Update docs or session note when authority changed.",
            "Commit and push the branch when the work unit is complete.",
            "If release closure is in scope, verify PR, merge, tag, release, and assets.",
        ],
    }
    out = root / "release" / "current" / "session_end_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return payload


def main() -> int:
    result = run_session_end()
    print(json.dumps(result, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
