from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from v1700.corpus_formula_bridge import run_local_corpus_formula_bridge


if __name__ == "__main__":
    print(json.dumps(run_local_corpus_formula_bridge(ROOT), ensure_ascii=False, indent=2))
