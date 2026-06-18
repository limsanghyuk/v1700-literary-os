from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from v1700.value_proof_arm_b_guidance_surface import run_value_proof_arm_b_guidance_surface
from v1700.value_proof_arm_b_preregistration_packet_builder import run_value_proof_arm_b_preregistration_packet_builder
from v1700.value_proof_blind_evaluator_packet_builder import run_value_proof_blind_evaluator_packet_builder


def _load(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _report_status(report: dict[str, Any] | None) -> str:
    return "present" if isinstance(report, dict) and report.get("status") == "pass" else "missing"


def main() -> None:
    guidance = _load(ROOT / "release/current/value_proof_arm_b_guidance_pack/value_proof_arm_b_guidance_surface_report.json")
    if guidance is None:
        guidance = run_value_proof_arm_b_guidance_surface(repo_root=ROOT)

    prereg = _load(ROOT / "release/current/value_proof_arm_b_preregistration_pack/value_proof_arm_b_preregistration_packet_report.json")
    if prereg is None:
        prereg = run_value_proof_arm_b_preregistration_packet_builder(repo_root=ROOT, guidance_surface_report=guidance)

    blind = _load(ROOT / "release/current/value_proof_blind_evaluator_pack/value_proof_blind_evaluator_packet_report.json")
    if blind is None:
        blind = run_value_proof_blind_evaluator_packet_builder(repo_root=ROOT, preregistration_report=prereg)

    checks = {
        "stage242_baseline": "present",
        "value_proof_guidance_report": _report_status(guidance),
        "value_proof_preregistration_report": _report_status(prereg),
        "value_proof_blind_evaluator_report": _report_status(blind),
        "provider_default_calls": 0,
        "runtime_training_enabled": False,
        "canonical_mutation_allowed": False,
        "page18_runtime_opened": False,
        "stage243_created": False,
    }

    issues = [f"{name}_missing" for name, value in checks.items() if name.endswith("_report") and value != "present"]
    status = "pass" if not issues else "blocked"
    decision = "ready_for_policy_review" if not issues else "not_ready"

    result = {
        "title": "Page18 Readiness Precheck",
        "created": str(date.today()),
        "branch": "corpus-absorption-formula-bridge-handoff",
        "baseline": "stage242",
        "status": status,
        "decision": decision,
        "checks": checks,
        "issues": issues,
        "next_required_action": (
            "policy review and warning decision before any Page18 opening"
            if not issues
            else "run local Value Proof chain and commit generated reports"
        ),
        "paths": {
            "value_proof_guidance_report": "release/current/value_proof_arm_b_guidance_pack/value_proof_arm_b_guidance_surface_report.json",
            "value_proof_preregistration_report": "release/current/value_proof_arm_b_preregistration_pack/value_proof_arm_b_preregistration_packet_report.json",
            "value_proof_blind_evaluator_report": "release/current/value_proof_blind_evaluator_pack/value_proof_blind_evaluator_packet_report.json",
        },
    }

    out = ROOT / "release/current/page18_readiness_precheck_report.json"
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
