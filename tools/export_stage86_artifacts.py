from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from v1700.traceability.stage86_exports import export_stage86_artifacts


if __name__ == "__main__":
    result = export_stage86_artifacts()
    print(json.dumps(result, ensure_ascii=True, indent=2))
