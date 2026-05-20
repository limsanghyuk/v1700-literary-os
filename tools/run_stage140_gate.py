from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from v1700.gates.stage140_release_gate import run_stage140_release_gate


if __name__ == "__main__":
    print(json.dumps(run_stage140_release_gate(ROOT), ensure_ascii=False, indent=2))
