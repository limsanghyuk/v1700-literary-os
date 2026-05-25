from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.execution_dry_run_trace import run_stage159_execution_dry_run_trace


def run_stage159(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    report = run_stage159_execution_dry_run_trace(root)
    summary = {
        "stage": "159",
        "baseline_stage": "158",
        "title": "Execution Dry-Run Trace",
        "status": report["status"],
        "main_report": "release/current/stage159_execution_dry_run_trace_report.json",
        "release_gate_report": "release/current/stage159_release_gate_report.json",
        "asset_manifest": "release/current/stage159_release_asset_manifest.json",
        "evidence_pack": "release/current/stage159_execution_dry_run_trace_pack/",
        "trace_step_count": report.get("trace_step_count"),
        "trace_checksum": report.get("trace_checksum"),
        "stage160_page03_release_seal_ready": report.get("stage160_page03_release_seal_ready"),
        "runtime_execution_enabled": False,
        "provider_execution_enabled": False,
        "write_operation_count": 0,
        "provider_default_calls": 0,
        "node2_raw_reveal_access": 0,
        "next_development_order": ["Stage160 Page03 Release Seal"],
    }
    _write_json(root / "release/current/stage159_summary.json", summary)
    return {**report, "stage159_summary": summary}


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
