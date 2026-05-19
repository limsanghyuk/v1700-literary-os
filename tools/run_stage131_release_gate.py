from __future__ import annotations

import json
from pathlib import Path

from v1700.gates.stage131_release_gate import run_stage131_release_gate


if __name__ == "__main__":
    print(json.dumps(run_stage131_release_gate(Path(__file__).resolve().parents[1]), ensure_ascii=False, indent=2))
