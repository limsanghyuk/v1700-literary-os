from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from v1700.graph_nexus.tools.shape_check import run_graph_nexus_shape_check


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    result = run_graph_nexus_shape_check(root).to_dict()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result["status"] == "pass" else 1)
