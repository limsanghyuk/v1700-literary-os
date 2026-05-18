from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from v1700.sidecars.gitnexus.probe import probe_gitnexus


if __name__ == "__main__":
    result = probe_gitnexus().to_dict()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0)
