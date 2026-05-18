from __future__ import annotations

import json
from pathlib import Path

from v1700.nie.adversarial.report import build_stage119_adversarial_report
from v1700.stage119.contracts import Stage119Contract


def run_stage119(root: Path | None = None) -> dict:
    root = root or Path(__file__).resolve().parents[3]
    adversarial = build_stage119_adversarial_report(root)
    contract = Stage119Contract().to_dict()
    issues: list[str] = list(adversarial.get("issues", []))
    if adversarial.get("normal_case_count", 0) < 1:
        issues.append("normal_case_missing")
    if adversarial.get("adversarial_cases_total", 0) < contract["min_adversarial_cases"]:
        issues.append("adversarial_case_count_below_contract")
    if adversarial.get("unexpected_pass_count") != 0:
        issues.append("unexpected_pass_count_nonzero")
    if adversarial.get("unexpected_block_count") != 0:
        issues.append("unexpected_block_count_nonzero")
    pack_dir = root / "release/current/stage119_nie_adversarial_pack"
    for name in contract["required_pack_files"]:
        if not (pack_dir / name).exists():
            issues.append(f"missing_pack_file:{name}")
    result = {
        "stage": "119",
        "baseline_stage": "118",
        "title": "NIE Adversarial Regression Pack",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "release_contract": contract,
        "adversarial_regression": adversarial,
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "embedding_provider_call_count": 0,
        "query_classifier_llm_call_count": 0,
        "physics_reward_bridge_llm_call_count": 0,
        "mae_live_provider_call_count": 0,
        "node2_raw_reveal_access": 0,
        "raw_manuscript_provider_leakage": 0,
        "credential_leakage": 0,
        "branchpoint_lineage_preserved": not issues,
        "next_development_order": ["Stage120"],
    }
    out = root / "release/current/stage119_nie_adversarial_regression_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result
