from __future__ import annotations
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from v1700.page04_release_seal import run_stage166_page04_release_seal

if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    result = run_stage166_page04_release_seal(root)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result.get("status") == "pass" else 1)
