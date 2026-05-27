from __future__ import annotations
import json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/"src"
if str(SRC) not in sys.path: sys.path.insert(0, str(SRC))
from v1700.gates.stage183_release_gate import run_stage183_release_gate
if __name__=="__main__":
    result=run_stage183_release_gate(ROOT)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    sys.exit(0 if result.get("status")=="pass" else 1)
