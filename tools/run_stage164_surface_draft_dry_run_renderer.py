from __future__ import annotations
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from v1700.surface_draft_dry_run_renderer import run_stage164_surface_draft_dry_run_renderer

if __name__ == "__main__":
    payload = run_stage164_surface_draft_dry_run_renderer()
    print(json.dumps(payload, ensure_ascii=True, indent=2))
    raise SystemExit(0 if payload["status"] == "pass" else 1)
