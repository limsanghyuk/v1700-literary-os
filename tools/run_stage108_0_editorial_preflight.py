from __future__ import annotations
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from v1700.stage108.orchestrator import run_stage108
if __name__ == '__main__':
    result = run_stage108(Path(__file__).resolve().parents[1]).get('stage108_0_preflight', {})
    print(json.dumps(result, ensure_ascii=True, indent=2))
    raise SystemExit(0 if result.get('status') == 'pass' else 1)
