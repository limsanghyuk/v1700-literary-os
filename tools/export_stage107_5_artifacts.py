from __future__ import annotations
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from v1700.gates.stage107_5_sandbox_gate import run_stage107_5_sandbox_gate

def main() -> int:
    root = Path(__file__).resolve().parents[1]
    gate = run_stage107_5_sandbox_gate(root)
    package = "V1700_stage107_5_provider_live_sandbox_adapter_verification_FIXED.zip"
    payload = {
        "stage": "107.5",
        "status": gate.get("status"),
        "canonical_package": package,
        "sha256_sidecar": package + ".sha256",
        "filelist": "V1700_stage107_5_FIXED_filelist.txt",
        "sandbox_results_included": "contract_reports_only",
        "raw_outputs_included": False,
        "credentials_included": False,
    }
    out = root / "release/current/stage107_5_artifact_export_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=True, indent=2))
    return 0 if payload["status"] == "pass" else 1

if __name__ == "__main__":
    raise SystemExit(main())
