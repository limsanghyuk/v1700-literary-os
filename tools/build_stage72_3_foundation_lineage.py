from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from v1700.graph_nexus.tools.foundation_lineage import write_foundation_lineage_artifacts


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    result = write_foundation_lineage_artifacts(root)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result["status"] == "pass" else 1)
