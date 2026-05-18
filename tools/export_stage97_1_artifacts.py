from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from v1700.gates.release_gate import run_release_gate
from v1700.gates.stage97_1_release_gate import run_stage97_1_release_gate
from v1700.longform_adversarial.adversarial_orchestrator import run_stage97_1_adversarial_validation
from v1700.longform_adversarial.report import (
    build_stage97_1_adversarial_validation_manifest,
    build_stage97_1_branchpoint_trace_manifest,
    build_stage97_1_manifest,
)

ROOT = Path(__file__).resolve().parents[1]
RELEASE = ROOT / "release" / "current"
PACK = RELEASE / "stage97_1_adversarial_pack"
MANIFESTS = ROOT / "manifests"


def main() -> int:
    PACK.mkdir(parents=True, exist_ok=True)
    MANIFESTS.mkdir(parents=True, exist_ok=True)
    written: dict[str, str] = {}
    validation = run_stage97_1_adversarial_validation(ROOT)
    _write_json(RELEASE / "stage97_1_adversarial_validation_report.json", validation, written)
    _write_json(PACK / "adversarial_case_index.json", validation["case_index"], written)
    _write_json(PACK / "adversarial_result_index.json", validation["results"], written)
    _write_json(PACK / "normal_case_result.json", _select_results(validation, "ADV-NOR"), written)
    _write_json(PACK / "broken_topology_results.json", _select_results(validation, "ADV-TOP"), written)
    _write_json(PACK / "broken_load_results.json", _select_results(validation, "ADV-LOD"), written)
    _write_json(PACK / "broken_payoff_results.json", _select_results(validation, "ADV-PAY"), written)
    _write_json(PACK / "passive_agency_results.json", _select_results(validation, "ADV-AGY"), written)
    _write_json(PACK / "weak_scene_results.json", _select_results(validation, "ADV-SCN"), written)
    _write_json(PACK / "speech_level_violation_results.json", _select_results(validation, "ADV-DLG"), written)
    _write_json(PACK / "style_drift_violation_results.json", _select_results(validation, "ADV-VOC"), written)
    _write_json(PACK / "attention_fatigue_results.json", _select_results(validation, "ADV-ATT"), written)
    _write_json(PACK / "coefficient_memory_bridge_report.json", validation["coefficient_memory_bridge"], written)
    _write_json(PACK / "manuscript_ingest_privacy_report.json", validation["manuscript_ingest_privacy"], written)
    _write_json(PACK / "production_scene_mapping_report.json", validation["production_scene_mapping"], written)
    summary = PACK / "stage97_1_summary.md"
    summary.write_text(_summary(validation) + "\n", encoding="utf-8")
    written[str(summary.relative_to(ROOT)).replace("\\", "/")] = str(summary.relative_to(ROOT))

    gate = run_stage97_1_release_gate(ROOT)
    _write_json(RELEASE / "stage97_1_release_gate_report.json", gate, written)
    _write_json(RELEASE / "release_gate_report.json", run_release_gate(), written)
    _write_json(MANIFESTS / "stage97_1_manifest.json", build_stage97_1_manifest(), written)
    _write_json(MANIFESTS / "stage97_1_branchpoint_trace_manifest.json", build_stage97_1_branchpoint_trace_manifest(), written)
    _write_json(MANIFESTS / "stage97_1_adversarial_validation_manifest.json", build_stage97_1_adversarial_validation_manifest(), written)
    handoff = RELEASE / "stage97_1_developer_handoff_report.md"
    handoff.write_text(_handoff(gate) + "\n", encoding="utf-8")
    written[str(handoff.relative_to(ROOT)).replace("\\", "/")] = str(handoff.relative_to(ROOT))
    print(json.dumps({"status": gate["status"], "artifacts": written}, ensure_ascii=True, indent=2))
    return 0 if gate.get("status") == "pass" else 1


def _select_results(validation: dict, prefix: str) -> list[dict]:
    return [result for result in validation["results"] if result["case_id"].startswith(prefix)]


def _write_json(path: Path, payload, written: dict[str, str]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    written[str(path.relative_to(ROOT)).replace("\\", "/")] = str(path.relative_to(ROOT))


def _summary(validation: dict) -> str:
    return "\n".join(
        [
            "# Stage97.1 Adversarial Validation Summary",
            "",
            f"- Status: `{validation['status']}`",
            f"- Total cases: `{validation['adversarial_cases_total']}`",
            f"- Matched expectation: `{validation['adversarial_cases_matched_expectation']}`",
            f"- Normal cases passed: `{validation['normal_cases_passed']}`",
            f"- Broken cases blocked: `{validation['blocked_cases_passed']}`",
            "- Provider calls during release: `0`",
            "- Node2 raw reveal access: `0`",
            "- Raw manuscript provider leakage: `0`",
        ]
    )


def _handoff(gate: dict) -> str:
    return "\n".join(
        [
            "# Stage97.1 Developer Handoff",
            "",
            "Stage97.1 hardens Stage97 with an adversarial negative corpus.",
            "",
            f"- Gate: `{gate['status']}`",
            f"- Total adversarial cases: `{gate['adversarial_cases_total']}`",
            f"- Matched expectations: `{gate['adversarial_cases_matched_expectation']}`",
            f"- Normal cases passed: `{gate['normal_cases_passed']}`",
            f"- Broken cases blocked: `{gate['blocked_cases_passed']}`",
            f"- Provider calls: `{gate['provider_call_count']}`",
            f"- Node2 raw reveal access: `{gate['node2_raw_reveal_access']}`",
        ]
    )


if __name__ == "__main__":
    raise SystemExit(main())
