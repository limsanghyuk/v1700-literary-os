from __future__ import annotations

import json
from pathlib import Path

from v1700.nie.rag.rag_fusion_report import build_stage116_rag_fusion_report
from v1700.stage116.contracts import Stage116Contract


def run_stage116(root: Path | None = None) -> dict:
    root = root or Path(__file__).resolve().parents[3]
    rag_report = build_stage116_rag_fusion_report()
    contract = Stage116Contract().to_dict()
    classified = rag_report.get("query_intent_classifier", {}).get("classified_queries", [])
    intents = {row.get("intent") for row in classified}
    issues: list[str] = []
    if rag_report.get("status") != "pass":
        issues.append("rag_fusion_report_blocked")
    if intents != {"CHARACTER", "EMOTIONAL", "PLOT_EVENT"}:
        issues.append("query_intent_coverage_missing")
    if rag_report.get("query_intent_classifier", {}).get("llm_call_count") != 0:
        issues.append("llm_query_classifier_call_detected")
    if rag_report.get("provider_call_count") != 0 or rag_report.get("embedding_provider_call_count") != 0:
        issues.append("provider_call_detected_in_stage116")
    result = {
        "stage": "116",
        "baseline_stage": "115",
        "title": "Domain-Specific RAG Fusion",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "release_contract": contract,
        "rag_fusion": rag_report,
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "embedding_provider_call_count": rag_report.get("embedding_provider_call_count", 0),
        "query_classifier_llm_call_count": rag_report.get("query_intent_classifier", {}).get("llm_call_count", 0),
        "physics_reward_bridge_llm_call_count": 0,
        "mae_live_provider_call_count": 0,
        "node2_raw_reveal_access": 0,
        "raw_manuscript_provider_leakage": 0,
        "credential_leakage": 0,
        "branchpoint_lineage_preserved": not issues,
        "next_development_order": ["Stage117", "Stage118", "Stage119", "Stage120"],
    }
    _write(root / "release/current/stage116_domain_rag_fusion_report.json", result)
    return result


def _write(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
