from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.user_cli_api_docs import run_stage143_user_cli_api_docs


def run_stage143(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    report = run_stage143_user_cli_api_docs(root)
    summary = {
        "stage": "143",
        "baseline_stage": "142",
        "title": "User CLI/API Minimum Docs",
        "status": report["status"],
        "main_report": "release/current/stage143_user_cli_api_docs_report.json",
        "release_gate_report": "release/current/stage143_release_gate_report.json",
        "asset_manifest": "release/current/stage143_release_asset_manifest.json",
        "evidence_pack": "release/current/stage143_user_cli_api_docs_pack/",
        "mode": report.get("mode"),
        "user_cli_api_docs_only": report.get("user_cli_api_docs_only"),
        "cli_help_available": report.get("cli_help_available"),
        "cli_json_example_valid": report.get("cli_json_example_valid"),
        "api_contract_documented_only": report.get("api_contract_documented_only"),
        "stage144_split_ci_runtime_ready": report.get("stage144_split_ci_runtime_ready"),
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "node2_raw_reveal_access": 0,
        "branchpoint_lineage_preserved": report.get("branchpoint_lineage_preserved", False),
        "next_development_order": [
            "Stage144 Split CI Runtime Strategy",
            "Roadmap terminal review after Stage144",
        ],
    }
    _write_json(root / "release/current/stage143_summary.json", summary)
    return {**report, "stage143_summary": summary}


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
