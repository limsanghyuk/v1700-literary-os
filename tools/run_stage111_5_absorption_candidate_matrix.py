from __future__ import annotations
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from v1700.stage111.absorption_candidate_matrix import build_absorption_candidate_matrix
if __name__ == '__main__':
    root = Path(__file__).resolve().parents[1]
    result = (lambda root: build_absorption_candidate_matrix())(root)
    print(json.dumps(result, ensure_ascii=True, indent=2))
    raise SystemExit(0 if result.get('status') == 'pass' else 1)
