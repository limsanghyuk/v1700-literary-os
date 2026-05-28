from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.run_mandatory_predevelopment_check import run_mandatory_predevelopment_check


def _run_git(root: Path, args: list[str]) -> tuple[int, str]:
    result = subprocess.run(
        ["git", *args],
        cwd=root,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=60,
        check=False,
    )
    output = ((result.stdout or "") + (result.stderr or "")).strip()
    return result.returncode, output


def _git_value(root: Path, args: list[str], fallback: str = "") -> str:
    code, output = _run_git(root, args)
    return output.splitlines()[0].strip() if code == 0 and output else fallback


def _latest_session_note(root: Path) -> str:
    sessions_dir = root / "docs" / "sessions"
    if not sessions_dir.exists():
        return ""
    files = sorted(
        sessions_dir.glob("*.md"),
        key=lambda item: (item.stat().st_mtime, item.name),
        reverse=True,
    )
    return files[0].relative_to(root).as_posix() if files else ""


def run_session_start(root: Path | None = None, fetch_remote: bool = True, write_report: bool = True) -> dict:
    root = root or Path(__file__).resolve().parents[1]
    fetch = {"status": "skipped", "command": "git fetch origin --tags --prune"}
    if fetch_remote:
        code, output = _run_git(root, ["fetch", "origin", "--tags", "--prune"])
        fetch = {
            "status": "pass" if code == 0 else "blocked",
            "command": "git fetch origin --tags --prune",
            "output_excerpt": output[:1000],
        }

    branch = _git_value(root, ["rev-parse", "--abbrev-ref", "HEAD"], "DETACHED_HEAD")
    head = _git_value(root, ["rev-parse", "HEAD"])
    origin_main = _git_value(root, ["rev-parse", "origin/main"])
    latest_tag = _git_value(root, ["describe", "--tags", "--abbrev=0", "--match", "v1700-stage*"])
    status_short = _git_value(root, ["status", "--short", "--branch"])
    latest_session_note = _latest_session_note(root)
    mandatory = run_mandatory_predevelopment_check(root, write_report=write_report)

    issues: list[str] = []
    if fetch["status"] == "blocked":
        issues.append("remote_fetch_failed")
    if not head:
        issues.append("head_missing")
    if not origin_main:
        issues.append("origin_main_missing")
    if not latest_tag:
        issues.append("latest_stage_tag_missing")
    if not latest_session_note:
        issues.append("latest_session_note_missing")
    if mandatory.get("status") != "pass":
        issues.append("mandatory_predevelopment_check_failed")

    payload = {
        "stage": "session_start",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "fetch": fetch,
        "branch": branch,
        "head": head,
        "origin_main": origin_main,
        "latest_stage_tag": latest_tag,
        "latest_session_note": latest_session_note,
        "git_status": status_short,
        "mandatory_predevelopment": {
            "status": mandatory.get("status"),
            "issues": mandatory.get("issues", []),
        },
        "required_next_steps": [
            "Read the target proposal and blueprint.",
            "Confirm stage-specific gate coverage before implementation.",
            "Refresh GitNexus if the index is stale or missing.",
        ],
    }
    if write_report:
        out = root / "release" / "current" / "session_start_report.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-fetch", action="store_true", help="Use current local refs without fetching origin.")
    args = parser.parse_args()
    result = run_session_start(fetch_remote=not args.no_fetch)
    print(json.dumps(result, ensure_ascii=True, indent=2))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
