from __future__ import annotations

import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from v1700.local_render_packet_store import run_stage162_local_render_packet_store


def main() -> int:
    payload = run_stage162_local_render_packet_store()
    print(json.dumps(payload, ensure_ascii=True, indent=2))
    return 0 if payload.get("status") == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
