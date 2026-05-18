from __future__ import annotations
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from v1700.stage107_5.provider_sandbox_orchestrator import run_stage107_5_2_adapter_contract
if __name__ == '__main__':
    result = run_stage107_5_2_adapter_contract(Path(__file__).resolve().parents[1])
    print(json.dumps(result, ensure_ascii=True, indent=2))
    raise SystemExit(0 if result.get('status') == 'pass' else 1)
