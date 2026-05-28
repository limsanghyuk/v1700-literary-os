from __future__ import annotations

import json
import subprocess
from pathlib import Path


PRE_COMMIT = """#!/bin/sh
set -eu
python tools/run_precommit_guard.py
"""

PRE_PUSH = """#!/bin/sh
set -eu
python tools/run_precommit_guard.py --require-release-gate
"""


def _git_dir(root: Path) -> Path:
    result = subprocess.run(
        ["git", "rev-parse", "--git-dir"],
        cwd=root,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=20,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError((result.stderr or result.stdout or "unable to resolve .git directory").strip())
    git_dir = Path(result.stdout.strip())
    return git_dir if git_dir.is_absolute() else (root / git_dir)


def install_predevelopment_hooks(root: Path | None = None) -> dict:
    root = root or Path(__file__).resolve().parents[1]
    hooks_dir = _git_dir(root) / "hooks"
    hooks_dir.mkdir(parents=True, exist_ok=True)

    pre_commit = hooks_dir / "pre-commit"
    pre_push = hooks_dir / "pre-push"
    pre_commit.write_text(PRE_COMMIT, encoding="utf-8", newline="\n")
    pre_push.write_text(PRE_PUSH, encoding="utf-8", newline="\n")
    pre_commit.chmod(0o755)
    pre_push.chmod(0o755)

    return {
        "status": "pass",
        "hooks_dir": hooks_dir.as_posix(),
        "installed": ["pre-commit", "pre-push"],
    }


def main() -> int:
    result = install_predevelopment_hooks()
    print(json.dumps(result, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
