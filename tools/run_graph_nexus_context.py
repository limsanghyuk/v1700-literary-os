from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from v1700.graph_nexus.tools.context import build_graph_nexus_context
from v1700.graph_nexus.tools.contracts import GraphNexusContextRequest


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", default="Node2ProseCompiler")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    result = build_graph_nexus_context(root, GraphNexusContextRequest(target=args.target))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result["status"] == "pass" else 1)
