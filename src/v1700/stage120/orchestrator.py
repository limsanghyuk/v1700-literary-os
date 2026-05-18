from __future__ import annotations

import json
from pathlib import Path

from v1700.nie.gate25.gate25_nie_v1 import build_gate25_nie_v1_report
from v1700.stage120.contracts import Stage120Contract


def run_stage120(root: Path | None = None) -> dict:
    root = root or Path(__file__).resolve().parents[3]
    contract = Stage120Contract().to_dict()
    gate25 = build_gate25_nie_v1_report(root)
    issues: list[str] = list(gate25.get("issues", []))
    pack_dir = root / "release/current/stage120_nie_v1_release_pack"
    for name in ("gate25_nie_v1_report.json", "stage120_nie_v1_summary.md", "stage120_component_matrix.json"):
        if not (pack_dir / name).exists():
            issues.append(f"missing_stage120_pack_file:{name}")
    result = {
        "stage": "120",
        "baseline_stage": "119",
        "title": "Gate25 NIE v1.0 Release",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "release_contract": contract,
        "gate25_nie_v1": gate25,
        "provider_default_calls": gate25.get("provider_default_calls", 0),
        "live_provider_call_count_in_release_gate": gate25.get("live_provider_call_count_in_release_gate", 0),
        "embedding_provider_call_count": gate25.get("embedding_provider_call_count", 0),
        "query_classifier_llm_call_count": gate25.get("query_classifier_llm_call_count", 0),
        "physics_reward_bridge_llm_call_count": gate25.get("physics_reward_bridge_llm_call_count", 0),
        "mae_live_provider_call_count": gate25.get("mae_live_provider_call_count", 0),
        "node2_raw_reveal_access": gate25.get("node2_raw_reveal_access", 0),
        "raw_manuscript_provider_leakage": gate25.get("raw_manuscript_provider_leakage", 0),
        "credential_leakage": gate25.get("credential_leakage", 0),
        "branchpoint_lineage_preserved": not issues,
        "next_development_order": ["post-120 NIE hardening or Stage121 if required"],
    }
    out = root / "release/current/stage120_gate25_nie_v1_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result
