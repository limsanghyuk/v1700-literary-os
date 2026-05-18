from __future__ import annotations
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from v1700.lineage.stage83_1_consistency_audit import build_gitnexus_branchpoint_bridge_manifest

if __name__ == "__main__":
    result = build_gitnexus_branchpoint_bridge_manifest()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result.get("status") == "pass" else 1)
