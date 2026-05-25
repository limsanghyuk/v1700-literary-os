from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.page02_release_seal import run_stage154_page02_release_seal


def run_stage154(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    report = run_stage154_page02_release_seal(root)
    summary = {
        "stage": "154",
        "baseline_stage": "153",
        "title": "Page02 Release Seal",
        "status": report["status"],
        "main_report": "release/current/stage154_page02_release_seal_report.json",
        "release_gate_report": "release/current/stage154_release_gate_report.json",
        "asset_manifest": "release/current/stage154_release_asset_manifest.json",
        "evidence_pack": "release/current/stage154_page02_release_seal_pack/",
        "mode": report.get("mode"),
        "page02_sealed": report.get("page02_sealed"),
        "page02_stage_count": report.get("page02_stage_count"),
        "page02_total_stage_count": report.get("page02_total_stage_count"),
        "page02_upstream_stage_count": report.get("page02_upstream_stage_count"),
        "stage155_entry_ready": report.get("stage155_entry_ready"),
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "node2_raw_reveal_access": 0,
        "memory_write_enabled": False,
        "runtime_training_enabled": False,
        "next_development_order": ["Stage155 Page03 Entry Planning"],
    }
    _write_json(root / "release/current/stage154_summary.json", summary)
    return {**report, "stage154_summary": summary}


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
