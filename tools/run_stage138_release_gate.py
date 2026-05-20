from __future__ import annotations

import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from v1700.gates.stage138_release_gate import run_stage138_release_gate


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    print(json.dumps(run_stage138_release_gate(root), ensure_ascii=False, indent=2))
