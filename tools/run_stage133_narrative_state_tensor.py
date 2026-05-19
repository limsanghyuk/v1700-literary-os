from __future__ import annotations

import json

from v1700.narrative_state_tensor import run_stage133_narrative_state_tensor


if __name__ == "__main__":
    print(json.dumps(run_stage133_narrative_state_tensor(), ensure_ascii=False, indent=2))
