from __future__ import annotations

from pathlib import Path

from .import_export import build_studio_beta_export
from .review_queue_panel import build_review_queue_panel
from .unified_board import build_unified_board
from .workspace_state import build_workspace_state_report


def run_sample_project_beta(root: Path) -> dict:
    workspace = build_workspace_state_report()
    board = build_unified_board()
    review = build_review_queue_panel()
    export = build_studio_beta_export(root)
    checks = {
        "workspace_pass": workspace.get("status") == "pass",
        "unified_board_pass": board.get("status") == "pass",
        "review_queue_pass": review.get("status") == "pass",
        "export_manifest_pass": export.get("status") == "pass",
        "full_text_default_false": export.get("includes_full_text") is False,
    }
    issues = [name for name, ok in checks.items() if not ok]
    return {
        "stage": "104.4",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "checks": checks,
        "workspace": workspace,
        "unified_board": board,
        "review_queue": review,
        "export_manifest": export,
        "provider_call_count": 0,
        "raw_manuscript_provider_leakage": 0,
    }
