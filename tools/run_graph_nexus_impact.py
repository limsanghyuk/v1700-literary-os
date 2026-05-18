from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from v1700.graph_nexus.tools.contracts import GraphNexusImpactRequest
from v1700.graph_nexus.tools.impact import run_graph_nexus_impact


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", default="ALL")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    result = run_graph_nexus_impact(root, GraphNexusImpactRequest(target=args.target))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result["status"] == "pass" else 1)
