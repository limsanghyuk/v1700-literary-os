from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.page03_release_seal import run_stage160_page03_release_seal


def run_stage160(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    report = run_stage160_page03_release_seal(root)
    summary = {
        "stage": "160",
        "baseline_stage": "159",
        "title": "Page03 Release Seal",
        "status": report["status"],
        "main_report": "release/current/stage160_page03_release_seal_report.json",
        "release_gate_report": "release/current/stage160_release_gate_report.json",
        "asset_manifest": "release/current/stage160_release_asset_manifest.json",
        "evidence_pack": "release/current/stage160_page03_release_seal_pack/",
        "page03_sealed": report.get("page03_sealed"),
        "page03_total_stage_count": report.get("page03_total_stage_count"),
        "stage161_rendering_contract_ready": report.get("stage161_rendering_contract_ready"),
        "page03_release_checksum": report.get("page03_release_checksum"),
        "provider_default_calls": 0,
        "runtime_execution_count": 0,
        "write_operation_count": 0,
        "node2_raw_reveal_access": 0,
        "next_development_order": ["Stage161 Rendering Contract"],
    }
    _write_json(root / "release/current/stage160_summary.json", summary)
    return {**report, "stage160_summary": summary}


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
