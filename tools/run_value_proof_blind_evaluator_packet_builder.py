from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from v1700.value_proof_blind_evaluator_packet_builder import run_value_proof_blind_evaluator_packet_builder


def main() -> None:
    result = run_value_proof_blind_evaluator_packet_builder(repo_root=ROOT)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
