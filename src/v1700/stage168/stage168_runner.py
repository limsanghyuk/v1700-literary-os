from __future__ import annotations

from pathlib import Path
from typing import Any

from v1700.evaluation_packet_store import run_stage168_local_evaluation_packet_store


def run_stage168(root: Path | None = None) -> dict[str, Any]:
    return run_stage168_local_evaluation_packet_store(root)

