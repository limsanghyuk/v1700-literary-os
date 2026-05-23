from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.local_memory_store import run_stage151_local_read_only_memory_store


def run_stage151(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    report = run_stage151_local_read_only_memory_store(root)
    summary = {
        "stage": "151",
        "baseline_stage": "150",
        "title": "Local Read-Only Memory Store",
        "status": report["status"],
        "main_report": "release/current/stage151_local_read_only_memory_store_report.json",
        "release_gate_report": "release/current/stage151_release_gate_report.json",
        "asset_manifest": "release/current/stage151_release_asset_manifest.json",
        "evidence_pack": "release/current/stage151_local_read_only_memory_store_pack/",
        "mode": report.get("mode"),
        "read_only_store_enabled": report.get("read_only_store_enabled"),
        "store_write_enabled": report.get("store_write_enabled"),
        "record_count": report.get("record_count"),
        "checksum_index_count": report.get("checksum_index_count"),
        "stage152_deterministic_query_ready": report.get("stage152_deterministic_query_ready"),
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "node2_raw_reveal_access": 0,
        "memory_write_enabled": False,
        "runtime_training_enabled": False,
        "next_development_order": [
            "Stage152 Deterministic Local Query / Ranking",
            "Stage153 Memory Health & Leakage Boundary",
        ],
    }
    _write_json(root / "release/current/stage151_summary.json", summary)
    return {**report, "stage151_summary": summary}


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
