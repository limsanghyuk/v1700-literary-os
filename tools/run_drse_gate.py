from pathlib import Path
import json, sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from v1700.gates.drse_quality_gate import run_drse_quality_gate

if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    report = run_drse_quality_gate(root)
    print(json.dumps(report, ensure_ascii=False, indent=2))
