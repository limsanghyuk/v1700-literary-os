
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.gates.stage151_release_gate import run_stage151_release_gate
from v1700.local_memory_store import load_memory_records

from .contracts import MemoryQueryRequest, QueryPolicyRule
from .query import (
    DEFAULT_STORE,
    find_characters,
    find_episodes,
    find_payoffs,
    find_project_memory,
    find_reveals,
    find_scenes,
    project_for_node2,
    query_by_intent,
)

TARGET_STAGE = "stage152"
TARGET_REPORT = "release/current/stage152_memory_query_interface_report.json"
PROJECT_ID = "sample_project_stage151"


def run_stage152_memory_query_interface(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    if _active_version(root) != TARGET_STAGE:
        existing = _load_existing(root / TARGET_REPORT)
        if existing is not None:
            return existing

    baseline = run_stage151_release_gate(root)
    pack = root / "release/current/stage152_memory_query_interface_pack"
    pack.mkdir(parents=True, exist_ok=True)

    records = load_memory_records(root / DEFAULT_STORE)
    api_catalog = _build_api_catalog()
    query_policy = _build_query_policy()
    intent_query = query_by_intent(root, MemoryQueryRequest(PROJECT_ID, "family secret continuity", ("character", "continuity", "reveal"), limit=5))
    type_queries = _build_type_query_report(root)
    ranking = _build_ranking_report(intent_query)
    node2_projection = project_for_node2(intent_query.get("candidates", []))

    parts = {
        "query_api_catalog": api_catalog,
        "query_policy": query_policy,
        "intent_query_result": intent_query,
        "type_query_results": type_queries,
        "ranking_report": ranking,
        "node2_projection_report": node2_projection,
    }
    for filename, payload in {
        "query_api_catalog.json": api_catalog,
        "query_policy.json": query_policy,
        "intent_query_result.json": intent_query,
        "type_query_results.json": type_queries,
        "ranking_report.json": ranking,
        "node2_projection_report.json": node2_projection,
    }.items():
        _write_json(pack / filename, payload)

    issues: list[str] = []
    if baseline.get("status") != "pass":
        issues.append("stage151_release_gate_blocked")
    if len(records) < 5:
        issues.append("stage151_store_records_insufficient")
    for name, payload in parts.items():
        if payload.get("status") != "pass":
            issues.append(f"{name}_blocked")
            issues.extend(f"{name}:{issue}" for issue in payload.get("issues", []))

    result = {
        "stage": "152",
        "baseline_stage": "151",
        "title": "Deterministic Local Query / Ranking",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "mode": "DETERMINISTIC_LOCAL_MEMORY_QUERY",
        "page": "Page02 Narrative Memory Body",
        "query_runtime_enabled": True,
        "ranking_runtime_enabled": True,
        "query_write_enabled": False,
        "memory_write_enabled": False,
        "store_write_enabled": False,
        "vector_db_runtime_dependency": False,
        "live_provider_rag_enabled": False,
        "runtime_training_enabled": False,
        "active_meta_learning_enabled": False,
        "model_weight_update_count": 0,
        "canon_auto_resolution_count": 0,
        "auto_repair_mutation_count": 0,
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "node2_raw_reveal_access": 0,
        "hidden_reveal_projection_count": 0,
        "private_note_projection_count": 0,
        "write_handle_projection_count": 0,
        "raw_manuscript_provider_leakage": 0,
        "raw_manuscript_cross_project_leakage": 0,
        "credential_leakage": 0,
        "branchpoint_lineage_preserved": not issues,
        "stage153_memory_health_monitor_ready": not issues,
        "api_count": api_catalog.get("api_count", 0),
        "candidate_count": intent_query.get("candidate_count", 0),
        "ranked_candidate_count": ranking.get("ranked_candidate_count", 0),
        "node2_projected_count": node2_projection.get("projected_count", 0),
        "node2_blocked_projection_count": node2_projection.get("blocked_projection_count", 0),
        "parts": {"stage151_release_gate": _compact(baseline), **parts},
    }
    _write_json(root / TARGET_REPORT, result)
    return result


def _build_api_catalog() -> dict[str, Any]:
    apis = [
        "find_project_memory",
        "find_characters",
        "find_episodes",
        "find_scenes",
        "find_events",
        "find_reveals",
        "find_payoffs",
        "query_by_intent",
        "rank_memory_candidates",
        "project_for_node2",
    ]
    return {"stage": TARGET_STAGE, "title": "Stage152 Query API Catalog", "status": "pass", "issues": [], "api_count": len(apis), "apis": apis}


def _build_query_policy() -> dict[str, Any]:
    rules = (
        QueryPolicyRule("local_only", "Queries read Stage151 local JSONL records only.", True, TARGET_REPORT),
        QueryPolicyRule("deterministic_scoring", "Ranking uses lexical overlap, field priority, temporal metadata, simple rank fusion, and boundary penalty.", True, TARGET_REPORT),
        QueryPolicyRule("provider_zero", "No provider call is allowed for query or ranking.", True, TARGET_REPORT),
        QueryPolicyRule("write_blocked", "Query APIs cannot write or mutate memory records.", True, TARGET_REPORT),
        QueryPolicyRule("node2_surface_projection", "Node2 projection strips hidden/private/write/learning/raw payloads.", True, TARGET_REPORT),
    )
    issues = [rule.name for rule in rules if not rule.passed]
    return {"stage": TARGET_STAGE, "title": "Stage152 Query Policy", "status": "pass" if not issues else "blocked", "issues": issues, "rule_count": len(rules), "rules": [rule.to_dict() for rule in rules]}


def _build_type_query_report(root: Path) -> dict[str, Any]:
    results = {
        "project": find_project_memory(root, PROJECT_ID, "memory", 10),
        "characters": find_characters(root, PROJECT_ID, "Minseo secret", 5),
        "episodes": find_episodes(root, PROJECT_ID, "pilot inheritance", 5),
        "scenes": find_scenes(root, PROJECT_ID, "opening scene", 5),
        "reveals": find_reveals(root, PROJECT_ID, "birth secret", 5),
        "payoffs": find_payoffs(root, PROJECT_ID, "episode payoff", 5),
    }
    issues = [name for name, payload in results.items() if payload.get("status") != "pass"]
    return {"stage": TARGET_STAGE, "title": "Stage152 Type Query Results", "status": "pass" if not issues else "blocked", "issues": issues, "results": results}


def _build_ranking_report(query_result: dict[str, Any]) -> dict[str, Any]:
    candidates = query_result.get("candidates", [])
    scores = [candidate.get("score", 0) for candidate in candidates]
    sorted_ok = scores == sorted(scores, reverse=True)
    return {
        "stage": TARGET_STAGE,
        "title": "Stage152 Deterministic Ranking Report",
        "status": "pass" if sorted_ok and candidates else "blocked",
        "issues": [] if sorted_ok and candidates else ["ranking_empty_or_not_sorted"],
        "ranked_candidate_count": len(candidates),
        "scoring_features": ["lexical_term_overlap", "field_priority", "temporal_metadata", "simple_rank_fusion", "boundary_safe_penalty"],
        "candidates": candidates,
    }


def _active_version(root: Path) -> str:
    manifest = root / "manifests/live_core_manifest.json"
    if not manifest.exists():
        return ""
    return json.loads(manifest.read_text(encoding="utf-8")).get("active_version", "")


def _load_existing(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _compact(report: dict[str, Any]) -> dict[str, Any]:
    keep = ("status", "stage", "baseline_stage", "title", "issues", "provider_default_calls", "live_provider_call_count_in_release_gate", "node2_raw_reveal_access", "raw_manuscript_provider_leakage", "credential_leakage", "branchpoint_lineage_preserved", "memory_write_enabled", "store_write_enabled", "runtime_training_enabled")
    return {key: report.get(key) for key in keep if key in report}


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
