from __future__ import annotations

import json
from pathlib import Path

from v1700.gig_advisory import run_stage131_gig_advisory


if __name__ == "__main__":
    print(json.dumps(run_stage131_gig_advisory(Path(__file__).resolve().parents[1]), ensure_ascii=False, indent=2))
