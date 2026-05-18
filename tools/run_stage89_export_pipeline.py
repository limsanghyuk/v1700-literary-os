from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from v1700.writer_studio.export_pipeline import run_stage89_export_pipeline_smoke

if __name__ == "__main__":
    result = run_stage89_export_pipeline_smoke()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result["status"] == "pass" else 1)
