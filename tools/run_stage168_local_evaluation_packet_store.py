from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from v1700.evaluation_packet_store import run_stage168_local_evaluation_packet_store


if __name__ == "__main__":
    payload = run_stage168_local_evaluation_packet_store()
    print(json.dumps(payload, ensure_ascii=True, indent=2))
    raise SystemExit(0 if payload.get("status") == "pass" else 1)

