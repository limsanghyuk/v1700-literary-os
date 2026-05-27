from __future__ import annotations

from pathlib import Path

from v1700.page06_release_seal import run_stage178_page06_release_seal

def run(root: Path | None = None) -> dict:
    return run_stage178_page06_release_seal(root)
