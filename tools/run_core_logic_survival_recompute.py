from __future__ import annotations
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from v1700.lineage.reabsorption_reconciliation import build_reconciled_core_logic_survival_matrix

if __name__ == "__main__":
    result = {"stage": "81.1", "recomputed_matrix": [entry.to_dict() for entry in build_reconciled_core_logic_survival_matrix()]}
    print(json.dumps(result, ensure_ascii=False, indent=2))
