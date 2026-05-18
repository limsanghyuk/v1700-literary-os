from pathlib import Path
import json, sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from v1700.gates.literary_formula_survival_gate import run_literary_formula_survival_gate

if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    report = run_literary_formula_survival_gate(root)
    print(json.dumps(report, ensure_ascii=False, indent=2))
