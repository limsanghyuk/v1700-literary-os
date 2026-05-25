from __future__ import annotations

from pathlib import Path
from typing import Any

from v1700.rendering_body_contract import run_stage161_rendering_contract


def run_stage161(root: Path | None = None) -> dict[str, Any]:
    return run_stage161_rendering_contract(root)
