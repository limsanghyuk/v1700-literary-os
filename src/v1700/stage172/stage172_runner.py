from __future__ import annotations

from pathlib import Path
from typing import Any

from v1700.page05_release_seal import run_stage172_page05_release_seal


def run_stage172(root: Path | None = None) -> dict[str, Any]:
    return run_stage172_page05_release_seal(root)
