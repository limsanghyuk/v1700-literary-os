
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from v1700.local_memory_store import load_memory_records
from v1700.local_memory_store.loader import node2_projection_for

from .contracts import MemoryQueryCandidate, MemoryQueryRequest

DEFAULT_STORE = "samples/stage151_memory_store/project_memory_records.jsonl"
FIELD_PRIORITY = {
    "character": 1.35,
    "episode": 1.25,
    "scene": 1.15,
    "event": 1.15,
    "reveal": 1.05,
    "payoff": 1.05,
    "continuity": 1.1,
    "world": 1.0,
}
NODE2_BLOCKED = {"PLANNER_PRIVATE", "HIDDEN_REVEAL", "PRIVATE_NOTE", "WRITE_HANDLE"}
FORBIDDEN_NODE2_KEYS = {
    "hidden_reveal_payload",
    "private_note",
    "write_handle",
    "canon_mutation_command",
    "learning_payload",
    "raw_manuscript_payload",
}


def tokenize(text: str) -> set[str]:
    return {token.lower() for token in re.findall(r"[A-Za-z0-9가-힣:_-]+", text)}


def _load(root: Path, store_path: str = DEFAULT_STORE) -> list[dict[str, Any]]:
    return load_memory_records(root / store_path)


def _score_record(record: dict[str, Any], query_terms: set[str]) -> float:
    haystack = " ".join(str(record.get(key, "")) for key in ("record_id", "record_type", "source_state_id", "summary", "visibility", "boundary_level"))
    terms = tokenize(haystack)
    overlap = len(query_terms & terms)
    if not query_terms:
        overlap = 1
    lexical = overlap / max(1, len(query_terms))
    field = FIELD_PRIORITY.get(str(record.get("record_type", "")), 1.0)
    stage_bonus = 0.1 if str(record.get("source_stage", "")).startswith("stage") else 0.0
    boundary_penalty = 0.25 if str(record.get("boundary_level", "")) in NODE2_BLOCKED else 0.0
    score = (lexical * 10.0 * field) + stage_bonus - boundary_penalty
    return round(max(score, 0.0), 6)


def _candidate(record: dict[str, Any], score: float, rank: int) -> MemoryQueryCandidate:
    return MemoryQueryCandidate(
        record_id=str(record["record_id"]),
        record_type=str(record["record_type"]),
        project_id=str(record["project_id"]),
        source_state_id=str(record["source_state_id"]),
        boundary_level=str(record["boundary_level"]),
        summary=str(record.get("summary", "")),
        score=score,
        rank=rank,
        node2_projection=node2_projection_for(record),
        checksum=str(record["checksum"]),
    )


def rank_memory_candidates(records: list[dict[str, Any]], request: MemoryQueryRequest) -> list[dict[str, Any]]:
    query_terms = tokenize(request.query)
    filtered = [
        record for record in records
        if record.get("project_id") == request.project_id
        and (not request.record_types or str(record.get("record_type")) in request.record_types)
    ]
    scored = [(_score_record(record, query_terms), record) for record in filtered]
    scored.sort(key=lambda item: (-item[0], str(item[1].get("record_id", ""))))
    candidates = [_candidate(record, score, rank + 1).to_dict() for rank, (score, record) in enumerate(scored[: request.limit])]
    return candidates


def query_by_intent(root: Path, request: MemoryQueryRequest, store_path: str = DEFAULT_STORE) -> dict[str, Any]:
    records = _load(root, store_path)
    candidates = rank_memory_candidates(records, request)
    return {
        "status": "pass",
        "request": request.to_dict(),
        "candidate_count": len(candidates),
        "candidates": candidates,
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
    }


def find_project_memory(root: Path, project_id: str, query: str = "", limit: int = 10) -> dict[str, Any]:
    return query_by_intent(root, MemoryQueryRequest(project_id=project_id, query=query, record_types=(), limit=limit))


def _find_type(root: Path, project_id: str, record_type: str, query: str = "", limit: int = 10) -> dict[str, Any]:
    return query_by_intent(root, MemoryQueryRequest(project_id=project_id, query=query, record_types=(record_type,), limit=limit))


def find_characters(root: Path, project_id: str, query: str = "", limit: int = 10) -> dict[str, Any]:
    return _find_type(root, project_id, "character", query, limit)


def find_episodes(root: Path, project_id: str, query: str = "", limit: int = 10) -> dict[str, Any]:
    return _find_type(root, project_id, "episode", query, limit)


def find_scenes(root: Path, project_id: str, query: str = "", limit: int = 10) -> dict[str, Any]:
    return _find_type(root, project_id, "scene", query, limit)


def find_events(root: Path, project_id: str, query: str = "", limit: int = 10) -> dict[str, Any]:
    return _find_type(root, project_id, "event", query, limit)


def find_reveals(root: Path, project_id: str, query: str = "", limit: int = 10) -> dict[str, Any]:
    return _find_type(root, project_id, "reveal", query, limit)


def find_payoffs(root: Path, project_id: str, query: str = "", limit: int = 10) -> dict[str, Any]:
    return _find_type(root, project_id, "payoff", query, limit)


def project_for_node2(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    projected: list[dict[str, Any]] = []
    leaks: list[str] = []
    for candidate in candidates:
        safe = {
            "record_id": candidate["record_id"],
            "record_type": candidate["record_type"],
            "source_state_id": candidate["source_state_id"],
            "summary": candidate["summary"] if candidate.get("node2_projection") == "surface_safe" else "BLOCKED_BY_NODE2_BOUNDARY",
            "node2_projection": candidate.get("node2_projection", "blocked"),
            "rank": candidate["rank"],
            "score": candidate["score"],
        }
        if any(key in safe for key in FORBIDDEN_NODE2_KEYS):
            leaks.append(str(candidate.get("record_id")))
        projected.append(safe)
    return {
        "status": "pass" if not leaks else "blocked",
        "issues": leaks,
        "projected_count": len(projected),
        "blocked_projection_count": sum(1 for entry in projected if entry["node2_projection"] != "surface_safe"),
        "entries": projected,
        "node2_raw_reveal_access": 0,
    }
