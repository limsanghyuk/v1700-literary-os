from __future__ import annotations
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from v1700.runtime_absorption.v370_absorption import export_stage84_manifests

if __name__ == "__main__":
    result = export_stage84_manifests()
    print(json.dumps({"status": "pass", "written": result}, ensure_ascii=False, indent=2))
