from pathlib import Path
import json, sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from v1700.gates.stage73_1_release_gate import run_stage73_1_release_gate

if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    report = run_stage73_1_release_gate(root)
    out = root / "release" / "current" / "stage73_1_literary_formula_restoration_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
