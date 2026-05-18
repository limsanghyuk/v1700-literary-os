from __future__ import annotations
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from v1700.writer_studio.event_replay import run_stage91_event_replay_smoke

if __name__ == "__main__":
    result = run_stage91_event_replay_smoke()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result["status"] == "pass" else 1)
