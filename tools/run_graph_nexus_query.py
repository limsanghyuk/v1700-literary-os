from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from v1700.graph_nexus.tools.contracts import GraphNexusQueryRequest
from v1700.graph_nexus.tools.query import run_graph_nexus_query


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("query", nargs="?", default="GraphNexus")
    parser.add_argument("--context", default="")
    parser.add_argument("--goal", default="")
    parser.add_argument("--limit", type=int, default=5)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    result = run_graph_nexus_query(
        root,
        GraphNexusQueryRequest(
            query=args.query,
            context=args.context,
            goal=args.goal,
            limit=args.limit,
        ),
    ).to_dict()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result["status"] == "pass" else 1)
