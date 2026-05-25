from __future__ import annotations

from pathlib import Path
from typing import Any

from v1700.surface_draft_dry_run_renderer import run_stage164_surface_draft_dry_run_renderer


def run_stage164(root: Path | None = None) -> dict[str, Any]:
    return run_stage164_surface_draft_dry_run_renderer(root)
