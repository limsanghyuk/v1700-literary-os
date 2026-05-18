from pathlib import Path
import json, sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from v1700.gates.stage74_release_gate import run_stage74_release_gate

if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    report = run_stage74_release_gate(root)
    out = root / "release" / "current" / "stage74_release_gate_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
