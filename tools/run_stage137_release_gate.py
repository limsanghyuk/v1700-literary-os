from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from v1700.gates.stage137_release_gate import run_stage137_release_gate


if __name__ == "__main__":
    print(json.dumps(run_stage137_release_gate(), ensure_ascii=False, indent=2))
