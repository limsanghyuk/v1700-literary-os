from __future__ import annotations
from pathlib import Path
from v1700.provider_live_sandbox.report import write_json, write_summary

def stage107_5_pack(root: Path) -> Path:
    path = root/'release/current/stage107_5_provider_live_sandbox_pack'
    path.mkdir(parents=True, exist_ok=True)
    return path
