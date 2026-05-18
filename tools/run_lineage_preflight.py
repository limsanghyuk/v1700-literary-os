from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from v1700.gates.lineage_preflight_gate import run_lineage_preflight_gate


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--goal", default="Stage72.1 GraphNexus restoration")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    result = run_lineage_preflight_gate(root, goal=args.goal)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result["status"] == "pass" else 1)
