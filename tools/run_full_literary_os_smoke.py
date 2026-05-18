from pathlib import Path
import json, sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from v1700.integration import run_full_literary_os_smoke

if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    report = run_full_literary_os_smoke()
    out = root / "release" / "current" / "stage79_full_literary_os_smoke_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
