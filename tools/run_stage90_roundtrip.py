from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from v1700.writer_studio.roundtrip import run_stage90_roundtrip_smoke


if __name__ == "__main__":
    print(json.dumps(run_stage90_roundtrip_smoke(), ensure_ascii=False, indent=2))
