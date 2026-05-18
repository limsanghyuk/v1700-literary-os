#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from v1700.narrative_weight_kernel import write_narrative_weight_kernel_report


if __name__ == "__main__":
    report = write_narrative_weight_kernel_report()
    print(json.dumps({"status": report["status"], "stage": report["stage"]}, ensure_ascii=False, sort_keys=True))
