from __future__ import annotations

from v1700.stage114.orchestrator import run_stage114


def run_smoke() -> dict:
    result = run_stage114()
    return {"status": result.get("status"), "stage": "114", "issues": result.get("issues", [])}
