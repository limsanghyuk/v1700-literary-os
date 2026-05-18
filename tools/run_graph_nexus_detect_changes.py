from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from v1700.graph_nexus.tools.detect_changes import run_graph_nexus_detect_changes


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    result = run_graph_nexus_detect_changes(root).to_dict()
    out = root / "release" / "current" / "stage72_2_graph_nexus_detect_changes_report.json"
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result["status"] == "pass" else 1)
