from __future__ import annotations

import json

from v1700.gates.stage133_release_gate import run_stage133_release_gate


if __name__ == "__main__":
    print(json.dumps(run_stage133_release_gate(), ensure_ascii=False, indent=2))
