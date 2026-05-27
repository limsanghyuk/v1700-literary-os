from __future__ import annotations

from pathlib import Path

from v1700.release_policy_registry import run_stage174_release_policy_registry

def run(root: Path | None = None) -> dict:
    return run_stage174_release_policy_registry(root)
