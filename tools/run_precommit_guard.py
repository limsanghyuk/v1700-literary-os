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


BLOCK_PATTERNS = {
    "dev_mode_true": "DEV_MODE=True",
    "provider_default_nonzero": "provider_default_calls = 1",
    "live_provider_nonzero": "live_provider_call_count_in_release_gate = 1",
    "raw_manuscript_leakage_nonzero": "raw_manuscript_provider_leakage = 1",
    "credential_leakage_nonzero": "credential_leakage = 1",
}


def _run(root: Path, args: list[str]) -> tuple[int, str]:
    result = subprocess.run(
        args,
        cwd=root,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=120,
        check=False,
    )
    output = ((result.stdout or "") + (result.stderr or "")).strip()
    return result.returncode, output


def _staged_files(root: Path) -> list[str]:
    code, output = _run(root, ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"])
    if code != 0 or not output:
        return []
    return [line.strip() for line in output.splitlines() if line.strip()]


def _staged_diff(root: Path) -> str:
    code, output = _run(root, ["git", "diff", "--cached", "--unified=0"])
    return output if code == 0 else ""


def run_precommit_guard(root: Path | None = None, require_release_gate: bool = False) -> dict:
    root = root or Path(__file__).resolve().parents[1]
    mandatory = run_mandatory_predevelopment_check(root, write_report=False)
    staged_files = _staged_files(root)
    staged_diff = _staged_diff(root)
    staged_python = [name for name in staged_files if name.endswith(".py")]
    issues = []

    if mandatory.get("status") != "pass":
        issues.append("mandatory_predevelopment_check_failed")

    for name, marker in BLOCK_PATTERNS.items():
        if f"+{marker}" in staged_diff or f"+ {marker}" in staged_diff:
            issues.append(name)

    release_gate = {"status": "skipped"}
    if require_release_gate or len(staged_python) >= 5:
        code, output = _run(root, ["python", "tools/run_release_gate.py"])
        release_gate = {"status": "pass" if code == 0 else "blocked", "output_excerpt": output[:1000]}
        if code != 0:
            issues.append("release_gate_failed")

    return {
        "stage": "precommit_guard",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "staged_files": staged_files,
        "staged_python_count": len(staged_python),
        "mandatory_predevelopment": {"status": mandatory.get("status"), "issues": mandatory.get("issues", [])},
        "release_gate": release_gate,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--require-release-gate", action="store_true")
    args = parser.parse_args()
    result = run_precommit_guard(require_release_gate=args.require_release_gate)
    print(json.dumps(result, ensure_ascii=True, indent=2))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
